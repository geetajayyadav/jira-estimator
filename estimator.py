from ai_model import predict_story_points
from semantic_engine import semantic_estimate


# -----------------------------
# 🔹 RULE ENGINE (technical complexity)
# -----------------------------
def rule_engine(text):
    score = 0
    reasons = []

    text = text.lower()

    if "api" in text or "integration" in text:
        score += 3
        reasons.append("API/Integration complexity")

    if "database" in text or "db" in text:
        score += 2
        reasons.append("Database work")

    if "security" in text or "auth" in text:
        score += 3
        reasons.append("Security concern")

    if "ui" in text or "frontend" in text:
        score += 1
        reasons.append("UI work")

    if "critical" in text or "production" in text:
        score += 2
        reasons.append("Critical production issue")

    return score, reasons


# -----------------------------
# 🔹 RISK / UNCERTAINTY
# -----------------------------
def risk_engine(text):
    risk_score = 0
    reasons = []

    text = text.lower()

    if "investigate" in text or "explore" in text:
        risk_score += 2
        reasons.append("High uncertainty (exploration)")

    if "unknown" in text:
        risk_score += 2
        reasons.append("Unknown requirements")

    if "migration" in text:
        risk_score += 3
        reasons.append("Migration risk")

    return risk_score, reasons


# -----------------------------
# 🔹 DEPENDENCY ENGINE
# -----------------------------
def dependency_engine(text):
    dep_score = 0
    reasons = []

    if "third party" in text or "external" in text:
        dep_score += 2
        reasons.append("External dependency")

    if "another team" in text:
        dep_score += 2
        reasons.append("Cross-team dependency")

    return dep_score, reasons


# -----------------------------
# 🔹 MARKET / PRIORITY FACTOR
# -----------------------------
def priority_factor(priority):
    if priority == "Highest":
        return 3, "High business urgency"
    elif priority == "High":
        return 2, "High priority work"
    elif priority == "Medium":
        return 1, "Normal priority"
    else:
        return 0, "Low priority"


# -----------------------------
# 🔹 SMART FIBONACCI
# -----------------------------
def normalize_story_points(score, risk):
    fibonacci = [1, 2, 3, 5, 8, 13, 21]

    # Risk-based rounding
    if risk > 2:
        return min([x for x in fibonacci if x >= score], default=21)
    else:
        return min(fibonacci, key=lambda x: abs(x - score))


# -----------------------------
# 🔹 MAIN ESTIMATOR (PROFESSOR LEVEL)
# -----------------------------
def estimate_story_points(summary, description, priority="Medium"):
    text = f"{summary} {description}"

    # 🔹 AI
    ai_result = predict_story_points(text)
    ai_score = ai_result["ai_points"]
    confidence = ai_result["confidence"]

    # 🔹 RULE
    rule_score, rule_reasons = rule_engine(text)

    # 🔹 RISK
    risk_score, risk_reasons = risk_engine(text)

    # 🔹 DEPENDENCY
    dep_score, dep_reasons = dependency_engine(text)

    # 🔹 PRIORITY
    priority_score, priority_reason = priority_factor(priority)

    # 🔹 SEMANTIC (historical learning)
    semantic_result = semantic_estimate(text)

    semantic_score = 0
    if semantic_result:
        semantic_score = semantic_result["semantic_points"]

    # -----------------------------
    # 🔥 WEIGHTED MODEL (IMPORTANT)
    # -----------------------------
    final_score = (
        (ai_score * 0.35) +
        (rule_score * 0.2) +
        (semantic_score * 0.25) +
        (risk_score * 0.1) +
        (dep_score * 0.05) +
        (priority_score * 0.05)
    )

    # -----------------------------
    # 🔥 CONFIDENCE ADJUSTMENT
    # -----------------------------
    if confidence < 50:
        final_score += 2

    # -----------------------------
    # 🔥 INTERACTION EFFECT
    # -----------------------------
    if rule_score > 3 and risk_score > 1:
        final_score += 2  # complexity explosion

    # -----------------------------
    # 🔹 NORMALIZE
    # -----------------------------
    story_points = normalize_story_points(round(final_score), risk_score)

    # -----------------------------
    # 🔹 REASONS (EXPLAINABILITY)
    # -----------------------------
    reasons = []
    reasons.extend(rule_reasons)
    reasons.extend(risk_reasons)
    reasons.extend(dep_reasons)
    reasons.append(priority_reason)

    if semantic_result:
        reasons.append(f"Similar past issue used (similarity: {semantic_result['similarity']})")

    # -----------------------------
    # 🔹 OUTPUT
    # -----------------------------
    return {
        "ai_points": ai_score,
        "confidence": confidence,
        "rule_score": rule_score,
        "risk_score": risk_score,
        "dependency_score": dep_score,
        "priority_score": priority_score,
        "semantic_score": semantic_score,
        "final_score": round(final_score),
        "story_points": story_points,
        "reasons": reasons
    }