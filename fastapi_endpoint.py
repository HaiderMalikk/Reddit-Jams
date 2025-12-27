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

app = FastAPI(
    title="RedditJams API",
    description="Song Recommendation API based on Spotify playlists and Reddit recommendations",
    version="1.0.0"
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
    playlist_name: Optional[str] = None
    recommendations: Optional[list] = None
    metadata: Optional[dict] = None
    error: Optional[str] = None


@app.post("/api/recommendations", response_model=RecommendationResponse)
async def get_song_recommendations(request: RecommendationRequest):
    """
    Get song recommendations based on Spotify playlist
    
    - **playlist_url**: Spotify playlist URL (required)
    """
    try:
        # Suppress print output during processing
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            # Call main recommendation function (async)
            result = await get_recommendations(
                playlist_url=request.playlist_url
            )
        finally:
            # Restore stdout
            sys.stdout = old_stdout
        
        # Prepare response
        return RecommendationResponse(
            success=True,
            playlist_name=result['playlist_data']['name'],
            recommendations=result['final_recommendations'],
            metadata={
                'total_tracks_analyzed': len(result['tracks_data']),
                'reddit_posts_found': len(result['reddit_data']),
                'recommendations_requested': result['metadata']['num_requested'],
                'recommendations_found': result['metadata']['num_found']
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "RedditJams API"
    }


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "RedditJams - Song Recommendation API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
