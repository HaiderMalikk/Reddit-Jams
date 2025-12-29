"""
FastAPI for Song Recommendation System
Receives playlist url from website and returns song recommendations as JSON
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from main import get_recommendations
import sys
import io
from spotipy.exceptions import SpotifyException

app = FastAPI(
    title="RedditJams API",
    description="Song Recommendation API based on Spotify playlists and Reddit recommendations",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendationRequest(BaseModel):
    playlist_url: str


class RecommendationResponse(BaseModel):
    success: bool
    playlist_details: Optional[dict] = None
    recommendations: Optional[list] = None
    metadata: Optional[dict] = None
    error: Optional[str] = None


@app.post("/api/recommendations", response_model=RecommendationResponse)
async def get_song_recommendations(request: RecommendationRequest):
    """
    Get song recommendations based on Spotify playlist

    - **playlist_url**: Spotify playlist URL (required)
    """
    # Validate that the URL starts with the correct Spotify playlist URL format
    if not request.playlist_url.startswith("https://open.spotify.com/playlist/"):
        return RecommendationResponse(
            success=False,
            error="Invalid playlist URL. Please provide a valid Spotify playlist link that starts with 'https://open.spotify.com/playlist/'",
        )

    try:
        # Suppress print output during processing
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            # Call main recommendation function (async)
            result = await get_recommendations(playlist_url=request.playlist_url)
        finally:
            # Restore stdout
            sys.stdout = old_stdout

        # Prepare response
        return RecommendationResponse(
            success=True,
            playlist_details={
                "name": result["playlist_data"]["name"],
                "owner": result["playlist_data"]["owner"],
                "total_tracks": result["playlist_data"]["total_tracks"],
                "album_art": result["playlist_data"]["album_art"],
            },
            recommendations=result["final_recommendations"],
            metadata={
                "total_tracks_analyzed": len(result["tracks_data"]),
                "reddit_posts_found": len(result["reddit_data"]),
                "recommendations_requested": result["metadata"]["num_requested"],
                "recommendations_found": result["metadata"]["num_found"],
            },
        )

    except SpotifyException as e:
        # Restore stdout if it was redirected
        if "old_stdout" in locals():
            sys.stdout = old_stdout

        # Handle Spotify API errors consistently
        error_message = str(e)

        # Check for invalid playlist ID (400) - malformed URL
        if "http status: 400" in error_message or "Invalid base62 id" in error_message:
            return RecommendationResponse(
                success=False,
                error="Invalid playlist URL. Please check the link and try again.",
            )
        # Check for private/not found playlist (404)
        elif (
            "http status: 404" in error_message or "Resource not found" in error_message
        ):
            return RecommendationResponse(
                success=False,
                error="Playlist not found. It may be private or deleted. Please make sure the playlist exists and is public.",
            )
        else:
            # Any other Spotify error - internal error
            return RecommendationResponse(
                success=False, error="Internal error. Please try again later."
            )

    except Exception as e:
        # Restore stdout if it was redirected
        if "old_stdout" in locals():
            sys.stdout = old_stdout

        # Generic error handler - internal error
        return RecommendationResponse(
            success=False, error="Internal error. Please try again later."
        )


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RedditJams API"}


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "RedditJams - Song Recommendation API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
