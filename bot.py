import threading
from flask import Flask
app = Flask(__name__)
@app.route("/")
def home():
    return "Bot is alive!"
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()
import os
import time
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    data = {"contents": [{"parts": [{"text": text}]}]}
    r = requests.post(url, json=data, timeout=30)
    try:
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "صار في مشكلة شوي، جرب مرة تانية."

def send(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text[:4000]})

def main():
    offset = 0
    print("Bot started...")
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?timeout=30&offset={offset}"
            res = requests.get(url, timeout=35).json()
            for upd in res.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message", {})
                text = msg.get("text", "")
                chat_id = msg.get("chat", {}).get("id")
                if text and chat_id:
                    print("User:", text)
                    reply = ask_gemini(text)
                    send(chat_id, reply)
        except Exception as e:
            print(e)
            time.sleep(2)
from flask import Flask
import threading
import os
app = Flask(__name__)
@app.route("/")
def home():
    return "Bot is running!"
def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    main()
