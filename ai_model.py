import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)


def predict_story_points(text: str):
    try:
        X = vectorizer.transform([text])

        prediction = model.predict(X)[0]

        probabilities = model.predict_proba(X)[0]
        confidence = round(np.max(probabilities) * 100, 2)

        return {
            "ai_points": int(prediction),
            "confidence": confidence
        }

    except Exception as e:
        print("AI Error:", str(e))
        return {
            "ai_points": 3,
            "confidence": 50
        }