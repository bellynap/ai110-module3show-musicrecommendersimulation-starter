from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and returns a list of dictionaries with correct types."""
    import csv
    songs = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences and returns a score and list of reasons."""
    score = 0.0
    reasons = []

    if song['genre'] == user_prefs['favorite_genre']:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song['mood'] == user_prefs['favorite_mood']:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_score = 1 - abs(song['energy'] - user_prefs['target_energy'])
    score += energy_score
    reasons.append(f"energy proximity (+{energy_score:.2f})")

    return (score, reasons)

def apply_diversity_penalty(scored: List[Tuple[Dict, float, str]], penalty: float = 0.5) -> List[Tuple[Dict, float, str]]:
    """Applies a penalty to songs whose artist or genre already appears in the top results."""
    seen_artists = set()
    seen_genres = set()
    reranked = []

    for song, score, explanation in scored:
        artist = song['artist']
        genre = song['genre']
        new_score = score

        if artist in seen_artists:
            new_score -= penalty
            explanation += f", diversity penalty (-{penalty})"
        if genre in seen_genres:
            new_score -= penalty
            explanation += f", genre diversity penalty (-{penalty})"

        seen_artists.add(artist)
        seen_genres.add(genre)
        reranked.append((song, new_score, explanation))

    return sorted(reranked, key=lambda x: x[1], reverse=True)

def score_song_with_mode(user_prefs: Dict, song: Dict, mode: str = "genre-first") -> Tuple[float, List[str]]:
    """Scores a song using a specified ranking strategy/mode."""
    score = 0.0
    reasons = []

    if mode == "genre-first":
        genre_weight, mood_weight, energy_weight = 2.0, 1.0, 1.0
    elif mode == "mood-first":
        genre_weight, mood_weight, energy_weight = 1.0, 2.0, 1.0
    elif mode == "energy-focused":
        genre_weight, mood_weight, energy_weight = 0.5, 0.5, 3.0
    else:
        genre_weight, mood_weight, energy_weight = 2.0, 1.0, 1.0

    if song['genre'] == user_prefs['favorite_genre']:
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight})")

    if song['mood'] == user_prefs['favorite_mood']:
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight})")

    energy_score = (1 - abs(song['energy'] - user_prefs['target_energy'])) * energy_weight
    score += energy_score
    reasons.append(f"energy proximity (+{energy_score:.2f})")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "genre-first") -> List[Tuple[Dict, float, str]]:
    """Scores all songs using the specified mode, applies diversity penalty, and returns top k."""
    scored = []
    for song in songs:
        score, reasons = score_song_with_mode(user_prefs, song, mode)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    scored = apply_diversity_penalty(scored)
    return scored[:k]
