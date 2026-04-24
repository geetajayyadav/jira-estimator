from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from jira_client import get_jira_issue, update_story_points
from estimator import estimate_story_points
from learning import save_estimation, get_learning_data

# ✅ USE GROQ (NOT LANGCHAIN)
from llm_reasoner import generate_llm_reasoning

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return {"message": "Jira AI Estimator Running 🚀"}


# Serve UI
@app.get("/ui")
def ui():
    return FileResponse("static/index.html")


# Estimate story points
@app.get("/estimate/{issue_key}")
def estimate(issue_key: str):
    issue = get_jira_issue(issue_key)

    if "error" in issue:
        return issue

    result = estimate_story_points(
    issue["summary"],
    issue["description"],
    issue["priority"]
)

    predicted = result["story_points"]
    actual = issue.get("actual_story_points")

    # Save learning
    save_estimation(issue_key, predicted, actual)

    # Update Jira
    update_story_points(issue_key, predicted)

    # ✅ AI Reasoning
    ai_reasoning = (
        f"AI predicted {result['ai_points']} points with "
        f"{result['confidence']}% confidence. "
        f"Rule engine added {result['rule_score']} points. "
        f"Final normalized to {result['story_points']}."
    )

    # ✅ LLM Reasoning (GROQ)
    llm_reasoning = generate_llm_reasoning(
        issue["summary"],
        result
    )

    return {
        "issue": issue_key,
        "summary": issue["summary"],
        "actual_story_points": actual,
        "estimated_story_points": result,

        # UI fields
        "ai_reasoning": ai_reasoning,
        "llm_reasoning": llm_reasoning
    }


# History API
@app.get("/history")
def history():
    return get_learning_data()