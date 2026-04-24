import requests
import os
from dotenv import load_dotenv

load_dotenv()

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


# 🔹 Get Jira issue basic details
def get_jira_issue(issue_key):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"

    response = requests.get(url, headers=HEADERS, auth=AUTH)

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()

    return {
        "summary": data["fields"]["summary"],
        "description": str(data["fields"].get("description", "")),
        "actual_story_points": data["fields"].get("customfield_10016"),
        "priority": data["fields"].get("priority", {}).get("name", "Medium"),
        "issue_type": data["fields"].get("issuetype", {}).get("name", "Story")
    }


# 🔹 Update story points in Jira
def update_story_points(issue_key, points):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"

    payload = {
        "fields": {
            "customfield_10016": points
        }
    }

    response = requests.put(url, json=payload, headers=HEADERS, auth=AUTH)

    if response.status_code == 204:
        return {"message": "Story points updated ✅"}

    return {"error": response.text}
