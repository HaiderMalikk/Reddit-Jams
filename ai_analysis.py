"""
AI Analysis Module
Handles OpenAI operations:
- Step 4: Format Data for ChatGPT
- Step 5: Get Recommendations from ChatGPT
"""

import json
from openai import OpenAI


def initialize_openai(api_key):
    """
    Initialize OpenAI client
    
    Args:
        api_key: OpenAI API key
    
    Returns:
        OpenAI client object
    """
    client = OpenAI(api_key=api_key)
    print("OpenAI API initialized")
    return client


def format_data_for_chatgpt(playlist_data, reddit_data, top_tracks, subreddit_name, num_recommendations):
    """
    Step 4: Format Data for ChatGPT
    
    Args:
        playlist_data: Dictionary with playlist information
        reddit_data: List of Reddit posts and comments
        top_tracks: List of top tracks
        subreddit_name: Name of subreddit
        num_recommendations: Number of recommendations to request
    
    Returns:
        str: Formatted prompt for ChatGPT
    """
    print("=" * 80)
    print("CREATING CHATGPT PROMPT")
    print("=" * 80)
    
    # Build playlist summary
    playlist_summary = f"Playlist: {playlist_data['name']}\n"
    playlist_summary += f"Total Tracks: {playlist_data['total_tracks']}\n\n"
    playlist_summary += "Top Tracks:\n"
    for i, track in enumerate(top_tracks[:10], 1):
        playlist_summary += f"{i}. {track['name']} - {track['artist_names']}\n"
    
    # Build Reddit recommendations summary
    reddit_summary = "\nReddit Community Recommendations:\n\n"
    for idx, post in enumerate(reddit_data[:15], 1):  # Limit to avoid token overflow
        reddit_summary += f"Post {idx}: {post['title']}\n"
        if post['body']:
            reddit_summary += f"Content: {post['body'][:300]}...\n"
        
        # Add top comments
        if post['comments']:
            reddit_summary += "Top Comments:\n"
            for comment in post['comments'][:3]:
                reddit_summary += f"  - {comment['body'][:200]}...\n"
        reddit_summary += "\n"
    
    # Create the prompt
    chatgpt_prompt = f"""You are a music recommendation expert. Based on a user's Spotify playlist and Reddit community recommendations, suggest 5 songs they will likely enjoy.

USER'S PLAYLIST:
{playlist_summary}

REDDIT RECOMMENDATIONS FROM r/{subreddit_name}:
{reddit_summary}

TASK:
Analyze the user's music taste from their playlist and the Reddit community recommendations. Recommend 5 NEW songs (not in the original playlist) that the user will love.

IMPORTANT: Return ONLY a JSON array with exactly {num_recommendations} songs in this format:
[
  {{"song": "Song Name", "artist": "Artist Name"}},
  {{"song": "Song Name", "artist": "Artist Name"}},
  ...
]

Do NOT include any explanation, just the JSON array. Make sure songs are real and can be found on Spotify."""
    
    return chatgpt_prompt


def get_chatgpt_recommendations(openai_client, chatgpt_prompt, model="gpt-4", temperature=0.7, max_tokens=500):
    """
    Step 5: Get Recommendations from ChatGPT
    
    Args:
        openai_client: OpenAI client object
        chatgpt_prompt: Formatted prompt string
        model: GPT model to use
        temperature: Temperature parameter for generation
        max_tokens: Maximum tokens for response
    
    Returns:
        list: List of song recommendations from ChatGPT
    """
    print("=" * 80)
    print("CALLING CHATGPT API")
    print("=" * 80)
    
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a music recommendation expert. Always return valid JSON."},
                {"role": "user", "content": chatgpt_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        gpt_response = response.choices[0].message.content
        print(f"ChatGPT Response received")
        print(f"\nRaw response:")
        print("-" * 80)
        print(gpt_response)
        print("-" * 80)
        
        # Parse JSON response
        gpt_recommendations = json.loads(gpt_response)
        
        print(f"\nParsed {len(gpt_recommendations)} recommendations:")
        for idx, rec in enumerate(gpt_recommendations, 1):
            print(f"   {idx}. {rec['song']} - {rec['artist']}")
        
        return gpt_recommendations
        
    except Exception as e:
        print(f"Error calling ChatGPT: {e}")
        return []


def analyze_and_recommend(openai_client, playlist_data, reddit_data, top_tracks, subreddit_name, num_recommendations=5, model="gpt-4", temperature=0.7, max_tokens=500):
    """
    Combined Steps 4 & 5: Format data and get ChatGPT recommendations
    
    Args:
        openai_client: OpenAI client object
        playlist_data: Dictionary with playlist information
        reddit_data: List of Reddit posts and comments
        top_tracks: List of top tracks
        subreddit_name: Name of subreddit
        num_recommendations: Number of recommendations to request
        model: GPT model to use
        temperature: Temperature parameter
        max_tokens: Maximum tokens for response
    
    Returns:
        list: List of song recommendations
    """
    # Step 4: Format data
    chatgpt_prompt = format_data_for_chatgpt(playlist_data, reddit_data, top_tracks, subreddit_name, num_recommendations)
    
    # Step 5: Get recommendations
    gpt_recommendations = get_chatgpt_recommendations(openai_client, chatgpt_prompt, model, temperature, max_tokens)
    
    return gpt_recommendations
