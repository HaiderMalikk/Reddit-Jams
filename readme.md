![alt text](assets/logowtext.svg)

# RedditJams - Music Recommendation APP

**RedditJams** is an intelligent music recommendation system that analyzes your Spotify playlist, searches Reddit's music community for similar tastes, and uses GPT-4 to generate personalized song recommendations.

---

## What It Does

Simply provide a **Spotify playlist URL**, and RedditJams will:

1. **Analyze your playlist** - Extracts diverse tracks and artists (top, bottom, and random) for broader coverage
2. **Search Reddit** - Finds music recommendation posts/threads from r/music community
3. **AI Analysis** - Uses GPT-4 to analyze both your taste and Reddit recommendations
4. **Return Results** - Delivers 5 personalized song recommendations with Spotify links

---

## How to Use the API

### API Endpoint

```
POST https://reddit-jams-backend.vercel.app/api/recommendations
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
curl -X POST https://reddit-jams-backend.vercel.app/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"playlist_url": "https://open.spotify.com/playlist/3XyDvjoxiae0oWpfJ4kga9"}'
```

---

## API Response

The API returns a JSON object with your personalized recommendations:

```json
{
  "success": true,
  "playlist_details": {
    "name": "Summer Nights",
    "owner": "Malik",
    "total_tracks": 68,
    "album_art": "https://image-cdn-ak.spotifycdn.com/image/ab67706c0000da848f15c90b02dadc6c6c154bb4"
  },
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
- Selects **9 diverse tracks** for analysis (configurable):
  - **Top 3** most popular tracks (NUM_TOP_TRACKS = 3)
  - **Bottom 3** least popular tracks (NUM_BOTTOM_TRACKS = 3)
  - **3 random** tracks from the middle range (NUM_RANDOM_TRACKS = 3)
- Selects **6 diverse artists** for analysis (configurable):
  - **Top 2** artists from your playlist (NUM_TOP_ARTISTS = 2)
  - **Bottom 2** artists from your playlist (NUM_BOTTOM_ARTISTS = 2)
  - **2 random** artists from the middle range (NUM_RANDOM_ARTISTS = 2)

#### **Step 2: Reddit Community Search (Parallel)**
The system searches Reddit's r/music community in parallel for similar music tastes:

**Track-Based Searches (9 parallel queries):**
- For each of your 9 diverse tracks, searches Reddit for: `"[track name] [artist] recommend"`
- Example: `"Running Up That Hill Kate Bush recommend"`
- Finds posts where users recommend songs similar to your selections
- Includes top hits, hidden gems, and random discoveries from your playlist

**Artist-Based Searches (6 parallel queries):**
- For each of your 6 diverse artists, searches Reddit for: `"[artist name] recommend similar"`
- Example: `"Kate Bush recommend similar"`
- Finds posts recommending artists/songs similar to your selections
- Covers well-known and lesser-known artists from your library

**Total: 15 simultaneous Reddit searches** - All executed in parallel for maximum speed and diversity

**Keyword Filtering:**
Only keeps posts/comments containing recommendation keywords:
- "recommend"
- "similar to"
- "if you like"
- "check out"
- "you might like"
- "fans of"
- "try"

> [!NOTE]
> **Why r/music?**

r/music is the optimal subreddit for music recommendations for several key reasons:

- **Unmatched Scale:** With over 32 million members, r/music is Reddit's largest music community by far. The next largest music subreddits (like r/listentothis at ~17M or r/hiphopheads at ~2.8M) are significantly smaller.

- **Genre Diversity:** Unlike specialized subreddits (r/metal, r/indieheads, r/jazz, r/edm, etc.) that focus on specific genres, r/music covers all music types in one place. This means:
  - A playlist mixing pop, rock, and electronic gets comprehensive recommendations
  - No need to query 10+ genre-specific subreddits separately
  - Avoids the complexity of analyzing user taste to determine which subreddits to search

- **High Engagement:** r/music has thousands of active daily discussions with genuine music discovery conversations, ensuring fresh recommendations across all genres.

- **Efficient Processing:** Searching one large, diverse subreddit is faster and simpler than:
  - Analyzing playlist genres → mapping to multiple subreddits → parallel searches across 5-10 communities
  - Managing different community rules, post formats, and recommendation patterns
  - Aggregating and deduplicating results from fragmented sources

By using r/music, we guarantee broad coverage of all music tastes while maintaining fast, reliable API performance.

#### **Step 3: AI-Powered Analysis**
- Sends your playlist data + Reddit recommendations to **GPT-4**
- GPT-4 analyzes patterns in your music taste
- Considers community recommendations from Reddit
- Generates **5 new song suggestions** (not in your original playlist) in order from most to least recomended
- Returns songs as JSON: `[{"song": "Title", "artist": "Artist"}, ...]`

#### **Step 4: Spotify Verification**
- Searches Spotify for each GPT-4 recommendation
- Retrieves full track details (album art, preview URLs, popularity, etc.)
- Ensures all recommendations are real, playable songs
- Returns complete track information with direct Spotify links

#### **Step 5: Results Delivery**
- Returns formatted JSON response with all recommendations
- Includes metadata about the recommendation process and the users playlist
- Ready to display in the application

---

## Configuration

The API uses the following default configuration:

| Parameter | Default | Description |
|-----------|---------|-------------|
| Subreddit | `music` | Reddit community to search |
| Reddit Posts Per Query | 20 | Max posts to fetch per search |
| Comments Per Post | 30 | Max comments to analyze per post |
| Top Tracks | 3 | Number of most popular tracks to analyze |
| Bottom Tracks | 3 | Number of least popular tracks to analyze |
| Random Tracks | 3 | Number of random tracks to analyze (total = 9) |
| Top Artists | 2 | Number of top artists to analyze |
| Bottom Artists | 2 | Number of bottom artists to analyze |
| Random Artists | 2 | Number of random artists to analyze (total = 6) |
| Recommendations | 5 | Number of songs to recommend |
| GPT Model | `gpt-4o-mini` | AI model for analysis |
| GPT Temperature | 0.7 | Creativity level (0-1) |

---

## Why It Works

**Community Intelligence:** Reddit's music community shares authentic recommendations based on real listening experiences, not just algorithmic similarities.

**Diverse Selection:** Analyzes top hits, hidden gems, and random discoveries from your playlist, ensuring recommendations aren't biased toward only your most popular tracks.

**Multi-Source Analysis:** Combines your actual playlist data with community wisdom, providing recommendations that are both personalized AND discovery-oriented.

**AI Understanding:** GPT-4 understands music context, genres, moods, and can identify nuanced patterns that simple collaborative filtering misses.

**Parallel Processing:** All 15 Reddit searches run simultaneously using async/await, making the API fast despite searching multiple queries.

**Real Spotify Integration:** Every recommendation is verified on Spotify with full metadata, ensuring you can instantly play any suggested song.

---

## Additional Endpoints

### Health Check
```bash
GET https://reddit-jams-backend.vercel.app/api/health
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
GET https://reddit-jams-backend.vercel.app/docs
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
2. Selects 9 diverse tracks (top 3, bottom 3, random 3) for broader coverage
3. Selects 6 diverse artists (top 2, bottom 2, random 2) for varied perspectives
4. Searches Reddit for 15 different recommendation queries in parallel
5. Finds 62+ Reddit posts with music recommendations
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