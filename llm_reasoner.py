import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

print("GROQ KEY:", os.getenv("GROQ_API_KEY"))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_llm_reasoning(summary, result):
    try:
        prompt = f"""
You are an expert Agile Scrum estimator.

Given:
Summary: {summary}

AI Prediction: {result['ai_points']}
Rule Score: {result['rule_score']}
Final Story Points: {result['story_points']}

Explain in simple human language why this story point is correct.
Keep it short (2-3 lines).
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ FIXED MODEL
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        print("LLM RESPONSE RECEIVED")  # 👈 DEBUG

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("LLM Error:", e)
        return "LLM reasoning unavailable"