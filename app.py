from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import spacy
import requests
import re


app = Flask(__name__)
CORS(app)


# Load spaCy model
nlp = spacy.load("en_core_web_sm")


# Set your Gemini API key
GEMINI_API_KEY = "AIzaSyAouC6EuQvB38HkT6Uuv0lSq3o1HvmEZCA"  # Replace this with your actual key


def call_gemini_api(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "Sorry, I couldn't understand that."
    else:
        return f"Gemini API Error: {response.status_code}"


def make_short_prompt(user_input):
    return (
        f"Answer briefly and simply—no formatting, lists, or asterisks. "
        f"Reply in one or two sentences. "
        f"Remove explanations, details, and avoid using * or bullet points. "
        f"Only give a direct answer. "
        f"User question: {user_input}"
    )


def clean_response(text):
    # Remove asterisks and trim spaces and excessive newlines
    text = text.replace("*", "").strip()
    # Collapse multiple spaces/newlines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    # If multiple sentences, only return the first two
    sentences = re.split(r'(?<=[.!?])\s+', ' '.join(lines))
    return ' '.join(sentences[:2])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get-response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_input = data.get("message", "")
    doc = nlp(user_input.lower())

    # Rule-based NLP intent matching
    if any(token.lemma_ in ["fee", "cost", "price"] for token in doc):
        reply = "The fee structure is ₹50,000 per semester."
    elif any(token.lemma_ in ["admission", "enroll", "apply"] for token in doc):
        reply = "Admissions are open till August 31st. Apply online through the college portal."
    elif any(token.lemma_ in ["requirement", "eligibility", "criteria"] for token in doc):
        reply = "Eligibility: Minimum 60% in 12th and a valid ID proof."
    elif any(token.lemma_ in ["hostel", "room", "stay"] for token in doc):
        reply = "Yes, hostel facilities are available for both boys and girls."
    elif any(token.lemma_ in ["scholarship", "fund", "discount"] for token in doc):
        reply = "Scholarships are available for meritorious and economically weaker students."
    elif any(token.lemma_ in ["contact", "call", "phone", "email"] for token in doc):
        reply = "You can contact the college at +91-9876543210 or email info@college.com"
    elif any(token.lemma_ in ["location", "address", "where"] for token in doc):
        reply = "The college is located in Karan Nagar, Srinagar, near SMHS Hospital."
    elif any(token.lemma_ in ["deadline", "last", "date"] for token in doc):
        reply = "The last date to apply is August 31st, 2025."
    else:
        # Fallback to Gemini for general questions with custom short prompt and cleaned response
        prompt = make_short_prompt(user_input)
        ai_response = call_gemini_api(prompt)
        reply = clean_response(ai_response)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
