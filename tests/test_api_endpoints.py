"""
API Endpoint Tests
Tests for FastAPI endpoints including success and error cases
"""

import pytest
import requests

BASE_URL = "https://reddit-jams-backend.vercel.app"

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "RedditJams API"


def test_root_endpoint():
    """Test root endpoint"""
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "RedditJams - Song Recommendation API"
    assert data["version"] == "1.0.0"


def test_successful_recommendation():
    """Test successful playlist recommendation"""
    payload = {
        "playlist_url": "https://open.spotify.com/playlist/3XyDvjoxiae0oWpfJ4kga9"
    }
    response = requests.post(
        f"{BASE_URL}/api/recommendations",
        json=payload,
        timeout=120  # Increased timeout for processing
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["playlist_name"] is not None
    assert len(data["recommendations"]) > 0
    assert data["error"] is None
    assert "metadata" in data


def test_private_playlist_error():
    """Test private playlist returns proper error"""
    payload = {
        "playlist_url": "https://open.spotify.com/playlist/7w46rm4NCAbC8aExBlYeNR?si=5754b28e10d64c85&nd=1&dlsi=2cb7428bb7744793"
    }
    response = requests.post(
        f"{BASE_URL}/api/recommendations",
        json=payload,
        timeout=30
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "private" in data["error"].lower() or "not found" in data["error"].lower()
    assert data["recommendations"] is None


def test_invalid_playlist_url():
    """Test invalid/non-existent playlist URL"""
    payload = {
        "playlist_url": "https://open.spotify.com/playlist/7w46rm4NCAbC8aExBlNR"
    }
    response = requests.post(
        f"{BASE_URL}/api/recommendations",
        json=payload,
        timeout=30
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"] is not None
    assert data["recommendations"] is None


def test_malformed_request():
    """Test malformed request without playlist_url"""
    payload = {}
    response = requests.post(
        f"{BASE_URL}/api/recommendations",
        json=payload,
        timeout=30
    )
    assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
