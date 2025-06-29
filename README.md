# 🎶 Music Recommendation System using Spotify API & KNN

This project is a **smart, content-based music recommendation system** that leverages **machine learning (KNN)** and **Spotify’s Web API** to recommend songs similar to a user-selected track and also download cover real time. It suggests similar songs based on **audio features** and **engineered traits**, while dynamically fetching real-time **album covers and metadata** from Spotify.

Although Spotify doesn’t allow direct audio playback via API, the system provides highly accurate recommendations and a visually rich experience with cover art, artist names, and genres. 🎨🎧

---

---

## 🚀 Key Features

- 🧠 **ML-Powered Music Recommender** using K-Nearest Neighbors (KNN)
- 📈 Complete **EDA & Feature Engineering** pipeline
- 🎼 **Real-time album cover fetching** via Spotify Web API
- 🎧 Uses **preprocessed music dataset** with rich audio features
- 📦 Web interface powered by Flask with HTML templates
- ❌ No playback – **Spotify playback is restricted via API**
- 🗂️ Responsive results UI built with **`index.html`** and **`recommended.html`**

---

## 📊 How It Works – End-to-End Workflow

### 🧹 Step 1: Data Collection & Cleaning

- A fixed CSV dataset containing songs with Spotify audio features is used.
- Features include:
  - `danceability`, `energy`, `acousticness`, `valence`, `tempo`, `loudness`, `instrumentalness`, etc.

### 🧪 Step 2: EDA (Exploratory Data Analysis)

- Visualize genre distributions, feature correlations, and tempo ranges.
- Identify outliers, missing values, and scale inconsistencies.

### 🧬 Step 3: Feature Engineering

- Create custom features:
  - **Mood Score** = `valence * energy`
  - **Tempo Clusters** – bucket songs into rhythmic categories
  - **Z-score scaling** or **StandardScaler** used for normalization

### 🧠 Step 4: Model Training

- Train a **KNN model** (`scikit-learn`) on scaled numerical features
- Model learns to identify "neighborhoods" of similar songs

### 🎯 Step 5: Prediction

- On input (song name), we:
  - Search the song in the dataset
  - Extract its feature vector
  - Use **KNN** to find `n` closest songs in feature space

### 🎨 Step 6: Spotify API Integration

- Use the `spotipy` library to:
  - Search for tracks by name and artist
  - Fetch:
    - Track ID
    - Artist name
    - Album name
    - **Album cover image (live!)**

> 📌 **Playback Note**: Spotify does not allow playing full or preview audio via the Web API without using embedded players or SDKs.

---

## 🛠️ Tech Stack

| Layer          | Technology                    |
|----------------|-------------------------------|
| Machine Learning | `scikit-learn` (KNN)         |
| Data Handling   | `pandas`, `numpy`             |
| Web API         | `spotipy` (Spotify API client)|
| Backend Server  | `Flask` or `Streamlit`        |
| Data Viz (EDA)  | `matplotlib`, `seaborn`       |
| Frontend        | `HTML`, `Jinja2`, Flask `templates/` |

---


