import pandas as pd
import numpy as np
from google import genai
from google.genai import types
import sys
import os
from dotenv import load_dotenv


sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

def analyze_sales_data(file_path):
    # Load data
    data = pd.read_csv(file_path)

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
            model="models/gemini-2.5-pro",
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