from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/emails", methods=["GET"])
def get_emails():
    try:
        with open("emails.json", "r", encoding="utf-8") as f:
            emails = json.load(f)
        return jsonify(emails)
    except FileNotFoundError:
        return jsonify({"error": "emails.json not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
