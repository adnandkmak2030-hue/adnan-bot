import telebot
from telebot import types
import os

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

def show_buttons(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("هلا 👋", callback_data="hala")
    b2 = types.InlineKeyboardButton("كيفك؟ 😊", callback_data="kifak")
    b3 = types.InlineKeyboardButton("شو اسمك؟ 🤔", callback_data="ismak")
    b4 = types.InlineKeyboardButton("نكتة 😂", callback_data="nokta")
    b5 = types.InlineKeyboardButton("شو بتعمل؟ ⚡", callback_data="shobtaamel")
    b6 = types.InlineKeyboardButton("دعاء 🙏", callback_data="duaa")
    markup.add(b1, b2, b3, b4, b5, b6)
    bot.send_message(chat_id, "اهلا فيك بعدنان الذكي ❤️\nاختار زر من تحت 👇", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    txt = message.text
    if txt == "/start" or txt == "/help":
        show_buttons(message.chat.id)
    elif "هلا" in txt or "سلام" in txt:
        bot.reply_to(message, "هلا والله! نورت ❤️")
    elif "كيفك" in txt:
        bot.reply_to(message, "انا تمام، وانت كيفك؟")
    elif "اسمك" in txt:
        bot.reply_to(message, "اسمي عدنان الذكي")
    else:
        bot.reply_to(message, "ابعتلو /start مشان تطلعلك الأزرار 👇")

@bot.callback_query_handler(func=lambda call: True)
def buttons(call):
    if call.data == "hala":
        bot.send_message(call.message.chat.id, "هلا والله! نورت البوت ❤️")
    elif call.data == "kifak":
        bot.send_message(call.message.chat.id, "انا تمام الحمدلله، وانت كيفك؟")
    elif call.data == "ismak":
        bot.send_message(call.message.chat.id, "اسمي عدنان الذكي")
    elif call.data == "nokta":
        bot.send_message(call.message.chat.id, "ليش الكمبيوتر راح للدكتور؟\nلانه مفيرس 😂")
    elif call.data == "shobtaamel":
        bot.send_message(call.message.chat.id, "انا قاعد عم استناك تحكي معي ⚡")
    elif call.data == "duaa":
        bot.send_message(call.message.chat.id, "الله يوفقك ويسعدك ويحققلك كل شي بتتمناه 🙏")
    bot.answer_callback_query(call.id)

print("البوت شغال...")
bot.infinity_polling(skip_pending=True, timeout=60)
