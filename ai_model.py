import joblib
import numpy as np

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


def predict_story_points(text: str):
    try:
        X = vectorizer.transform([text])

        prediction = model.predict(X)[0]

        # REAL confidence (now works)
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