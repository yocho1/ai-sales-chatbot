import pandas as pd
import numpy as np
import os
import sys
from dotenv import load_dotenv
from google import genai

# Enable UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

def analyze_sales_data(file_path):
    # --- LOAD DATA ---
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return
    except pd.errors.EmptyDataError:
        print(f"❌ CSV file is empty: {file_path}")
        return
    except Exception as e:
        print(f"❌ Failed to read CSV: {e}")
        return

    # --- VALIDATION ---
    if "sales" not in data.columns or "product" not in data.columns:
        print("❌ CSV must contain 'product' and 'sales' columns.")
        return
    if not np.issubdtype(data["sales"].dtype, np.number):
        print("❌ 'sales' column must be numeric.")
        return

    # --- BASIC STATS ---
    total_sales = data['sales'].sum()
    avg_sales = data['sales'].mean()
    median_sales = data['sales'].median()
    std_sales = data['sales'].std()
    highest_sale = data.loc[data['sales'].idxmax()]
    lowest_sale = data.loc[data['sales'].idxmin()]

    # --- TREND DETECTION ---
    trend = None
    if len(data['sales']) > 1:
        if data['sales'].iloc[-1] > data['sales'].iloc[0]:
            trend = "increasing"
        elif data['sales'].iloc[-1] < data['sales'].iloc[0]:
            trend = "decreasing"
        else:
            trend = "stable"

    # --- AI INSIGHT GENERATION ---
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

    # --- PRINT RESULTS ---
    print("\n📊 SALES REPORT")
    print(f"Total Sales: {total_sales}")
    print(f"Average Sales: {avg_sales:.2f}")
    print(f"Median Sales: {median_sales:.2f}")
    print(f"Standard Deviation: {std_sales:.2f}")
    print(f"Highest Sale: {highest_sale['product']} ({highest_sale['sales']})")
    print(f"Lowest Sale: {lowest_sale['product']} ({lowest_sale['sales']})")
    print(f"Trend: {trend}")

    print("\n🤖 AI INSIGHT")
    print(ai_insight)

if __name__ == "__main__":
    analyze_sales_data("data.csv")