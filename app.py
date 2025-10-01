from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import statistics
import os
from dotenv import load_dotenv
import openai

# Load environment variables (for OpenAI key)
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)  # Allow frontend to connect to backend

# In-memory storage
submissions = []

# Default weight config if frontend not provided
DEFAULT_WEIGHTS = {
    "gwp": 0.4,
    "circularity": 0.4,
    "cost": 0.2
}

# ---------- HELPER FUNCTIONS ----------

def calculate_score(data):
    """
    Compute sustainability score based on GWP, Circularity, Cost
    using either provided weights from frontend or defaults.
    """
    try:
        gwp = float(data["gwp"])
        circularity = float(data["circularity"])
        cost = float(data["cost"])
    except ValueError:
        return None, "Invalid format for gwp, circularity, or cost."

    # Get weights from frontend or fallback to defaults
    weight_gwp = float(data.get("weight_gwp", DEFAULT_WEIGHTS["gwp"]))
    weight_circularity = float(data.get("weight_circularity", DEFAULT_WEIGHTS["circularity"]))
    weight_cost = float(data.get("weight_cost", DEFAULT_WEIGHTS["cost"]))

    # Normalize weights (to sum=1)
    total_weight = weight_gwp + weight_circularity + weight_cost
    if total_weight == 0:
        weight_gwp, weight_circularity, weight_cost = DEFAULT_WEIGHTS.values()
        total_weight = sum(DEFAULT_WEIGHTS.values())

    weight_gwp /= total_weight
    weight_circularity /= total_weight
    weight_cost /= total_weight

    # Normalize scores (0–100 scale)
    gwp_score = max(0, 100 - gwp * 10)           # lower GWP is better
    circularity_score = circularity              # already 0–100
    cost_score = max(0, 100 - cost * 5)          # cheaper is better

    final_score = (
        weight_gwp * gwp_score +
        weight_circularity * circularity_score +
        weight_cost * cost_score
    )

    return round(max(0, min(final_score, 100)), 2), None  # clamp 0–100

def assign_rating(score):
    if score >= 85:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "D"

def generate_ai_suggestions(data):
    """
    Uses OpenAI GPT to generate actionable sustainability suggestions.
    """
    system_prompt = (
        "You are a sustainability expert. Given product attributes such as materials used, "
        "transport method, packaging, global warming potential (GWP), cost, and circularity, "
        "give 2-3 actionable suggestions to make the product more environmentally sustainable. "
        "Avoid repeating general phrases. Base suggestions on concrete facts like material impact, "
        "transport emissions, etc."
    )

    product_desc = f"""
Product: {data.get("product_name", "Unknown")}
Materials: {', '.join(data.get("materials", []))}
Weight (g): {data.get("weight_grams", 0)}
Transport: {data.get("transport", "unknown")}
Packaging: {data.get("packaging", "unknown")}
GWP: {data.get("gwp", "unknown")}
Cost: {data.get("cost", "unknown")}
Circularity: {data.get("circularity", "unknown")}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": product_desc}
            ],
            temperature=0.7,
            max_tokens=150
        )
        output = response.choices[0].message.content
        suggestions = [line.strip("-• ").strip() for line in output.strip().split("\n") if line.strip()]
        return suggestions
    except Exception as e:
        print(f"AI suggestion error: {e}")
        return ["Unable to generate AI suggestions at this time."]

# ---------- API ROUTES ----------

@app.route("/score", methods=["POST"])
def score():
    data = request.get_json()

    required_fields = ["product_name", "materials", "weight_grams", "transport",
                       "packaging", "gwp", "cost", "circularity"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    score_value, error = calculate_score(data)
    if error:
        return jsonify({"error": error}), 400

    rating = assign_rating(score_value)

    # AI-powered suggestions
    suggestions = generate_ai_suggestions(data)

    result = {
        "product_name": data["product_name"],
        "sustainability_score": score_value,
        "rating": rating,
        "suggestions": suggestions
    }

    # For summary we can still extract some issues heuristically (keywords)
    issues_for_summary = []
    if "air" in data.get("transport", "").lower():
        issues_for_summary.append("Air transport")
    if "plastic" in [mat.lower() for mat in data.get("materials", [])]:
        issues_for_summary.append("Use of plastic")
    if "recyclable" not in data.get("packaging", "").lower():
        issues_for_summary.append("Non-recyclable packaging")

    submissions.append({
        "product_name": data["product_name"],
        "score": score_value,
        "rating": rating,
        "issues": issues_for_summary
    })

    return jsonify(result), 200

@app.route("/history", methods=["GET"])
def history():
    return jsonify(submissions)

@app.route("/score-summary", methods=["GET"])
def score_summary():
    if not submissions:
        return jsonify({"message": "No data yet"}), 200

    total_products = len(submissions)
    average_score = round(statistics.mean([s["score"] for s in submissions]), 2)

    ratings = {}
    issues = {}

    for s in submissions:
        r = s["rating"]
        ratings[r] = ratings.get(r, 0) + 1

        for issue in s["issues"]:
            issues[issue] = issues.get(issue, 0) + 1

    # Sort issues by frequency
    sorted_issues = sorted(issues.items(), key=lambda x: x[1], reverse=True)
    issue_labels = [item[0] for item in sorted_issues[:5]]
    issue_counts = [item[1] for item in sorted_issues[:5]]

    return jsonify({
        "total_products": total_products,
        "average_score": average_score,
        "ratings": ratings,
        "issue_labels": issue_labels,
        "issue_counts": issue_counts
    })

# ---------- FRONTEND ROUTE ----------

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
    #app.run(debug=True)
