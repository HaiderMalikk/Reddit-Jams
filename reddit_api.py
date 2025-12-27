"""
Reddit API Module
Handles Reddit authentication and operations:
- Step 3: Search Reddit for recommendations
"""

import praw


def initialize_reddit(client_id, client_secret, username, password, user_agent):
    """
    Initialize Reddit API client
    
    Args:
        client_id: Reddit client ID
        client_secret: Reddit client secret
        username: Reddit username
        password: Reddit password
        user_agent: Reddit user agent
    
    Returns:
        Reddit client object
    """
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )
    
    print(f"Reddit API initialized (Read-only: {reddit.read_only})")
    return reddit


def search_reddit_for_recommendations(reddit, query, subreddit_name, max_posts=20, max_comments=30):
    """
    Search Reddit for recommendation posts/comments
    Focus on: "recommend", "similar to", "if you like"
    
    Args:
        reddit: Reddit client object
        query: Search query string
        subreddit_name: Name of subreddit to search
        max_posts: Maximum number of posts to retrieve
        max_comments: Maximum number of comments per post
    
    Returns:
        list: List of recommendation posts with comments
    """
    subreddit = reddit.subreddit(subreddit_name)
    recommendations = []
    
    try:
        # Search for posts
        search_results = subreddit.search(query, limit=max_posts)
        
        for post in search_results:
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
                    post.comments.replace_more(limit=0)
                    for comment in post.comments.list()[:max_comments]:
                        comment_text = comment.body.lower()
                        if any(keyword in comment_text for keyword in ['recommend', 'similar', 'if you like', 'check out', 'you might like', 'try']):
                            post_data['comments'].append({
                                'body': comment.body,
                                'score': comment.score,
                                'author': str(comment.author) if comment.author else '[deleted]'
                            })
                except Exception as e:
                    pass
                
                if post_data['comments'] or any(keyword in text for keyword in ['recommend', 'similar']):
                    recommendations.append(post_data)
    
    except Exception as e:
        print(f"   Error searching Reddit: {e}")
    
    return recommendations


def get_reddit_recommendations(reddit, tracks_data, subreddit_name, max_reddit_posts_per_query=20, max_comments_per_post=30, num_top_tracks=5, num_top_artists=3):
    """
    Step 3: Search Reddit for Recommendations
    
    Args:
        reddit: Reddit client object
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
    print("SEARCHING REDDIT FOR RECOMMENDATIONS")
    print("=" * 80)
    
    all_reddit_data = []
    
    # Search for top tracks + top artists
    top_tracks = sorted(tracks_data, key=lambda x: x['popularity'], reverse=True)[:num_top_tracks]
    all_artists = list(set([artist for track in tracks_data for artist in track['artists']]))[:num_top_artists]
    
    print(f"\nSearching for recommendations based on:")
    print(f"   - Top {len(top_tracks)} tracks")
    print(f"   - Top {len(all_artists)} artists")
    print()
    
    # Search by track name
    for idx, track in enumerate(top_tracks, 1):
        print(f"[{idx}/{len(top_tracks)}] Searching: '{track['name']}'")
        query = f"{track['name']} {track['artist_names']} recommend"
        results = search_reddit_for_recommendations(reddit, query, subreddit_name, max_reddit_posts_per_query, max_comments_per_post)
        
        if results:
            all_reddit_data.extend(results)
            print(f"         ✅ Found {len(results)} recommendation posts/threads")
        else:
            print(f"         ℹ️  No recommendations found")
    
    # Search by artist
    for idx, artist in enumerate(all_artists, 1):
        print(f"[Artist {idx}/{len(all_artists)}] Searching: '{artist}'")
        query = f"{artist} recommend similar"
        results = search_reddit_for_recommendations(reddit, query, subreddit_name, max_reddit_posts_per_query, max_comments_per_post)
        
        if results:
            all_reddit_data.extend(results)
            print(f"         Found {len(results)} recommendation posts/threads")
        else:
            print(f"         No recommendations found")
    
    print(f"\nTotal Reddit data collected: {len(all_reddit_data)} posts with recommendations")
    print(f"   Total comments: {sum(len(post['comments']) for post in all_reddit_data)}")
    
    return {
        'all_reddit_data': all_reddit_data,
        'top_tracks': top_tracks,
        'all_artists': all_artists
    }
