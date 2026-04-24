def generate_reasoning(summary, result):
    reasons = []

    # AI reasoning
    reasons.append(
        f"AI model predicted {result['ai_points']} story points "
        f"with {result['confidence']}% confidence based on text complexity."
    )

    # Rule reasoning
    if result["rule_score"] > 0:
        reasons.append(
            f"Rule engine increased score by {result['rule_score']} due to:"
        )
        for r in result["reasons"]:
            reasons.append(f"• {r}")

    # Final reasoning
    reasons.append(
        f"Final score normalized to {result['story_points']} "
        f"based on Fibonacci scale."
    )

    return reasons