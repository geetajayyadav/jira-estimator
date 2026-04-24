import json
import os

FILE_PATH = "learning_data.json"


def save_estimation(issue_key, predicted, actual, text=None):
    data = []

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []

    difference = None
    if actual is not None:
        difference = actual - predicted

    data.append({
        "issue": issue_key,
        "predicted": predicted,
        "actual": actual,
        "difference": difference,
        "text": text
    })

    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def get_learning_data():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r") as f:
        try:
            return json.load(f)
        except:
            return []