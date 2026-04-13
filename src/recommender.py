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
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    print(f"Loading songs from {csv_path}...")
    songs = []
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                if field in row:
                    row[field] = int(row[field])
            for field in float_fields:
                if field in row:
                    row[field] = float(row[field])
            songs.append(row)

    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Scores each song using cosine similarity between the song's numeric feature
    vector and the user's preference vector, then adds categorical boosts:
      +2.0  genre match
      +1.0  mood match
      +1.0  acousticness within ±0.1 of user preference (if provided)
    """
    import math

    # Numeric dimensions used for cosine similarity.
    # Missing user prefs default to 0.5 (midpoint / neutral).
    FEATURES = ["energy", "valence", "danceability", "acousticness"]

    def cosine_similarity(a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        mag_a = math.sqrt(sum(x * x for x in a))
        mag_b = math.sqrt(sum(x * x for x in b))
        if mag_a == 0.0 or mag_b == 0.0:
            return 0.0
        return dot / (mag_a * mag_b)

    user_vec = [float(user_prefs.get(f, 0.5)) for f in FEATURES]

    scored = []
    for song in songs:
        song_vec = [float(song.get(f, 0.5)) for f in FEATURES]

        sim = cosine_similarity(user_vec, song_vec)
        score = sim
        reasons = [f"cosine similarity ({sim:.2f})"]

        if song.get("genre") == user_prefs.get("genre"):
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.get("mood") == user_prefs.get("mood"):
            score += 1.0
            reasons.append("mood match (+1.0)")

        user_acousticness = user_prefs.get("acousticness")
        if user_acousticness is not None:
            if abs(float(song.get("acousticness", 0.0)) - float(user_acousticness)) <= 0.1:
                score += 1.0
                reasons.append("acousticness match (+1.0)")

        scored.append((song, score, ", ".join(reasons)))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
