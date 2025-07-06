<<<<<<< HEAD
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle
import requests

app = Flask(__name__)

df = pd.read_csv("songs.csv")
x_scaled = np.load("x_scaled.npy")
model = pickle.load(open("knn_model.pkl", "rb"))

SPOTIFY_CLIENT_ID = "Enter your client id"
SPOTIFY_CLIENT_SECRET = "Enter your client secret"

def get_spotify_token():
    auth_url = "https://accounts.spotify.com/api/token"
    res = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    })
    return res.json().get("access_token")

def get_spotify_data(track_name, artist=""):
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    query = f"{track_name} {artist}".strip().replace(" ", "%20")
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None, None

    items = response.json().get("tracks", {}).get("items", [])
    if items:
        track = items[0]
        cover = track['album']['images'][0]['url'] if track['album']['images'] else None
        preview = track['preview_url']
        return cover, preview
    return None, None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_song = request.form.get('song', '').strip()
    print("🎵 Received song input:", selected_song)

    if not selected_song:
        return render_template("recommend.html", recommendations=[], song="(empty)")

    try:
        idx = df[df['track_name'].str.lower() == selected_song.lower()].index[0]
    except IndexError:
        return render_template("recommend.html", recommendations=[], song=selected_song)

    distances, indices = model.kneighbors([x_scaled[idx]])
    recs = df.iloc[indices[0][1:11]]

    recommendations = []
    for _, row in recs.iterrows():
        name = row['track_name']
        artist = row['artists'] if 'artists' in row else ""
        cover_url, preview_url = get_spotify_data(name, artist)
        recommendations.append({
            "track_name": name,
            "cover_url": cover_url or "https://via.placeholder.com/100",
            "preview_url": preview_url
        })

    return render_template("recommend.html", recommendations=recommendations, song=selected_song)

if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle
import requests

app = Flask(__name__)

df = pd.read_csv("songs.csv")
x_scaled = np.load("x_scaled.npy")
model = pickle.load(open("knn_model.pkl", "rb"))

SPOTIFY_CLIENT_ID = "4c12216d3caa4d34924fcd927e75bb17"
SPOTIFY_CLIENT_SECRET = "109b406dc24d4b72afcde81c9ebe7032"

def get_spotify_token():
    auth_url = "https://accounts.spotify.com/api/token"
    res = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    })
    return res.json().get("access_token")

def get_spotify_data(track_name, artist=""):
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    query = f"{track_name} {artist}".strip().replace(" ", "%20")
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None, None

    items = response.json().get("tracks", {}).get("items", [])
    if items:
        track = items[0]
        cover = track['album']['images'][0]['url'] if track['album']['images'] else None
        preview = track['preview_url']
        return cover, preview
    return None, None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_song = request.form.get('song', '').strip()
    print("🎵 Received song input:", selected_song)

    if not selected_song:
        return render_template("recommend.html", recommendations=[], song="(empty)")

    try:
        idx = df[df['track_name'].str.lower() == selected_song.lower()].index[0]
    except IndexError:
        return render_template("recommend.html", recommendations=[], song=selected_song)

    distances, indices = model.kneighbors([x_scaled[idx]])
    recs = df.iloc[indices[0][1:11]]

    recommendations = []
    for _, row in recs.iterrows():
        name = row['track_name']
        artist = row['artists'] if 'artists' in row else ""
        cover_url, preview_url = get_spotify_data(name, artist)
        recommendations.append({
            "track_name": name,
            "cover_url": cover_url or "https://via.placeholder.com/100",
            "preview_url": preview_url
        })

    return render_template("recommend.html", recommendations=recommendations, song=selected_song)

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> a26163d (updting)
