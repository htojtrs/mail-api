from flask import Flask, jsonify
import json
import requests

app = Flask(__name__)

# Microsoft Graph API credentials
tenant_id = "a188da3d-cf4b-4657-9b77-3da81142fa4d"
client_id = "94da0819-4aad-4801-bb65-44d844a10aaf"
client_secret = "R.p8Q~sXVSX9bZjBK5IbQIHccZgMVq5Tnw7-0bDZ"
scope = "https://graph.microsoft.com/.default"
user_email = "jacob@htoperations.dk"

@app.route("/emails", methods=["GET"])
def get_emails():
    try:
        with open("emails.json", "r", encoding="utf-8") as f:
            emails = json.load(f)
        return jsonify(emails)
    except FileNotFoundError:
        return jsonify({"error": "emails.json not found"}), 404

@app.route("/refresh", methods=["POST"])
def refresh_emails():
    # Hent token
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope
    }
    token_r = requests.post(token_url, data=token_data)
    access_token = token_r.json().get("access_token")

    if not access_token:
        return jsonify({"error": "Kunne ikke hente token", "details": token_r.text}), 500

    # Hent e-mails
    graph_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/mailFolders/inbox/messages?$top=10"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    emails_r = requests.get(graph_url, headers=headers)

    if emails_r.status_code != 200:
        return jsonify({"error": "Fejl ved hentning af e-mails", "details": emails_r.text}), 500

    emails = emails_r.json().get("value", [])

    # Gem i fil
    with open("emails.json", "w", encoding="utf-8") as f:
        json.dump(emails, f, indent=2, ensure_ascii=False)

    return jsonify({"message": "E-mails opdateret", "antal": len(emails)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
