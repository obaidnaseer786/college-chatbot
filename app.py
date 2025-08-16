from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Load API key from environment variable (set it in Render dashboard)
GEMINI_API_KEY = os.getenv("AIzaSyAouC6EuQvB38HkT6Uuv0lSq3o1HvmEZCA")

def call_gemini_api(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return "Sorry, I couldn’t understand that."
    else:
        return f"Error: {response.text}"

@app.route("/get-response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_input = data.get("message", "").lower()

    # Simple keyword-based rules
    if "fee" in user_input or "cost" in user_input or "price" in user_input:
        reply = "The fee structure is ₹50,000 per semester."
    elif "admission" in user_input or "apply" in user_input:
        reply = "Admissions are open till August 31st. Apply online through the college portal."
    elif "hostel" in user_input or "room" in user_input:
        reply = "Yes, hostel facilities are available for both boys and girls."
    else:
        # Fallback to Gemini API
        reply = call_gemini_api(user_input)

    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "College Chatbot Backend is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
