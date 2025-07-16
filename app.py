from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/get-response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_input = data.get("message", "").lower()

    # Keyword-based response logic
    if "fee" in user_input:
        reply = "The fee structure is ₹50,000 per semester."
    elif "admission" in user_input:
        reply = "Admissions are open till August 31st. Apply online through the college portal."
    elif "requirement" in user_input or "eligibility" in user_input:
        reply = "Eligibility: Minimum 60% in 12th and a valid ID proof."
    elif "duration" in user_input or "course length" in user_input:
        reply = "The course duration is 3 years (6 semesters)."
    elif "hostel" in user_input:
        reply = "Yes, hostel facilities are available for both boys and girls."
    elif "scholarship" in user_input:
        reply = "Scholarships are available for meritorious and economically weaker students."
    elif "contact" in user_input or "phone" in user_input:
        reply = "You can contact the college at +91-9876543210 or email info@college.com"
    elif "location" in user_input or "where" in user_input:
        reply = "The college is located in Karan Nagar, Srinagar, near SMHS Hospital."
    elif "last date" in user_input or "deadline" in user_input:
        reply = "The last date to apply is August 31st, 2025."
    else:
        reply = "I'm not sure about that. Please ask about fees, admission, hostel, or eligibility."

    return jsonify({"reply": reply})

# 🟢 This part is required for deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
