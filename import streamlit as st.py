import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import base64
from PIL import Image
import io
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
from urllib.parse import quote

# Page configuration
st.set_page_config(
    page_title="🎵 Spotify Galaxy",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Spotify API credentials (you'll need to get these from Spotify Developer Dashboard)
SPOTIFY_CLIENT_ID = "4c12216d3caa4d34924fcd927e75bb17"
SPOTIFY_CLIENT_SECRET = "109b406dc24d4b72afcde81c9ebe7032"

# Custom CSS for GTA 6-like styling with enhanced interactivity
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@300;400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 20%, #16213e 40%, #0f3460 60%, #533483 80%, #7209b7 100%);
        animation: galaxyFlow 15s ease infinite;
        position: relative;
        overflow-x: hidden;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at 20% 80%, rgba(120, 9, 183, 0.3) 0%, transparent 50%), 
                    radial-gradient(circle at 80% 20%, rgba(0, 255, 255, 0.2) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes galaxyFlow {
        0%, 100% { 
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 20%, #16213e 40%, #0f3460 60%, #533483 80%, #7209b7 100%);
        }
        33% { 
            background: linear-gradient(135deg, #7209b7 0%, #533483 20%, #0f3460 40%, #16213e 60%, #1a1a2e 80%, #0a0a0a 100%);
        }
        66% { 
            background: linear-gradient(135deg, #0f3460 0%, #16213e 20%, #1a1a2e 40%, #7209b7 60%, #533483 80%, #0a0a0a 100%);
        }
    }
    
    .main-container {
        position: relative;
        z-index: 1;
    }
    
    .cyber-header {
        font-family: 'Orbitron', monospace;
        font-size: 5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00ffff, #ff006e, #8338ec, #3a86ff);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientText 3s ease infinite, textGlow 2s ease-in-out infinite alternate;
        margin: 2rem 0;
        position: relative;
    }
    
    .cyber-header::after {
        content: '🎵 SPOTIFY GALAXY 🌌';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.1), transparent);
        -webkit-background-clip: text;
        animation: scanline 4s linear infinite;
        z-index: -1;
    }
    
    @keyframes gradientText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes textGlow {
        from { filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.5)); }
        to { filter: drop-shadow(0 0 40px rgba(255, 0, 110, 0.8)); }
    }
    
    @keyframes scanline {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .control-matrix {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(20px);
        border: 2px solid transparent;
        background-clip: padding-box;
        border-radius: 25px;
        padding: 30px;
        margin: 20px 0;
        position: relative;
        box-shadow: 0 20px 60px rgba(0, 255, 255, 0.1);
    }
    
    .control-matrix::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #00ffff, #ff006e, #8338ec, #00ffff);
        border-radius: 25px;
        z-index: -1;
        animation: borderGlow 3s linear infinite;
    }
    
    @keyframes borderGlow {
        0%, 100% { background: linear-gradient(45deg, #00ffff, #ff006e, #8338ec, #00ffff); }
        50% { background: linear-gradient(45deg, #8338ec, #00ffff, #ff006e, #8338ec); }
    }
    
    .album-poster {
        position: relative;
        border-radius: 20px;
        overflow: hidden;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        background: linear-gradient(45deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 110, 0.1));
    }
    
    .album-poster::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.2), transparent);
        opacity: 0;
        transition: all 0.3s ease;
        z-index: 2;
    }
    
    .album-poster:hover {
        transform: translateY(-20px) rotateX(5deg) rotateY(5deg) scale(1.05);
        box-shadow: 0 30px 70px rgba(0, 255, 255, 0.4);
    }
    
    .album-poster:hover::before {
        opacity: 1;
        animation: posterScan 1s ease-in-out;
    }
    
    @keyframes posterScan {
        0% { transform: translateX(-100%) skewX(-15deg); }
        100% { transform: translateX(100%) skewX(-15deg); }
    }
    
    .play-overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0);
        width: 80px;
        height: 80px;
        background: linear-gradient(45deg, #ff006e, #8338ec);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        color: white;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        z-index: 3;
        box-shadow: 0 10px 30px rgba(255, 0, 110, 0.5);
    }
    
    .album-poster:hover .play-overlay {
        transform: translate(-50%, -50%) scale(1);
        animation: playPulse 2s ease-in-out infinite;
    }
    
    @keyframes playPulse {
        0%, 100% { box-shadow: 0 10px 30px rgba(255, 0, 110, 0.5); }
        50% { box-shadow: 0 20px 50px rgba(255, 0, 110, 0.8); }
    }
    
    .track-card {
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .track-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .track-card:hover {
        transform: translateY(-10px);
        border-color: #00ffff;
        box-shadow: 0 25px 50px rgba(0, 255, 255, 0.3);
    }
    
    .track-card:hover::before {
        left: 100%;
    }
    
    .cyber-button {
        background: linear-gradient(45deg, #00ffff, #ff006e);
        border: none;
        border-radius: 25px;
        padding: 15px 35px;
        font-family: 'Orbitron', monospace;
        font-weight: bold;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .cyber-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .cyber-button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.5);
    }
    
    .cyber-button:hover::before {
        left: 100%;
    }
    
    .search-interface {
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 50px;
        padding: 15px 25px;
        color: white;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .search-interface:focus {
        outline: none;
        border-color: #00ffff;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    .search-interface::placeholder {
        color: rgba(255, 255, 255, 0.5);
    }
    
    .audio-visualizer {
        width: 100%;
        height: 60px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        padding: 10px;
        margin: 15px 0;
        gap: 3px;
    }
    
    .visualizer-bar {
        width: 4px;
        background: linear-gradient(to top, #ff006e, #00ffff);
        border-radius: 2px;
        animation: audioWave 1.5s ease-in-out infinite;
        animation-delay: var(--delay);
    }
    
    @keyframes audioWave {
        0%, 100% { height: 5px; }
        50% { height: var(--height); }
    }
    
    .now-playing {
        background: linear-gradient(45deg, rgba(255, 0, 110, 0.2), rgba(0, 255, 255, 0.2));
        border: 1px solid rgba(0, 255, 255, 0.5);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        animation: playingGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes playingGlow {
        from { box-shadow: 0 5px 20px rgba(0, 255, 255, 0.3); }
        to { box-shadow: 0 10px 40px rgba(255, 0, 110, 0.5); }
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    .metric-orb {
        background: radial-gradient(circle, rgba(0, 255, 255, 0.2), rgba(255, 0, 110, 0.1));
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .metric-orb:hover {
        transform: scale(1.1);
        border-color: #00ffff;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
    }
    
    .loading-portal {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        flex-direction: column;
    }
    
    .portal-ring {
        width: 100px;
        height: 100px;
        border: 3px solid transparent;
        border-top: 3px solid #00ffff;
        border-right: 3px solid #ff006e;
        border-radius: 50%;
        animation: portalSpin 1s linear infinite;
        position: relative;
    }
    
    .portal-ring::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        border: 3px solid transparent;
        border-bottom: 3px solid #8338ec;
        border-left: 3px solid #3a86ff;
        border-radius: 50%;
        animation: portalSpin 1.5s linear infinite reverse;
    }
    
    @keyframes portalSpin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .status-hud {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        padding: 15px;
        z-index: 1000;
        color: white;
        font-family: 'Orbitron', monospace;
        min-width: 200px;
    }
    
    .sidebar .stSelectbox label,
    .sidebar .stTextInput label {
        color: #00ffff !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'knn_model' not in st.session_state:
    st.session_state.knn_model = None
if 'X_scaled' not in st.session_state:
    st.session_state.X_scaled = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'spotify_client' not in st.session_state:
    st.session_state.spotify_client = None
if 'current_playing' not in st.session_state:
    st.session_state.current_playing = None

@st.cache_data
def load_dataset():
    """Load the Spotify dataset"""
    try:
        df = pd.read_csv("spotify_tracks.csv")
        return df
    except FileNotFoundError:
        st.error("❌ spotify_tracks.csv not found! Please make sure the file is in the same directory.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")
        return None

@st.cache_resource
def load_models():
    """Load the pre-trained KNN model and scaled features"""
    try:
        # Load the KNN model
        with open('knn_model.pkl', 'rb') as f:
            knn_model = pickle.load(f)
        
        # Load the scaled features
        X_scaled = np.load('x_scaled.npy')
        
        return knn_model, X_scaled
    except FileNotFoundError as e:
        st.error(f"❌ Model files not found: {str(e)}")
        st.error("Please make sure 'knn_model.pkl' and 'x_scaled.npy' are in the same directory.")
        return None, None
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        return None, None

def initialize_spotify_client():
    """Initialize Spotify client"""
    try:
        if SPOTIFY_CLIENT_ID != "your_client_id_here" and SPOTIFY_CLIENT_SECRET != "your_client_secret_here":
            client_credentials_manager = SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            )
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            return sp
        else:
            st.warning("⚠️ Spotify API credentials not configured. Using placeholder images.")
            return None
    except Exception as e:
        st.warning(f"⚠️ Spotify API error: {str(e)}. Using placeholder images.")
        return None

def get_album_cover_and_preview(track_name, artist_name, spotify_client):
    """Get album cover and preview URL from Spotify"""
    if not spotify_client:
        return generate_placeholder_cover(), None
    
    try:
        query = f"track:{track_name} artist:{artist_name}"
        results = spotify_client.search(q=query, type='track', limit=1)
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            
            # Get album cover
            album_cover_url = None
            if track['album']['images']:
                album_cover_url = track['album']['images'][0]['url']
            
            # Get preview URL
            preview_url = track.get('preview_url')
            
            return album_cover_url, preview_url
        else:
            return generate_placeholder_cover(), None
            
    except Exception as e:
        st.warning(f"Spotify API error for {track_name}: {str(e)}")
        return generate_placeholder_cover(), None

def generate_placeholder_cover():
    """Generate a futuristic placeholder album cover"""
    # Create a gradient placeholder with cyber aesthetics
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    
    # Create gradient
    for i in range(300):
        for j in range(300):
            # Create a radial gradient with neon colors
            center_x, center_y = 150, 150
            distance = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            
            # Normalize distance
            distance = min(distance / 150, 1.0)
            
            # Neon gradient
            r = int(255 * (1 - distance) * 0.8)
            g = int(255 * distance * 0.6)
            b = int(255 * (0.5 + 0.5 * np.sin(distance * 10)))
            
            img[i, j] = [r, g, b]
    
    return Image.fromarray(img)

def create_audio_visualizer():
    """Create an animated audio visualizer"""
    bars_html = ""
    for i in range(20):
        height = np.random.randint(10, 40)
        delay = i * 0.1
        bars_html += f'<div class="visualizer-bar" style="--height: {height}px; --delay: {delay}s;"></div>'
    
    return f'<div class="audio-visualizer">{bars_html}</div>'

def get_song_recommendations(song_name, df, knn_model, X_scaled):
    """Get song recommendations using the loaded model"""
    try:
        # Find the song in the dataset
        song_matches = df[df['track_name'].str.lower().str.contains(song_name.lower(), na=False)]
        
        if song_matches.empty:
            return None, "🔍 Song not found in our galaxy database. Try a different search term!"
        
        song_index = song_matches.index[0]
        song_vector = X_scaled[song_index].reshape(1, -1)
        distances, indices = knn_model.kneighbors(song_vector)
        
        recommendations = []
        for idx in indices[0][1:]:  # Skip the first one (same song)
            rec_song = df.iloc[idx]
            recommendations.append({
                'track_name': rec_song['track_name'],
                'artists': rec_song['artists'],
                'album_name': rec_song.get('album_name', 'Unknown Album'),
                'track_genre': rec_song.get('track_genre', 'Unknown'),
                'popularity': rec_song.get('popularity', 0),
                'danceability': rec_song.get('danceability', 0),
                'energy': rec_song.get('energy', 0),
                'valence': rec_song.get('valence', 0),
                'acousticness': rec_song.get('acousticness', 0),
                'instrumentalness': rec_song.get('instrumentalness', 0)
            })
        
        return recommendations, None
        
    except Exception as e:
        return None, f"❌ Error getting recommendations: {str(e)}"

def play_preview(track_name, preview_url):
    """Handle music preview playback"""
    if preview_url:
        # Open the preview URL (30-second clip)
        webbrowser.open(preview_url)
        st.session_state.current_playing = track_name
        return True
    else:
        st.warning(f"🎵 No preview available for '{track_name}' - this is common for some tracks on Spotify.")
        return False

def main():
    # Status HUD
    st.markdown(f"""
    <div class="status-hud">
        <div style="font-size: 0.9rem; margin-bottom: 10px;">🌌 GALAXY STATUS</div>
        <div style="font-size: 0.8rem;">
            {'🟢 MODELS LOADED' if st.session_state.model_loaded else '🔴 MODELS OFFLINE'}<br>
            {'🟢 SPOTIFY CONNECTED' if st.session_state.spotify_client else '🟡 SPOTIFY LIMITED'}<br>
            {'🎵 NOW PLAYING: ' + st.session_state.current_playing if st.session_state.current_playing else '⏸️ NO TRACK PLAYING'}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main header with enhanced styling
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="cyber-header">🎵 SPOTIFY GALAXY 🌌</h1>', unsafe_allow_html=True)
    
    # Control Matrix
    with st.container():
        st.markdown('<div class="control-matrix">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🚀 MISSION CONTROL")
            
            if st.button("🔮 INITIALIZE GALAXY ENGINE", key="init_btn"):
                with st.spinner("🌌 Loading models from the digital realm..."):
                    progress_bar = st.progress(0)
                    
                    # Load dataset
                    progress_bar.progress(25)
                    df = load_dataset()
                    
                    if df is not None:
                        st.session_state.df = df
                        
                        # Load models
                        progress_bar.progress(50)
                        knn_model, X_scaled = load_models()
                        
                        if knn_model is not None and X_scaled is not None:
                            st.session_state.knn_model = knn_model
                            st.session_state.X_scaled = X_scaled
                            
                            # Initialize Spotify
                            progress_bar.progress(75)
                            spotify_client = initialize_spotify_client()
                            st.session_state.spotify_client = spotify_client
                            
                            progress_bar.progress(100)
                            st.session_state.model_loaded = True
                            
                            st.success("🎉 GALAXY ENGINE ONLINE! Ready for musical exploration!")
                            st.balloons()
                        
                    progress_bar.empty()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main Application Interface
    if not st.session_state.model_loaded:
        # Welcome Portal
        st.markdown("""
        <div style="text-align: center; padding: 100px 20px;">
            <div class="loading-portal">
                <div class="portal-ring"></div>
                <h2 style="color: #00ffff; font-family: 'Orbitron', monospace; margin-top: 30px;">
                    WELCOME TO THE MUSIC MULTIVERSE
                </h2>
                <p style="color: rgba(255, 255, 255, 0.8); font-size: 1.2rem; margin-top: 20px; font-family: 'Rajdhani', sans-serif;">
                    🌟 AI-Powered Cosmic Recommendations<br>
                    🎨 Interactive Holographic Album Covers<br>
                    🎵 Instant 30-Second Previews<br>
                    🌌 Immersive Galactic Experience<br>
                    🚀 Real Spotify Integration
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Search Interface
        st.markdown("### 🔍 COSMIC MUSIC DISCOVERY")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "Search the music galaxy:",
                placeholder="Enter a song name to discover similar cosmic vibes...",
                key="search_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_btn = st.button("🎯 SCAN GALAXY", key="search_btn")
        
        # Process search
        if (search_btn or search_query) and search_query:
            with st.spinner("🌌 Scanning the cosmic frequencies..."):
                recommendations, error = get_song_recommendations(
                    search_query,
                    st.session_state.df,
                    st.session_state.knn_model,
                    st.session_state.X_scaled
                )
                
                if error:
                    st.error(error)
                else:
                    st.session_state.recommendations = recommendations
                    st.success(f"🎵 Discovered {len(recommendations)} cosmic harmonies!")
        
        # Display Recommendations
        if 'recommendations' in st.session_state and st.session_state.recommendations:
            st.markdown("### 🌟 COSMIC RECOMMENDATIONS")
            
            # Create grid layout for album posters
            cols = st.columns(3)
            
            for i, song in enumerate(st.session_state.recommendations):
                col_idx = i % 3
                
                with cols[col_idx]:
                    # Get album cover and preview
                    album_cover, preview_url = get_album_cover_and_preview(
                        song['track_name'],
                        song['artists'],
                        st.session_state.spotify_client
                    )