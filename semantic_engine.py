import json
import os
from sklearn.metrics.pairwise import cosine_similarity
import joblib

DATA_FILE = "learning_data.json"

# Load vectorizer (same as AI model)
vectorizer = joblib.load("vectorizer.pkl")


def semantic_estimate(text):
    try:
        if not os.path.exists(DATA_FILE):
            return None

        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        if not data:
            return None

        texts = [d.get("issue", "") for d in data]
        points = [d.get("actual") for d in data]

        # Remove None values
        valid_data = [(t, p) for t, p in zip(texts, points) if p is not None]

        if not valid_data:
            return None

        texts, points = zip(*valid_data)

        X = vectorizer.transform(texts)
        input_vec = vectorizer.transform([text])

        similarities = cosine_similarity(input_vec, X)[0]

        best_index = similarities.argmax()
        best_score = similarities[best_index]

        # Threshold (important)
        if best_score < 0.3:
            return None

        return {
            "semantic_points": int(points[best_index]),
            "similarity": round(float(best_score), 2)
        }

    except Exception as e:
        print("Semantic Error:", e)
        return None