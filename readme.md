![alt text](assets/logowtext.svg)

# RedditJams - Music Recommendation APP

**RedditJams** is an intelligent music recommendation system that analyzes your Spotify playlist, searches Reddit's music community for similar tastes, and uses GPT-4 to generate personalized song recommendations.

---

## What It Does

Simply provide a **Spotify playlist URL**, and RedditJams will:

1. **Analyze your playlist** - Extracts your top tracks and artists based on popularity
2. **Search Reddit** - Finds music recommendation posts/threads from r/music community
3. **AI Analysis** - Uses GPT-4 to analyze both your taste and Reddit recommendations
4. **Return Results** - Delivers 5 personalized song recommendations with Spotify links

---

## How to Use the API

### API Endpoint

```
POST coming soon...
```

### Request Format

Send a POST request with JSON body containing your Spotify playlist URL (for how to get your spotify playlist url visit the website):

```json
{
  "playlist_url": "https://open.spotify.com/playlist/3XyDvjoxiae0oWpfJ4kga9"
}
```

### Example cURL Request

```bash
curl -X POST http://your-domain.com:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"playlist_url": "https://open.spotify.com/playlist/YOUR_PLAYLIST_ID"}'
```

---

## API Response

The API returns a JSON object with your personalized recommendations:

```json
{
  "success": true,
  "playlist_name": "My Awesome Playlist",
  "recommendations": [
    {
      "name": "Watermelon Sugar",
      "artist": "Harry Styles",
      "album": "Fine Line",
      "release_date": "2019-12-13",
      "duration_ms": 174000,
      "duration_readable": "2:54",
      "popularity": 85,
      "external_url": "https://open.spotify.com/track/6UelLqGlWMcVH1E5c4H7lY",
      "preview_url": "https://p.scdn.co/mp3-preview/...",
      "uri": "spotify:track:6UelLqGlWMcVH1E5c4H7lY",
      "album_art": "https://i.scdn.co/image/ab67616d0000b273..."
    },
    {
      "name": "Fast Car",
      "artist": "Tracy Chapman",
      "album": "Tracy Chapman",
      "release_date": "1988-04-05",
      "duration_ms": 296933,
      "duration_readable": "4:56",
      "popularity": 78,
      "external_url": "https://open.spotify.com/track/2Kerz9H9IejzeIpjhDJoYG",
      "preview_url": "https://p.scdn.co/mp3-preview/...",
      "uri": "spotify:track:2Kerz9H9IejzeIpjhDJoYG",
      "album_art": "https://i.scdn.co/image/ab67616d0000b273..."
    }
  ],
  "metadata": {
    "total_tracks_analyzed": 69,
    "reddit_posts_found": 62,
    "recommendations_requested": 2,
    "recommendations_found": 2,
  }
  "error": null
}
```

### Response Fields

- **success** - Boolean indicating if the request succeeded
- **playlist_name** - Name of your Spotify playlist
- **recommendations** - Array of recommended songs with full details:
  - `name` - Song title
  - `artist` - Artist name
  - `album` - Album name
  - `release_date` - Release date (YYYY-MM-DD)
  - `duration_ms` - Duration in milliseconds
  - `duration_readable` - Human-readable duration (M:SS)
  - `popularity` - Spotify popularity score (0-100)
  - `external_url` - Direct Spotify link to the song
  - `preview_url` - 30-second preview URL (if available)
  - `uri` - Spotify URI for the track
  - `album_art` - Album artwork URL
- **metadata** - Statistics about the recommendation process:
  - `total_tracks_analyzed` - Number of tracks in your playlist
  - `reddit_posts_found` - Number of Reddit posts analyzed
  - `recommendations_requested` - Number of recommendations requested (default: 5)
  - `recommendations_found` - Number of recommendations successfully found on Spotify

---

## How It Works

### The Algorithm

RedditJams uses a multi-step process to generate highly personalized recommendations:

#### **Step 1: Playlist Analysis**
- Connects to Spotify API using your playlist URL
- Extracts all tracks with metadata (name, artist, popularity, etc.)
- Identifies your **top 5 most popular tracks**
- Identifies your **top 3 most frequent artists**

#### **Step 2: Reddit Community Search (Parallel)**
The system searches Reddit's r/music community in parallel for similar music tastes:

**Track-Based Searches (5 parallel queries):**
- For each of your top 5 tracks, searches Reddit for: `"[track name] [artist] recommend"`
- Example: `"Running Up That Hill Kate Bush recommend"`
- Finds posts where users recommend songs similar to your favorites

**Artist-Based Searches (3 parallel queries):**
- For each of your top 3 artists, searches Reddit for: `"[artist name] recommend similar"`
- Example: `"Kate Bush recommend similar"`
- Finds posts recommending artists/songs similar to your favorites

**Total: 8 simultaneous Reddit searches** - All executed in parallel for maximum speed

**Keyword Filtering:**
Only keeps posts/comments containing recommendation keywords:
- "recommend"
- "similar to"
- "if you like"
- "check out"
- "you might like"
- "fans of"
- "try"

#### **Step 3: AI-Powered Analysis**
- Sends your playlist data + Reddit recommendations to **GPT-4**
- GPT-4 analyzes patterns in your music taste
- Considers community recommendations from Reddit
- Generates **5 new song suggestions** (not in your original playlist)
- Returns songs as JSON: `[{"song": "Title", "artist": "Artist"}, ...]`

#### **Step 4: Spotify Verification**
- Searches Spotify for each GPT-4 recommendation
- Retrieves full track details (album art, preview URLs, popularity, etc.)
- Ensures all recommendations are real, playable songs
- Returns complete track information with direct Spotify links

#### **Step 5: Results Delivery**
- Returns formatted JSON response with all recommendations
- Includes metadata about the recommendation process
- Ready to display in your application

---

## Configuration

The API uses the following default configuration:

| Parameter | Default | Description |
|-----------|---------|-------------|
| Subreddit | `music` | Reddit community to search |
| Reddit Posts Per Query | 20 | Max posts to fetch per search |
| Comments Per Post | 30 | Max comments to analyze per post |
| Top Tracks | 5 | Number of top tracks to analyze |
| Top Artists | 3 | Number of top artists to analyze |
| Recommendations | 5 | Number of songs to recommend |
| GPT Model | `gpt-4o-mini` | AI model for analysis |
| GPT Temperature | 0.7 | Creativity level (0-1) |

---

## Why It Works

**Community Intelligence:** Reddit's music community shares authentic recommendations based on real listening experiences, not just algorithmic similarities.

**Multi-Source Analysis:** Combines your actual playlist data with community wisdom, providing recommendations that are both personalized AND discovery-oriented.

**AI Understanding:** GPT-4 understands music context, genres, moods, and can identify nuanced patterns that simple collaborative filtering misses.

**Parallel Processing:** All Reddit searches run simultaneously using async/await, making the API fast despite searching multiple queries.

**Real Spotify Integration:** Every recommendation is verified on Spotify with full metadata, ensuring you can instantly play any suggested song.

---

## Additional Endpoints

### Health Check
```bash
GET http://your-domain.com:8000/api/health
```

Returns:
```json
{
  "status": "healthy",
  "service": "RedditJams API"
}
```

### API Documentation
```bash
GET http://your-domain.com:8000/docs
```

Opens interactive Swagger UI documentation where you can test the API directly in your browser.

---

## Example Use Case

**Your Input:**
```json
{
  "playlist_url": "https://open.spotify.com/playlist/3XyDvjoxiae0oWpfJ4kga9"
}
```

**What Happens:**
1. Analyzes 69 tracks from your playlist
2. Identifies top tracks: "DAISIES", "Running Up That Hill", "Lover, You Should've Come Over"
3. Identifies top artists: "Kate Bush", "Fleetwood Mac", "Jeff Buckley"
4. Searches Reddit for 8 different recommendation queries in parallel
5. Finds 62 Reddit posts with music recommendations
6. GPT-4 analyzes all data and suggests 5 new songs
7. Verifies all songs exist on Spotify
8. Returns complete track information with links

**Result:**
You get 5 personalized song recommendations you've never heard, based on your taste + community wisdom, ready to play on Spotify.

---

## Privacy & Data

- **No Data Storage:** The API doesn't store your playlist data or recommendations
- **No Authentication Required:** Public playlists can be analyzed without Spotify login
- **Read-Only Access:** Only reads playlist data, never modifies your Spotify account
- **Anonymous Reddit Search:** Searches public Reddit posts, no account needed

---

## Tips for Best Results

1. **Use Diverse Playlists:** Playlists with varied tracks get more interesting recommendations
2. **Include Popular Songs:** Well-known tracks have more Reddit discussions
3. **Genre Consistency:** Playlists focused on specific genres get more relevant suggestions
4. **Longer Playlists:** More tracks = better understanding of your taste (ideal: 30+ songs)

---

## Technology Stack

### Backend
- **FastAPI** - High-performance async web framework
- **AsyncPRAW** - Asynchronous Reddit API wrapper (parallel searches)
- **Spotipy** - Spotify API integration
- **OpenAI GPT-4** - AI-powered recommendation analysis
- **Python asyncio** - Concurrent processing for speed
- **Vercel** - Deployment

### Frontend
- **Next.js** - React framework for the web interface
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Vercel** - Deployment and analytics tracking

---

## API Error Handling

The API returns consistent error responses in the `error` field:

### Success Response
```json
{
  "success": true,
  "playlist_name": "My Playlist",
  "recommendations": [...],
  "metadata": {...},
  "error": null
}
```

### Error Responses

**Invalid Playlist URL** (malformed link):
```json
{
  "success": false,
  "error": "Invalid playlist URL. Please check the link and try again."
}
```

**Playlist Not Found** (private or deleted):
```json
{
  "success": false,
  "error": "Playlist not found. It may be private or deleted. Please make sure the playlist exists and is public."
}
```

**Internal Error** (API failures, rate limits, etc.):
```json
{
  "success": false,
  "error": "Internal error. Please try again later."
}
```

---

**Built for music lovers who want to discover their next favorite song.**

[View Website](https://redditjams.com)

[Licence](/licence)

[About The Creater](https://www.haidercodes.com)