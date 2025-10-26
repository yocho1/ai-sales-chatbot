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

    # Convert numpy / pandas scalar types to native Python types so jsonify can serialize them
    def to_native(val):
        try:
            if isinstance(val, (np.integer,)):
                return int(val)
            if isinstance(val, (np.floating,)):
                return float(val)
            if hasattr(val, 'item'):
                return val.item()
        except Exception:
            pass
        return val

    total_sales_native = to_native(total_sales)
    avg_sales_native = to_native(round(avg_sales, 2))
    median_sales_native = to_native(round(median_sales, 2))
    std_sales_native = to_native(round(std_sales, 2))

    highest_sale_product = str(highest_sale['product'])
    lowest_sale_product = str(lowest_sale['product'])
    highest_sale_sales = to_native(highest_sale['sales'])
    lowest_sale_sales = to_native(lowest_sale['sales'])

    return {
        "total_sales": total_sales_native,
        "average_sales": avg_sales_native,
        "median_sales": median_sales_native,
        "std_sales": std_sales_native,
        "highest_sale": {"product": highest_sale_product, "sales": highest_sale_sales},
        "lowest_sale": {"product": lowest_sale_product, "sales": lowest_sale_sales},
        "trend": str(trend),
        "ai_insight": ai_insight
    }

# --- ROUTES ---

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # Your chat HTML

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = str(data['message'])

        # Build a prompt for the AI model. You can expand this to include
        # conversation history or system instructions.
        prompt = f"User: {user_message}\nAssistant:"

        try:
            response = client.models.generate_content(
                model="models/gemini-pro-latest",
                contents=prompt
            )
            ai_reply = getattr(response, 'text', None) or str(response)
        except Exception as e:
            # If the AI call fails, fall back to a friendly message
            ai_reply = f"(AI generation failed) {e}"

        return jsonify({"response": ai_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "GET":
        return render_template("analyze.html")  # Create this template or use index.html
        
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
            
        file = request.files["file"]
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
            
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Only CSV files are allowed"}), 400
            
        data = pd.read_csv(file)

        result = analyze_sales_df(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})




if __name__ == "__main__":
    app.run(debug=True)
