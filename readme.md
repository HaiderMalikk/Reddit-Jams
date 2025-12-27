# 🎵 Reddit-Powered Song Recommendation System

An AI-powered music recommendation engine that combines **Spotify playlists**, **Reddit community insights**, and **ChatGPT** to generate personalized song recommendations.

**ADD VARS FOR SUBREDDIT SO USER CAN CHANGE AND FOR POSTS FECTHED TO CONTROL TIME TAKEN**

RedditJa

## 🎯 What Makes This Different?

Unlike Spotify's built-in recommendations, this system:

- **Uses Reddit Community Knowledge**: Searches r/music for real user recommendations like "if you like X, try Y"
- **AI-Powered Analysis**: ChatGPT analyzes patterns between your playlist and Reddit discussions
- **No User Login Required**: Uses Spotify's Client Credentials (read-only, no authentication)
- **Focuses on Recommendations, Not Reviews**: Filters for recommendation posts/comments, not general music discussions
- **Returns Full Track Objects**: Get complete Spotify metadata (name, artist, album, cover art, URLs)

## 🚀 How It Works

```
1. Extract Playlist Data from Spotify
   ↓
2. Search Reddit for Recommendations (based on top songs/artists)
   ↓
3. Format Data for ChatGPT
   ↓
4. ChatGPT Analyzes & Generates 5 Recommendations
   ↓
5. Search Spotify for Recommended Tracks
   ↓
6. Return Full Spotify Song Objects
```

### Detailed Pipeline

1. **Spotify Extraction**: Gets all tracks from your playlist (songs, artists, albums, popularity)
2. **Reddit Search**: 
   - Searches for top 5 most popular tracks from playlist
   - Searches for top 3 artists from playlist
   - Filters for posts/comments with keywords: "recommend", "similar", "if you like"
3. **ChatGPT Processing**: Sends playlist + Reddit data to GPT-4 for pattern analysis
4. **Spotify Lookup**: Converts ChatGPT recommendations back to full Spotify track objects
5. **Export & Logging**: Saves all data at each step for debugging and analysis

## 📋 Requirements

### Python Packages
```bash
pip install spotipy praw python-dotenv pandas openai
```

### API Keys Required

You'll need API credentials for:

1. **Spotify** (Client Credentials - no user login)
   - Get from: https://developer.spotify.com/dashboard
   - Create an app → Copy Client ID & Secret

2. **Reddit** (PRAW)
   - Get from: https://www.reddit.com/prefs/apps
   - Create a script app → Copy credentials

3. **OpenAI** (ChatGPT API)
   - Get from: https://platform.openai.com/api-keys
   - Create API key

## ⚙️ Setup

1. **Clone/Download the project**

2. **Create `.env` file** in the project root:

```env
# Spotify API (Client Credentials)
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

# Reddit API
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=your_app_name (by u/your_username)

# OpenAI API
OPENAI_API_KEY=your_openai_api_key
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## 🎮 Usage

### Option 1: Run the Jupyter Notebook

Open `steps.ipynb` and run cells in order:

1. **Cell 1-3**: Install packages and initialize APIs
2. **Cell 4-5**: Configure playlist URL and settings
3. **Cell 6**: Extract playlist data from Spotify
4. **Cell 7**: Search Reddit for recommendations
5. **Cell 8**: Format data for ChatGPT
6. **Cell 9**: Get AI recommendations
7. **Cell 10**: Search Spotify for recommended tracks
8. **Cell 11-13**: Display results and export data

### Configuration Variables

Edit these in the notebook (Cell 5):

```python
PLAYLIST_URL = "https://open.spotify.com/playlist/YOUR_PLAYLIST_ID"
SUBREDDIT_NAME = "music"  # Which subreddit to search
MAX_REDDIT_POSTS_PER_QUERY = 20  # Posts per search
MAX_COMMENTS_PER_POST = 30  # Comments to analyze per post
NUM_RECOMMENDATIONS = 5  # How many songs to recommend
```

## 📊 Output

The system generates:

### 1. Console Output
- Step-by-step progress logs
- Found Reddit posts and comments
- ChatGPT recommendations
- Final Spotify track details

### 2. JSON Logs
- `recommendation_log_TIMESTAMP.json`: Complete pipeline data
- `recommendations_TIMESTAMP.json`: Just the final recommendations

### 3. CSV Export
- `recommendations_TIMESTAMP.csv`: DataFrame of recommendations

### Example Recommendation Output

```
🎵 FINAL SONG RECOMMENDATIONS
================================================================================

1. Song Name
   Artist: Artist Name
   Album: Album Name
   Release: 2023-01-15
   Duration: 3:45
   Popularity: 87/100
   🎧 Listen: https://open.spotify.com/track/...
   🖼️  Album Art: https://i.scdn.co/image/...
   ▶️  Preview: https://p.scdn.co/mp3-preview/...
   URI: spotify:track:...
```

## 🔍 What Gets Searched on Reddit?

- **Top 5 songs** from your playlist (by popularity)
- **Top 3 artists** from your playlist (unique)

Search queries look like:
- `"Song Name Artist Name recommend"`
- `"Artist Name recommend similar"`

Only posts/comments with recommendation keywords are collected:
- "recommend"
- "similar to"
- "if you like"
- "check out"
- "you might like"
- "fans of"

## 📁 Project Structure

```
spotifyredditproject/
├── steps.ipynb              # Main recommendation pipeline
├── spotifyapi.ipynb         # Spotify API exploration/testing
├── redditstructuredtest.ipynb  # Reddit scraping tests
├── reddittest.ipynb         # Additional Reddit tests
├── .env                     # API credentials (not committed)
├── requirements.txt         # Python dependencies
└── readme.md               # This file
```

## 🛠️ Troubleshooting

### "No Reddit recommendations found"
- Try a different subreddit (e.g., "listentothis", "ifyoulikeblank")
- Increase `MAX_REDDIT_POSTS_PER_QUERY`
- Check if your playlist songs are popular enough to have Reddit discussions

### "ChatGPT returned invalid JSON"
- The system will log the raw response for debugging
- Try adjusting the prompt or temperature in Cell 9

### "Spotify track not found"
- ChatGPT might suggest obscure songs not on Spotify
- Check the logs to see what was searched
- The system continues even if some tracks aren't found

## 🎓 Learning Resources

- [Spotify Web API Docs](https://developer.spotify.com/documentation/web-api)
- [PRAW (Reddit API) Docs](https://praw.readthedocs.io/)
- [OpenAI API Docs](https://platform.openai.com/docs)

## ⚠️ Rate Limits & Costs

- **Spotify**: Free tier allows 100 requests per 30 seconds
- **Reddit**: PRAW handles rate limiting automatically
- **OpenAI**: GPT-4 costs ~$0.03 per request (depending on prompt size)

## 🔮 Future Improvements

- [ ] Support for multiple playlists
- [ ] Search multiple subreddits
- [ ] Add audio feature analysis
- [ ] Create Spotify playlist from recommendations
- [ ] Web interface
- [ ] Cache Reddit results to save API calls

## 📝 License

This is a personal project. Feel free to use and modify as needed.

## 🤝 Contributing

This is a learning project! Feel free to fork and experiment.

---

**Made with ❤️ using Spotify, Reddit, and ChatGPT APIs**