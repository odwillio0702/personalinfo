from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route("/schedule", methods=["POST"])
def schedule():
    data = request.json
    chat_id = data["chat_id"]
    text = data["text"]
    time = data["time"]
    days = data["days"]

    message = f"/schedule {text} {time} {days}"

    r = requests.post(
        f"{BOT_API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": message
        }
    )

    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
