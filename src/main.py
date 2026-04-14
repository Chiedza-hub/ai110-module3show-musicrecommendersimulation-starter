"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    profiles = {
        "Pop / Happy":    {"genre": "pop",  "mood": "happy",     "energy": 0.8, "acousticness": 0.2},
        "Lofi / Calm":    {"genre": "lofi", "mood": "calm",      "energy": 0.3, "acousticness": 0.8},
        "RnD / Neutral":  {"genre": "rnd",  "mood": "neutral",   "energy": 0.5, "acousticness": 0.5},
        # --- Tricky / adversarial profiles ---

        # energy=0 and acousticness=0 means those two dimensions contribute nothing to
        # the cosine vector.  valence and danceability silently default to 0.5 inside
        # score_song, so the ranking is driven entirely by those hidden dimensions.
        # Expect dancy, positive songs — not the quiet ones the label implies.
        "Ghost Acoustic (energy=0, acousticness=0)": {
            "genre": "lofi", "mood": "chill", "energy": 0.0, "acousticness": 0.0,
        },

        # The +2.0 genre bonus in score_song dwarfs the maximum cosine similarity of
        # 1.0.  A soft, high-acousticness preference labelled "rock" will still surface
        # Iron Cathedral and Storm Runner at the top because the genre tag overrides
        # every feature signal.
        "Genre Trojan (soft features, rock label)": {
            "genre": "rock", "mood": "peaceful", "energy": 0.2, "acousticness": 0.9,
        },

        # All four cosine features are 0.0 → zero-magnitude vector → cosine similarity
        # returns 0.0 for every song.  Only the +2.0 / +1.0 label bonuses survive,
        # so whichever songs match genre or mood win regardless of their audio features.
        "Zero Vector (all features = 0)": {
            "genre": "jazz", "mood": "groovy", "energy": 0.0, "acousticness": 0.0,
            "valence": 0.0, "danceability": 0.0,
        },

        # valence and danceability are valid keys in score_song but never shown in the
        # normal profiles above.  Adding them shifts the cosine vector and can
        # completely reorder results — a hidden interface most users never discover.
        "Hidden Dimensions (valence + danceability unlocked)": {
            "genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.2,
            "valence": 1.0, "danceability": 1.0,
        },

        # No song in the dataset is simultaneously high-energy AND highly acoustic —
        # those traits are inversely correlated.  The recommender must pick the least
        # wrong match, and the result is unpredictable without inspecting the math.
        "Contradictory (energy=1.0 AND acousticness=1.0)": {
            "genre": "ambient", "mood": "energetic", "energy": 1.0, "acousticness": 1.0,
        },
    }

    for label, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 50)
        print(f"  TOP RECOMMENDATIONS — {label}")
        print("=" * 50)

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{rank}  {song['title']} by {song['artist']}")
            print(f"    Score : {score:.2f}")
            print("    Why   :")
            for reason in explanation.split(", "):
                print(f"            - {reason}")

        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
