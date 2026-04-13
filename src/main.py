"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs
from tabulate import tabulate


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nTop recommendations for: {user_prefs['favorite_genre']} / {user_prefs['favorite_mood']} / energy {user_prefs['target_energy']}\n")

    for mode in ["genre-first", "mood-first", "energy-focused"]:
        recommendations = recommend_songs(user_prefs, songs, k=5, mode=mode)
        print(f"\nMode: {mode.upper()}\n")
        table = []
        for i, (song, score, explanation) in enumerate(recommendations, 1):
            table.append([i, song['title'], song['artist'], f"{score:.2f}", explanation])
        print(tabulate(
            table,
            headers=["Rank", "Title", "Artist", "Score", "Reasons"],
            tablefmt="rounded_outline"
        ))


if __name__ == "__main__":
    main()
