import os
import telebot

TOKEN = os.environ.get("BOT_TOKEN", "حط_التوكن_هون")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "أهلا فيك! أنا بوتك العربي، شغال تمام ✅")

@bot.message_handler(func=lambda m: True)
def echo(message):
    if message.text:
        bot.reply_to(message, "وصلتني رسالتك: " + message.text)

print("البوت شغال...")
bot.infinity_polling()
