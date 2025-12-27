"""
Flask API for Song Recommendation System
Receives configuration from website and returns song recommendations as JSON
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from main import get_recommendations
import sys
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests


@app.route('/api/recommendations', methods=['POST'])
def get_song_recommendations():
    """
    API endpoint to get song recommendations
    
    Expected JSON payload:
    {
        "playlist_url": "https://open.spotify.com/playlist/...",  # REQUIRED
        "subreddit_name": "music",  # Optional, default: "music"
        "max_reddit_posts_per_query": 20,  # Optional, default: 20
        "max_comments_per_post": 30,  # Optional, default: 30
        "num_top_tracks": 5,  # Optional, default: 5
        "num_top_artists": 3,  # Optional, default: 3
        "gpt_model": "gpt-4",  # Optional, default: "gpt-4"
        "gpt_temperature": 0.7,  # Optional, default: 0.7
        "gpt_max_tokens": 500,  # Optional, default: 500
        "num_recommendations": 5  # Optional, default: 5
    }
    
    Returns:
        JSON response with recommendations
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required field
        if not data or 'playlist_url' not in data:
            return jsonify({
                'error': 'playlist_url is required',
                'success': False
            }), 400
        
        # Extract parameters with defaults
        playlist_url = data['playlist_url']
        subreddit_name = data.get('subreddit_name', 'music')
        max_reddit_posts_per_query = data.get('max_reddit_posts_per_query', 20)
        max_comments_per_post = data.get('max_comments_per_post', 30)
        num_top_tracks = data.get('num_top_tracks', 5)
        num_top_artists = data.get('num_top_artists', 3)
        gpt_model = data.get('gpt_model', 'gpt-4')
        gpt_temperature = data.get('gpt_temperature', 0.7)
        gpt_max_tokens = data.get('gpt_max_tokens', 500)
        num_recommendations = data.get('num_recommendations', 5)
        
        # Suppress print output during processing
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            # Call main recommendation function
            result = get_recommendations(
                playlist_url=playlist_url,
                subreddit_name=subreddit_name,
                max_reddit_posts_per_query=max_reddit_posts_per_query,
                max_comments_per_post=max_comments_per_post,
                num_top_tracks=num_top_tracks,
                num_top_artists=num_top_artists,
                gpt_model=gpt_model,
                gpt_temperature=gpt_temperature,
                gpt_max_tokens=gpt_max_tokens,
                num_recommendations=num_recommendations
            )
        finally:
            # Restore stdout
            sys.stdout = old_stdout
        
        # Prepare response
        response = {
            'success': True,
            'playlist_name': result['playlist_data']['name'],
            'recommendations': result['final_recommendations'],
            'metadata': {
                'total_tracks_analyzed': len(result['tracks_data']),
                'reddit_posts_found': len(result['reddit_data']),
                'recommendations_requested': result['metadata']['num_requested'],
                'recommendations_found': result['metadata']['num_found']
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'RedditJams API'
    }), 200


@app.route('/', methods=['GET'])
def home():
    """Root endpoint with API documentation"""
    return jsonify({
        'service': 'RedditJams - Song Recommendation API',
        'version': '1.0',
        'endpoints': {
            '/api/recommendations': {
                'method': 'POST',
                'description': 'Get song recommendations based on Spotify playlist',
                'required_params': ['playlist_url'],
                'optional_params': [
                    'subreddit_name', 'max_reddit_posts_per_query', 
                    'max_comments_per_post', 'num_top_tracks', 
                    'num_top_artists', 'gpt_model', 'gpt_temperature', 
                    'gpt_max_tokens', 'num_recommendations'
                ]
            },
            '/api/health': {
                'method': 'GET',
                'description': 'Health check endpoint'
            }
        }
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
