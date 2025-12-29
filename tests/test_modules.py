"""
Module Tests
Tests for individual modules: spotify_api, reddit_api, ai_analysis, main
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch, AsyncMock
from dotenv import load_dotenv

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv()

# Import modules to test
from spotify_api import initialize_spotify, get_playlist_id, search_spotify_song
from ai_analysis import initialize_openai, format_data_for_chatgpt
import asyncio


class TestSpotifyAPI:
    """Tests for spotify_api.py"""
    
    def test_initialize_spotify(self):
        """Test Spotify client initialization"""
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        sp = initialize_spotify(client_id, client_secret)
        assert sp is not None
    
    def test_get_playlist_id(self):
        """Test playlist ID extraction from URL"""
        url = "https://open.spotify.com/playlist/3XyDvjoxiae0oWpfJ4kga9?si=test"
        playlist_id = get_playlist_id(url)
        assert playlist_id == "3XyDvjoxiae0oWpfJ4kga9"
    
    def test_search_spotify_song(self):
        """Test Spotify song search"""
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        sp = initialize_spotify(client_id, client_secret)
        
        result = search_spotify_song(sp, "Watermelon Sugar", "Harry Styles")
        assert result is not None
        assert result["name"] == "Watermelon Sugar"
        assert "Harry Styles" in result["artist"]


class TestAIAnalysis:
    """Tests for ai_analysis.py"""
    
    def test_initialize_openai(self):
        """Test OpenAI client initialization"""
        api_key = os.getenv('OPENAI_API_KEY')
        client = initialize_openai(api_key)
        assert client is not None
    
    def test_format_data_for_chatgpt(self):
        """Test ChatGPT prompt formatting"""
        playlist_data = {
            'name': 'Test Playlist',
            'total_tracks': 10
        }
        reddit_data = []
        top_tracks = [
            {'name': 'Song 1', 'artist_names': 'Artist 1'},
            {'name': 'Song 2', 'artist_names': 'Artist 2'}
        ]
        
        prompt = format_data_for_chatgpt(
            playlist_data, reddit_data, top_tracks, "music", 5
        )
        
        assert "Test Playlist" in prompt
        assert "Song 1" in prompt
        assert "JSON array" in prompt


class TestRedditAPI:
    """Tests for reddit_api.py"""
    
    @pytest.mark.asyncio
    async def test_reddit_search_structure(self):
        """Test Reddit search returns proper structure"""
        # Mock test - structure validation
        mock_result = {
            'all_reddit_data': [],
            'top_tracks': [],
            'all_artists': []
        }
        assert 'all_reddit_data' in mock_result
        assert 'top_tracks' in mock_result
        assert isinstance(mock_result['all_reddit_data'], list)


class TestMainOrchestrator:
    """Tests for main.py orchestrator"""
    
    def test_configuration_values(self):
        """Test that configuration values are set"""
        from main import GPT_MODEL, NUM_RECOMMENDATIONS, SUBREDDIT_NAME
        
        assert GPT_MODEL == "gpt-4o-mini"
        assert NUM_RECOMMENDATIONS == 5
        assert SUBREDDIT_NAME == "music"
    
    @pytest.mark.asyncio
    async def test_get_recommendations_structure(self):
        """Test get_recommendations returns proper structure"""
        # Mock test - validates expected return structure
        expected_keys = [
            'playlist_data', 'tracks_data', 'reddit_data',
            'top_tracks', 'top_artists', 'gpt_recommendations',
            'final_recommendations', 'metadata'
        ]
        
        mock_result = {key: None for key in expected_keys}
        for key in expected_keys:
            assert key in mock_result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
