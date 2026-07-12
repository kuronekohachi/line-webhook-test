from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "ok", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    print("=== body ===")
    print(request.get_data(as_text=True))
    return "ok", 200
