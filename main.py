"""
Main Orchestrator
Coordinates all steps of the recommendation system and displays results (Step 7)
"""

import os
from dotenv import load_dotenv
from spotify_api import initialize_spotify, get_playlist_data, search_spotify_recommendations
from reddit_api import initialize_reddit, get_reddit_recommendations
from ai_analysis import initialize_openai, analyze_and_recommend


def get_recommendations(
    # Required parameters
    playlist_url,
    
    # Spotify parameters (optional - loaded from env)
    spotify_client_id=None,
    spotify_client_secret=None,
    
    # Reddit parameters (optional - loaded from env)
    reddit_client_id=None,
    reddit_client_secret=None,
    reddit_username=None,
    reddit_password=None,
    reddit_user_agent=None,
    subreddit_name="music",
    max_reddit_posts_per_query=20,
    max_comments_per_post=30,
    num_top_tracks=5,
    num_top_artists=3,
    
    # OpenAI parameters (optional - loaded from env)
    openai_api_key=None,
    gpt_model="gpt-4",
    gpt_temperature=0.7,
    gpt_max_tokens=500,
    num_recommendations=5
):
    """
    Main function to get song recommendations
    
    Args:
        playlist_url (str): Spotify playlist URL (REQUIRED)
        
        Spotify params:
            spotify_client_id (str): Spotify client ID
            spotify_client_secret (str): Spotify client secret
        
        Reddit params:
            reddit_client_id (str): Reddit client ID
            reddit_client_secret (str): Reddit client secret
            reddit_username (str): Reddit username
            reddit_password (str): Reddit password
            reddit_user_agent (str): Reddit user agent
            subreddit_name (str): Name of subreddit to search (default: "music")
            max_reddit_posts_per_query (int): Max posts per query (default: 20)
            max_comments_per_post (int): Max comments per post (default: 30)
            num_top_tracks (int): Number of top tracks to search (default: 5)
            num_top_artists (int): Number of top artists to search (default: 3)
        
        OpenAI params:
            openai_api_key (str): OpenAI API key
            gpt_model (str): GPT model to use (default: "gpt-4")
            gpt_temperature (float): Temperature parameter (default: 0.7)
            gpt_max_tokens (int): Max tokens for response (default: 500)
            num_recommendations (int): Number of recommendations (default: 5)
    
    Returns:
        dict: Contains final recommendations and metadata
    """
    
    # Load environment variables if not provided
    load_dotenv()
    
    # Use provided parameters or fall back to environment variables
    spotify_client_id = spotify_client_id or os.getenv('SPOTIFY_CLIENT_ID')
    spotify_client_secret = spotify_client_secret or os.getenv('SPOTIFY_CLIENT_SECRET')
    
    reddit_client_id = reddit_client_id or os.getenv('REDDIT_CLIENT_ID')
    reddit_client_secret = reddit_client_secret or os.getenv('REDDIT_CLIENT_SECRET')
    reddit_username = reddit_username or os.getenv('REDDIT_USERNAME')
    reddit_password = reddit_password or os.getenv('REDDIT_PASSWORD')
    reddit_user_agent = reddit_user_agent or os.getenv('REDDIT_USER_AGENT')
    
    openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
    
    print("=" * 80)
    print("SONG RECOMMENDATION SYSTEM")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  Playlist URL: {playlist_url}")
    print(f"  Subreddit: r/{subreddit_name}")
    print(f"  Max Reddit posts per query: {max_reddit_posts_per_query}")
    print(f"  Max comments per post: {max_comments_per_post}")
    print(f"  Number of top tracks: {num_top_tracks}")
    print(f"  Number of top artists: {num_top_artists}")
    print(f"  GPT Model: {gpt_model}")
    print(f"  GPT Temperature: {gpt_temperature}")
    print(f"  GPT Max Tokens: {gpt_max_tokens}")
    print(f"  Recommendations to generate: {num_recommendations}")
    print("=" * 80)
    
    # Initialize APIs
    print("\nInitializing APIs...")
    sp = initialize_spotify(spotify_client_id, spotify_client_secret)
    reddit = initialize_reddit(reddit_client_id, reddit_client_secret, reddit_username, reddit_password, reddit_user_agent)
    openai_client = initialize_openai(openai_api_key)
    print()
    
    # Step 2: Extract Playlist Data
    playlist_result = get_playlist_data(sp, playlist_url)
    playlist_data = playlist_result['playlist_info']
    tracks_data = playlist_result['tracks_data']
    print()
    
    # Step 3: Search Reddit for Recommendations
    reddit_result = get_reddit_recommendations(
        reddit,
        tracks_data,
        subreddit_name,
        max_reddit_posts_per_query,
        max_comments_per_post,
        num_top_tracks,
        num_top_artists
    )
    all_reddit_data = reddit_result['all_reddit_data']
    top_tracks = reddit_result['top_tracks']
    all_artists = reddit_result['all_artists']
    print()
    
    # Steps 4 & 5: Format Data and Get ChatGPT Recommendations
    gpt_recommendations = analyze_and_recommend(
        openai_client,
        playlist_data,
        all_reddit_data,
        top_tracks,
        subreddit_name,
        num_recommendations,
        gpt_model,
        gpt_temperature,
        gpt_max_tokens
    )
    print()
    
    # Step 6: Search Spotify for Recommended Songs
    final_recommendations = search_spotify_recommendations(sp, gpt_recommendations)
    print()
    
    print("\n" + "=" * 80)
    print("FINAL SONG RECOMMENDATIONS")
    print("=" * 80)
    
    if final_recommendations:
        for idx, track in enumerate(final_recommendations, 1):
            print(f"\n{idx}. {track['name']}")
            print(f"   Artist: {track['artist']}")
            print(f"   Album: {track['album']}")
            print(f"   Release: {track['release_date']}")
            print(f"   Duration: {track['duration_readable']}")
            print(f"   Popularity: {track['popularity']}/100")
            print(f"   Listen: {track['external_url']}")
            if track['album_art']:
                print(f"   Album Art: {track['album_art']}")
            if track['preview_url']:
                print(f"   Preview: {track['preview_url']}")
            print(f"   URI: {track['uri']}")
    else:
        print("No recommendations found.")
    
    print("\n" + "=" * 80)
    
    # Return structured data
    return {
        'playlist_data': playlist_data,
        'tracks_data': tracks_data,
        'reddit_data': all_reddit_data,
        'top_tracks': top_tracks,
        'top_artists': all_artists,
        'gpt_recommendations': gpt_recommendations,
        'final_recommendations': final_recommendations,
        'metadata': {
            'subreddit': subreddit_name,
            'num_requested': num_recommendations,
            'num_found': len(final_recommendations)
        }
    }


if __name__ == "__main__":
    # Example usage - can be run directly
    PLAYLIST_URL = "https://open.spotify.com/playlist/3XyDvjoxiae0oWpfJ4kga9?si=d2f57623799b4ebb"
    
    result = get_recommendations(playlist_url=PLAYLIST_URL)
    
    print("\nRecommendation system completed!")
    print(f"   Found {len(result['final_recommendations'])}/{result['metadata']['num_requested']} recommendations")
