"""
Spotify API Module
Handles Spotify authentication and operations:
- Step 2: Extract playlist data
- Step 6: Search Spotify for recommended songs
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import Dict, List, Optional, Any
import os


def initialize_spotify(client_id: str, client_secret: str) -> spotipy.Spotify:
    """
    Initialize Spotify API client

    Args:
        client_id: Spotify client ID
        client_secret: Spotify client secret

    Returns:
        Spotify client object
    """
    spotify_client_credentials = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=spotify_client_credentials)

    print("Spotify API initialized (Read-only)")
    return sp


def get_playlist_id(url: str) -> str:
    """Extract playlist ID from URL"""
    return url.split("playlist/")[1].split("?")[0]


def get_playlist_data(sp: spotipy.Spotify, playlist_url: str) -> Dict[str, Any]:
    """
    Step 2: Extract Playlist Data from Spotify

    Args:
        sp: Spotify client object
        playlist_url: Spotify playlist URL

    Returns:
        dict: Contains playlist_info and tracks_data
    """
    # Get playlist data
    playlist_id = get_playlist_id(playlist_url)
    playlist = sp.playlist(playlist_id)

    print("=" * 80)
    print("PLAYLIST INFORMATION")
    print("=" * 80)
    print(f"Name: {playlist['name']}")
    print(f"Owner: {playlist['owner']['display_name']}")
    print(f"Total Tracks: {playlist['tracks']['total']}")
    print(f"Description: {playlist['description']}")
    print("=" * 80)

    # Extract tracks
    tracks_data = []
    results = sp.playlist_tracks(playlist_id)

    for idx, item in enumerate(results["items"], 1):
        track = item["track"]
        if track:
            track_info = {
                "name": track["name"],
                "artists": [artist["name"] for artist in track["artists"]],
                "artist_names": ", ".join(
                    [artist["name"] for artist in track["artists"]]
                ),
                "album": track["album"]["name"],
                "id": track["id"],
                "uri": track["uri"],
                "popularity": track["popularity"],
                "preview_url": track["preview_url"],
                "external_url": track.get("external_urls", {}).get("spotify", None),
                "album_image": track["album"]["images"][0]["url"]
                if track["album"]["images"]
                else None,
            }
            tracks_data.append(track_info)
            print(f"[{idx}] {track_info['name']} - {track_info['artist_names']}")

    print(f"\nExtracted {len(tracks_data)} tracks from playlist")

    # Store for logging
    playlist_data = {
        "name": playlist["name"],
        "owner": playlist["owner"]["display_name"],
        "total_tracks": len(tracks_data),
        "album_art": playlist["images"][0]["url"] if playlist["images"] else None,
        "tracks": tracks_data,
    }

    return {"playlist_info": playlist_data, "tracks_data": tracks_data}


def search_spotify_song(
    sp: spotipy.Spotify, song_name: str, artist_name: str
) -> Optional[Dict[str, Any]]:
    """
    Search Spotify for a song and return full track object

    Args:
        sp: Spotify client object
        song_name: Name of the song
        artist_name: Name of the artist

    Returns:
        dict: Track information or None if not found
    """
    try:
        query = f"track:{song_name} artist:{artist_name}"
        results = sp.search(q=query, type="track", limit=1)

        if results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            return {
                "name": track["name"],
                "artist": ", ".join([a["name"] for a in track["artists"]]),
                "album": track["album"]["name"],
                "release_date": track["album"]["release_date"],
                "popularity": track["popularity"],
                "duration_ms": track["duration_ms"],
                "duration_readable": f"{track['duration_ms'] // 60000}:{(track['duration_ms'] % 60000) // 1000:02d}",
                "preview_url": track["preview_url"],
                "external_url": track["external_urls"]["spotify"],
                "uri": track["uri"],
                "album_art": track["album"]["images"][0]["url"]
                if track["album"]["images"]
                else None,
                "id": track["id"],
            }
    except Exception as e:
        print(f"   Error searching for '{song_name}': {e}")

    return None


def search_spotify_recommendations(
    sp: spotipy.Spotify, gpt_recommendations: List[Dict[str, str]]
) -> List[Dict[str, Any]]:
    """
    Step 6: Search Spotify for Recommended Songs

    Args:
        sp: Spotify client object
        gpt_recommendations: List of dicts with 'song' and 'artist' keys

    Returns:
        list: List of found Spotify tracks
    """
    print("=" * 80)
    print("SEARCHING SPOTIFY FOR RECOMMENDATIONS")
    print("=" * 80)

    final_recommendations = []

    for idx, rec in enumerate(gpt_recommendations, 1):
        print(
            f"\n[{idx}/{len(gpt_recommendations)}] Searching: {rec['song']} - {rec['artist']}"
        )

        spotify_track = search_spotify_song(sp, rec["song"], rec["artist"])

        if spotify_track:
            final_recommendations.append(spotify_track)
            print(f"         Found on Spotify!")
            print(f"            Album: {spotify_track['album']}")
            print(f"            Popularity: {spotify_track['popularity']}/100")
            print(f"            URL: {spotify_track['external_url']}")
        else:
            print(f"         Not found on Spotify")

    print(
        f"\nSuccessfully found {len(final_recommendations)}/{len(gpt_recommendations)} recommendations on Spotify"
    )

    return final_recommendations
