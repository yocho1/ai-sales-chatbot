from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from google import genai
import sys

# Fix Unicode printing issues on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Load .env variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__, template_folder="templates")  # Make sure your index.html is in 'templates'

# --- SALES DATA ANALYSIS FUNCTION ---
def analyze_sales_df(data):
    if "sales" not in data.columns or "product" not in data.columns:
        return {"error": "CSV/JSON must contain 'product' and 'sales' columns."}

    if not np.issubdtype(data["sales"].dtype, np.number):
        return {"error": "'sales' column must be numeric."}

    total_sales = data['sales'].sum()
    avg_sales = data['sales'].mean()
    median_sales = data['sales'].median()
    std_sales = data['sales'].std()
    highest_sale = data.loc[data['sales'].idxmax()]
    lowest_sale = data.loc[data['sales'].idxmin()]

    trend = "stable"
    if len(data['sales']) > 1:
        if data['sales'].iloc[-1] > data['sales'].iloc[0]:
            trend = "increasing"
        elif data['sales'].iloc[-1] < data['sales'].iloc[0]:
            trend = "decreasing"

    prompt = f"""
You are a senior data analyst AI.
Analyze this sales dataset deeply and provide:
1. Key performance summary
2. Top performing products
3. Weak products
4. Sales trend interpretation
5. Strategic recommendations to increase revenue

Data summary:
- Total Sales: {total_sales}
- Average Sales: {avg_sales:.2f}
- Median Sales: {median_sales:.2f}
- Standard Deviation: {std_sales:.2f}
- Highest Sale: {highest_sale['product']} ({highest_sale['sales']})
- Lowest Sale: {lowest_sale['product']} ({lowest_sale['sales']})
- Trend: {trend}
"""
    try:
        response = client.models.generate_content(
            model="models/gemini-pro-latest",
            contents=prompt
        )
        ai_insight = response.text
    except Exception as e:
        ai_insight = f"❌ AI Insight generation failed: {e}"

    return {
        "total_sales": total_sales,
        "average_sales": round(avg_sales, 2),
        "median_sales": round(median_sales, 2),
        "std_sales": round(std_sales, 2),
        "highest_sale": {"product": highest_sale['product'], "sales": highest_sale['sales']},
        "lowest_sale": {"product": lowest_sale['product'], "sales": lowest_sale['sales']},
        "trend": trend,
        "ai_insight": ai_insight
    }

# --- ROUTES ---

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # Your chat HTML

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"error": "No message provided."})

        response = client.models.generate_content(
            model="models/gemini-pro-latest",
            contents=user_message
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" in request.files:
        data = pd.read_csv(request.files["file"])
    else:
        json_data = request.get_json()
        data = pd.DataFrame(json_data)

    result = analyze_sales_df(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
