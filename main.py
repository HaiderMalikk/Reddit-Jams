"""
Main Orchestrator
Coordinates all steps of the recommendation system and displays results (Step 7)
"""

import os
import asyncio
from dotenv import load_dotenv
from spotify_api import initialize_spotify, get_playlist_data, search_spotify_recommendations
from reddit_api import get_reddit_recommendations
from ai_analysis import initialize_openai, analyze_and_recommend

# Load environment variables
load_dotenv()

# API Credentials Configuration (loaded from environment)
SPOTIFY_CLIENT_ID: str | None = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET: str | None = os.getenv('SPOTIFY_CLIENT_SECRET')
REDDIT_CLIENT_ID: str | None = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET: str | None = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME: str | None = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD: str | None = os.getenv('REDDIT_PASSWORD')
REDDIT_USER_AGENT: str | None = os.getenv('REDDIT_USER_AGENT')
OPENAI_API_KEY: str | None = os.getenv('OPENAI_API_KEY')

# GPT Model Configuration
GPT_MODEL: str = "gpt-4o-mini"
GPT_TEMPERATURE: float = 0.7
GPT_MAX_TOKENS: int = 500

# Reddit Configuration
SUBREDDIT_NAME: str = "music"
MAX_REDDIT_POSTS_PER_QUERY: int = 20
MAX_COMMENTS_PER_POST: int = 30

# Analysis Configuration
NUM_TOP_TRACKS: int = 5
NUM_TOP_ARTISTS: int = 3
NUM_RECOMMENDATIONS: int = 5


async def get_recommendations(playlist_url: str) -> dict:
    """
    Main function to get song recommendations (Async)
    
    Args:
        playlist_url: Spotify playlist URL (REQUIRED)
    
    Returns:
        dict: Contains final recommendations and metadata
    """
    
    print("=" * 80)
    print("SONG RECOMMENDATION SYSTEM")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  Playlist URL: {playlist_url}")
    print(f"  Subreddit: r/{SUBREDDIT_NAME}")
    print(f"  Max Reddit posts per query: {MAX_REDDIT_POSTS_PER_QUERY}")
    print(f"  Max comments per post: {MAX_COMMENTS_PER_POST}")
    print(f"  Number of top tracks: {NUM_TOP_TRACKS}")
    print(f"  Number of top artists: {NUM_TOP_ARTISTS}")
    print(f"  GPT Model: {GPT_MODEL}")
    print(f"  GPT Temperature: {GPT_TEMPERATURE}")
    print(f"  GPT Max Tokens: {GPT_MAX_TOKENS}")
    print(f"  Recommendations to generate: {NUM_RECOMMENDATIONS}")
    print("=" * 80)
    
    # Initialize APIs
    print("\nInitializing APIs...")
    sp = initialize_spotify(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    openai_client = initialize_openai(OPENAI_API_KEY)
    print()
    
    # Step 2: Extract Playlist Data
    playlist_result = get_playlist_data(sp, playlist_url)
    playlist_data = playlist_result['playlist_info']
    tracks_data = playlist_result['tracks_data']
    print()
    
    # Step 3: Search Reddit for Recommendations (Async)
    reddit_result = await get_reddit_recommendations(
        REDDIT_CLIENT_ID,
        REDDIT_CLIENT_SECRET,
        REDDIT_USERNAME,
        REDDIT_PASSWORD,
        REDDIT_USER_AGENT,
        tracks_data,
        SUBREDDIT_NAME,
        MAX_REDDIT_POSTS_PER_QUERY,
        MAX_COMMENTS_PER_POST,
        NUM_TOP_TRACKS,
        NUM_TOP_ARTISTS
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
        SUBREDDIT_NAME,
        NUM_RECOMMENDATIONS,
        GPT_MODEL,
        GPT_TEMPERATURE,
        GPT_MAX_TOKENS
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
            'subreddit': SUBREDDIT_NAME,
            'num_requested': NUM_RECOMMENDATIONS,
            'num_found': len(final_recommendations)
        }
    }


if __name__ == "__main__":
    # Example usage - can be run directly
    PLAYLIST_URL = "https://open.spotify.com/playlist/3XyDvjoxiae0oWpfJ4kga9?si=d2f57623799b4ebb"
    
    result = asyncio.run(get_recommendations(playlist_url=PLAYLIST_URL))
    
    print("\nRecommendation system completed!")
    print(f"   Found {len(result['final_recommendations'])}/{result['metadata']['num_requested']} recommendations")
