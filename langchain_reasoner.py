import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Initialize LLM
llm = ChatOpenAI(
    temperature=0.3,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Prompt template
prompt = PromptTemplate.from_template("""
You are an expert Agile Scrum estimator.

Jira Ticket:
Summary: {summary}
Description: {description}

AI Prediction: {ai_points}
Rule Score: {rule_score}

Explain clearly:
- Why this estimate makes sense
- Keep it simple for a beginner

Answer:
""")


def generate_langchain_reasoning(summary, description, ai_points, rule_score):
    try:
        # Create final prompt
        final_prompt = prompt.format(
            summary=summary,
            description=description,
            ai_points=ai_points,
            rule_score=rule_score
        )

        # Direct invoke (NEW way, no chains)
        response = llm.invoke(final_prompt)

        return response.content

    except Exception as e:
        print("LangChain Error:", str(e))
        return "LLM reasoning unavailable"