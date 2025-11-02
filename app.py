from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# set your secret
SECRET = "Tushar123SecretKey"  # must match what you fill in Google Form

@app.route("/quiz", methods=["POST"])
def quiz():
    try:
        data = request.get_json()
    except:
        return jsonify({"error": "Invalid JSON"}), 400

    # Verify secret
    if data.get("secret") != SECRET:
        return jsonify({"error": "Forbidden"}), 403

    email = data.get("email")
    quiz_url = data.get("url")

    if not (email and quiz_url):
        return jsonify({"error": "Missing fields"}), 400

    # Fetch quiz page
    page = requests.get(quiz_url)
    soup = BeautifulSoup(page.text, "html.parser")

    # Extract example question
    question_text = soup.text.lower()

    # (Example logic for a sample question — customize when real quiz comes)
    if "sum" in question_text:
        answer = 12345
    else:
        answer = "unknown"

    # Submit the answer to the provided submit URL
    submit_url = "https://tds-llm-analysis.s-anand.net/submit"
    response = requests.post(submit_url, json={
        "email": email,
        "secret": SECRET,
        "url": quiz_url,
        "answer": answer
    })

    return jsonify({"message": "Answer submitted", "response": response.text}), 200


if __name__ == "__main__":
    app.run(debug=True)
