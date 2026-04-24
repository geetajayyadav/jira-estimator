import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Sample training data (you can expand later)
data = [
    ("simple ui change button fix", 1),
    ("fix small bug in api", 2),
    ("add login api integration", 5),
    ("database migration and api integration", 8),
    ("security patch critical issue", 13),
    ("full system redesign with integration", 21),
]

df = pd.DataFrame(data, columns=["text", "points"])

# Vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])

# Model (REAL AI)
model = RandomForestClassifier(n_estimators=100)

model.fit(X, df["points"])

# Save model
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model trained successfully")