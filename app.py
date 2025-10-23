import pandas as pd
import os
from flask import Flask, request, jsonify
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEN_API_KEY"))

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    # Read CSV
    df = pd.read_csv("data.csv")
    csv_data = df.to_csv(index=False)

    prompt = f"{user_message}\n\nHere is the sales data:\n{csv_data}"

    try:
        response = genai.TextGenerationModel(model="models/gemini-2.5-pro").generate_text(
            prompt=prompt
        )
        ai_reply = response.text
    except Exception as e:
        ai_reply = f"❌ Error while generating AI insight:\n{str(e)}"

    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)