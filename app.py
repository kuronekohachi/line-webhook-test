from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.environ.get("LINE_USER_ID")

@app.route("/")
def home():
    return "ok", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    print("=== webhook body ===")
    print(request.get_data(as_text=True))
    return "ok", 200

@app.route("/notify", methods=["GET", "POST"])
def notify():
    if not LINE_CHANNEL_ACCESS_TOKEN:
        return jsonify({"error": "LINE_CHANNEL_ACCESS_TOKEN is not set"}), 500
    if not LINE_USER_ID:
        return jsonify({"error": "LINE_USER_ID is not set"}), 500

    text = request.args.get("text", "通知テストです")

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    r = requests.post(url, headers=headers, json=body)
    return jsonify({
        "status_code": r.status_code,
        "response": r.text
    }), r.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
