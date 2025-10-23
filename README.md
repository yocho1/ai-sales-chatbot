# AI Sales Chatbot

An AI-powered chatbot that analyzes and summarizes sales data.  
Built with **Python**, **Flask**, **Pandas**, and **Google Gemini / OpenAI APIs**.

---

## Features

- Upload sales data in **CSV** format or JSON array.
- Automatically calculates:
  - Total Sales
  - Average Sales
  - Highest Sale
  - Lowest Sale
- Generates AI insights and summaries about sales trends.
- Handles large datasets efficiently.
- Can be extended for deeper analytics (top products, sales by region, growth trends).

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yocho1/ai-sales-chatbot.git
cd ai-sales-chatbot

python -m venv venv
source venv/Scripts/activate   # Windows
# OR
source venv/bin/activate       # Linux / macOS

pip install -r requirements.txt

OPENAI_API_KEY=your_openai_api_key
# OR
GOOGLE_API_KEY=your_gemini_api_key

python app.py

curl -X POST http://127.0.0.1:5000/chat \
-H "Content-Type: application/json" \
-d '{
  "sales_data": [
    {"product": "Shoes", "sales": 200},
    {"product": "Bags", "sales": 300},
    {"product": "Hats", "sales": 450}
  ]
}'

curl -X POST -F "file=@data.csv" http://127.0.0.1:5000/upload


ai-sales-chatbot/
│
├── app.py              # Main Flask application
├── analyzer.py         # Simple Pandas sales analysis
├── analyzer_ai.py      # AI-powered sales analysis
├── data.csv            # Example sales data
├── requirements.txt    # Python dependencies
├── .env                # API keys (not pushed to GitHub)
└── README.md           # Project documentation
