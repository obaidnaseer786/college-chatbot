from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import spacy

app = Flask(__name__)
CORS(app)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

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
        reply = "I'm not sure about that. Please ask about fees, admissions, or hostel."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
