# 🤖 AI Sales Chatbot (Flask + Gemini AI)

This project is an intelligent **AI-powered sales analysis chatbot** built using **Flask**, **Gemini AI**, and **Python**.  
It allows users to chat with an AI or upload sales data (CSV/JSON) to get detailed insights such as:
- Top-performing products  
- Weak products  
- Trend interpretation  
- Revenue improvement recommendations  

---

## 🧰 Tech Stack
- **Backend:** Flask (Python)
- **AI Model:** Gemini Pro (via `google-generativeai`)
- **Data Processing:** Pandas & NumPy
- **Environment Management:** python-dotenv
- **Frontend:** Simple HTML/CSS + JavaScript (index.html)

---

## 🚀 Features
✅ AI chat powered by Gemini  
✅ Sales data upload (CSV or JSON)  
✅ Automated data analysis and insights  
✅ JSON-based API endpoints  
✅ Ready for local testing or deployment  

---

## ⚙️ Installation Guide


### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/ai-sales-chatbot.git
cd ai-sales-chatbot

### 2️⃣ Create and Activate a Virtual Environment

# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Set Up Environment Variables

GEMINI_API_KEY=your_gemini_api_key_here

🧩 Project Structure : 

📁 ai-sales-chatbot/
 ┣ 📄 app.py
 ┣ 📄 requirements.txt
 ┣ 📄 README.md
 ┣ 📄 .env              # (keep this private)
 ┣ 📁 templates/
 ┃ ┗ 📄 index.html
 ┗ 📁 static/
    ┗ 📄 style.css


🧠 API Endpoints
🔹 Chat with AI

POST → /chat

{
  "message": "Hello, who are you?"
}


Response:

{
  "reply": "Hello! I'm your AI assistant for sales insights."
}

🔹 Analyze Sales Data

POST → /analyze

Option 1: Send JSON
curl -X POST http://127.0.0.1:5000/analyze \
-H "Content-Type: application/json" \
-d '[{"product": "Pouf A", "sales": 120}, {"product": "Pouf B", "sales": 300}]'

Option 2: Send CSV
curl -X POST http://127.0.0.1:5000/analyze \
-F "file=@data.csv"


Response Example:

{
  "total_sales": 420,
  "average_sales": 210,
  "trend": "increasing",
  "ai_insight": "Your top performer is Pouf B with 300 sales..."
}

💻 Run the App : 
python app.py


Visit:

http://127.0.0.1:5000

👨‍💻 Author

Achraf Lachgar
💼 AI Developer
📍 Based in Morocco
