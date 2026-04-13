"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    print(f"{'Rank':<5} {'Title':<25} {'Score':<8} Reasons")
    print("-" * 70)
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{i:<5} {song['title']:<25} {score:<8.2f} {explanation}")


if __name__ == "__main__":
    main()
