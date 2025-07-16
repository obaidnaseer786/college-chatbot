from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

responses = {
    "fee": "The BCA fee is ₹30,000 per semester.",
    "admission": "Admission requires 10+2 with minimum 50%.",
    "last date": "The last date to apply is July 30, 2025.",
    "contact": "You can reach us at info@college.edu or call 01234-567890."
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-response", methods=["POST"])
def get_response():
    user_input = request.json.get("message", "").lower()
    for keyword in responses:
        if keyword in user_input:
            return jsonify({"reply": responses[keyword]})
    return jsonify({"reply": "Sorry, I didn’t understand that."})

if __name__ == "__main__":
    app.run(debug=True)
