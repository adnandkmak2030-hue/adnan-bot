import os
import time
import threading
import requests
from flask import Flask

# التوكن - منجرب كل الأسماء مشان ما يوقف
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("BOT_TOKEN") or os.getenv("TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

print("Token exists:", bool(TELEGRAM_TOKEN))
print("Gemini exists:", bool(GEMINI_KEY))

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    data = {"contents": [{"parts": [{"text": text}]}]}
    try:
        r = requests.post(url, json=data, timeout=30)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Gemini error:", e)
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
                    if text == "/start":
                        send(chat_id, "هلا! أنا عدنان الذكي 🤖 اسألني أي شي")
                    else:
                        reply = ask_gemini(text)
                        send(chat_id, reply)
        except Exception as e:
            print("Loop error:", e)
            time.sleep(2)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    main()
