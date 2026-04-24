import json
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

FILE_PATH = "learning_data.json"

with open(FILE_PATH, "r") as f:
    data = json.load(f)

# Use only valid actual data
filtered = [d for d in data if d["actual"] is not None and d.get("text")]

if len(filtered) < 5:
    print("Not enough data to retrain")
    exit()

df = pd.DataFrame(filtered)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])
y = df["actual"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model retrained using real Jira data")