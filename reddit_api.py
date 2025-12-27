"""
Reddit API Module
Handles Reddit authentication and operations:
- Step 3: Search Reddit for recommendations (Async with parallel searches)
"""

import asyncpraw
import asyncio
from typing import Dict, List, Any


def initialize_reddit(client_id: str, client_secret: str, username: str, password: str, user_agent: str) -> asyncpraw.Reddit:
    """
    Initialize async Reddit API client
    
    Args:
        client_id: Reddit client ID
        client_secret: Reddit client secret
        username: Reddit username
        password: Reddit password
        user_agent: Reddit user agent
    
    Returns:
        Async Reddit client object
    """
    reddit = asyncpraw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )
    
    print(f"Async Reddit API initialized")
    return reddit


async def search_reddit_for_recommendations(reddit: asyncpraw.Reddit, query: str, subreddit_name: str, max_posts: int = 20, max_comments: int = 30) -> List[Dict[str, Any]]:
    """
    Search Reddit for recommendation posts/comments (Async)
    Focus on: "recommend", "similar to", "if you like"
    
    Args:
        reddit: Async Reddit client object
        query: Search query string
        subreddit_name: Name of subreddit to search
        max_posts: Maximum number of posts to retrieve
        max_comments: Maximum number of comments per post
    
    Returns:
        list: List of recommendation posts with comments
    """
    subreddit = await reddit.subreddit(subreddit_name)
    recommendations = []
    
    try:
        # Search for posts
        search_results = subreddit.search(query, limit=max_posts)
        
        async for post in search_results:
            # Look for recommendation keywords in title or body
            text = f"{post.title} {post.selftext}".lower()
            
            if any(keyword in text for keyword in ['recommend', 'similar', 'if you like', 'check out', 'you might like', 'fans of']):
                post_data = {
                    'title': post.title,
                    'body': post.selftext,
                    'score': post.score,
                    'url': f"https://reddit.com{post.permalink}",
                    'comments': []
                }
                
                # Get comments
                try:
                    await post.comments.replace_more(limit=0)
                    all_comments = post.comments.list()
                    
                    for comment in all_comments[:max_comments]:
                        try:
                            comment_text = comment.body.lower()
                            if any(keyword in comment_text for keyword in ['recommend', 'similar', 'if you like', 'check out', 'you might like', 'try']):
                                post_data['comments'].append({
                                    'body': comment.body,
                                    'score': comment.score,
                                    'author': str(comment.author) if comment.author else '[deleted]'
                                })
                        except AttributeError:
                            # Skip if comment doesn't have body attribute (e.g., MoreComments object)
                            continue
                except Exception as e:
                    pass
                
                if post_data['comments'] or any(keyword in text for keyword in ['recommend', 'similar']):
                    recommendations.append(post_data)
    
    except Exception as e:
        print(f"   Error searching Reddit: {e}")
    
    return recommendations


async def get_reddit_recommendations(client_id: str, client_secret: str, username: str, password: str, user_agent: str, tracks_data: List[Dict[str, Any]], subreddit_name: str, max_reddit_posts_per_query: int = 20, max_comments_per_post: int = 30, num_top_tracks: int = 5, num_top_artists: int = 3) -> Dict[str, Any]:
    """
    Step 3: Search Reddit for Recommendations (Async with parallel searches)
    
    Args:
        client_id: Reddit client ID
        client_secret: Reddit client secret
        username: Reddit username
        password: Reddit password
        user_agent: Reddit user agent
        tracks_data: List of track dictionaries from Spotify
        subreddit_name: Name of subreddit to search
        max_reddit_posts_per_query: Maximum posts to fetch per query
        max_comments_per_post: Maximum comments per post
        num_top_tracks: Number of top tracks to search for
        num_top_artists: Number of top artists to search for
    
    Returns:
        dict: Contains all_reddit_data, top_tracks, and all_artists
    """
    print("=" * 80)
    print("SEARCHING REDDIT FOR RECOMMENDATIONS (PARALLEL)")
    print("=" * 80)
    
    # Initialize Reddit client within async context
    async with asyncpraw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    ) as reddit:
        print("Async Reddit API initialized")
        
        # Search for top tracks + top artists
        top_tracks = sorted(tracks_data, key=lambda x: x['popularity'], reverse=True)[:num_top_tracks]
        all_artists = list(set([artist for track in tracks_data for artist in track['artists']]))[:num_top_artists]
        
        print(f"\nSearching for recommendations based on:")
        print(f"   - Top {len(top_tracks)} tracks")
        print(f"   - Top {len(all_artists)} artists")
        print(f"   - Running ALL searches in parallel...")
        print()
        
        # Create all search tasks for tracks
        track_search_tasks = []
        for idx, track in enumerate(top_tracks, 1):
            query = f"{track['name']} {track['artist_names']} recommend"
            print(f"[Track {idx}/{len(top_tracks)}] Queuing: '{track['name']}'")
            task = search_reddit_for_recommendations(reddit, query, subreddit_name, max_reddit_posts_per_query, max_comments_per_post)
            track_search_tasks.append(task)
        
        # Create all search tasks for artists
        artist_search_tasks = []
        for idx, artist in enumerate(all_artists, 1):
            query = f"{artist} recommend similar"
            print(f"[Artist {idx}/{len(all_artists)}] Queuing: '{artist}'")
            task = search_reddit_for_recommendations(reddit, query, subreddit_name, max_reddit_posts_per_query, max_comments_per_post)
            artist_search_tasks.append(task)
        
        print(f"\nExecuting {len(track_search_tasks) + len(artist_search_tasks)} searches in parallel...")
        print()
        
        # Run ALL searches in parallel (tracks + artists together)
        all_results = await asyncio.gather(*track_search_tasks, *artist_search_tasks)
        
        # Flatten all results and show individual search results
        all_reddit_data = []
        
        # Display track search results
        for idx, results in enumerate(all_results[:len(top_tracks)], 1):
            track_name = top_tracks[idx-1]['name']
            if results:
                all_reddit_data.extend(results)
                print(f"[{idx}/{len(top_tracks)}] Searching: '{track_name}'")
                print(f"         Found {len(results)} recommendation posts/threads")
            else:
                print(f"[{idx}/{len(top_tracks)}] Searching: '{track_name}'")
                print(f"         No recommendations found")
        
        # Display artist search results
        for idx, results in enumerate(all_results[len(top_tracks):], 1):
            artist_name = all_artists[idx-1]
            if results:
                all_reddit_data.extend(results)
                print(f"[Artist {idx}/{len(all_artists)}] Searching: '{artist_name}'")
                print(f"         Found {len(results)} recommendation posts/threads")
            else:
                print(f"[Artist {idx}/{len(all_artists)}] Searching: '{artist_name}'")
                print(f"         No recommendations found")
        
        print(f"\nTotal Reddit data collected: {len(all_reddit_data)} posts with recommendations")
        print(f"   Total comments: {sum(len(post['comments']) for post in all_reddit_data)}")

    return {
        'all_reddit_data': all_reddit_data,
        'top_tracks': top_tracks,
        'all_artists': all_artists
    }
