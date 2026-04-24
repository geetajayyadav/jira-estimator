from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from jira_client import get_jira_issue, update_story_points
from estimator import estimate_story_points
from learning import save_estimation, get_learning_data

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

    # ✅ STEP 1: Safe Jira Fetch
    try:
        issue = get_jira_issue(issue_key)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Failed to fetch Jira issue",
                "details": str(e)
            }
        )

    # ✅ STEP 2: Validate Issue
    if not issue or "summary" not in issue:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid Jira issue key or no data found"}
        )

    try:
        # ✅ STEP 3: Estimation
        result = estimate_story_points(
            issue.get("summary", ""),
            issue.get("description", ""),
            issue.get("priority", "Medium")
        )

        # 🔥 VERY IMPORTANT FIX
        if not result:
            result = {}

        result.setdefault("story_points", 3)
        result.setdefault("ai_points", 3)
        result.setdefault("confidence", 50)
        result.setdefault("rule_score", 0)
        result.setdefault("reasons", [])   # ⚠️ CRITICAL FIX

        predicted = result["story_points"]
        actual = issue.get("actual_story_points")

        # ✅ STEP 4: Save Learning (safe)
        try:
            save_estimation(issue_key, predicted, actual)
        except Exception as e:
            print("Learning save error:", e)

        # ✅ STEP 5: Update Jira (safe)
        try:
            update_story_points(issue_key, predicted)
        except Exception as e:
            print("Jira update error:", e)

        # ✅ STEP 6: AI Reasoning
        ai_reasoning = (
            f"AI predicted {result['ai_points']} points with "
            f"{result['confidence']}% confidence. "
            f"Rule engine added {result['rule_score']} points. "
            f"Final normalized to {result['story_points']}."
        )

        # ✅ STEP 7: LLM Reasoning (safe)
        try:
            llm_reasoning = generate_llm_reasoning(
                issue.get("summary", ""),
                result
            )
        except Exception as e:
            print("LLM Error:", e)
            llm_reasoning = "LLM reasoning not available"

        # ✅ FINAL RESPONSE (SAFE)
        return {
            "issue": issue_key,
            "summary": issue.get("summary"),
            "actual_story_points": actual,
            "estimated_story_points": result,
            "ai_reasoning": ai_reasoning,
            "llm_reasoning": llm_reasoning
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Estimation failed",
                "details": str(e)
            }
        )


# History API
@app.get("/history")
def history():
    try:
        return get_learning_data()
    except Exception as e:
        return {"error": str(e)}