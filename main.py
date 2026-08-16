import os
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# =============================================================
# আপনার তথ্য দিয়ে নিচের মানগুলো পরিবর্তন করুন
# =============================================================
BOT_TOKEN = "8611125204:AAGOYnrYofv-8O-REpGXckY7FQePqZ_i2L8"          # BotFather থেকে প্রাপ্ত টোকেন
YOUTUBE_URL = "https://youtube.com/@imueditznews"  # আপনার ইউটিউব চ্যানেল লিংক
TELEGRAM_CHANNEL = "@viralvideohd2"  # @ সহ টেলিগ্রাম চ্যানেলের ইউজারনেম
LOCKED_LINK = "https://t.me/viralvideohd2/43" # ইউজার যে আনলকড ফাইল/লিংক পাবে
# =============================================================

# Flask Server (Koyeb-এ বট ২৪/৭ সচল রাখার জন্য)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Telegram Bot Setup
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    
    btn_yt = InlineKeyboardButton(text="🔴 Subscribe YouTube", url=YOUTUBE_URL)
    btn_tg = InlineKeyboardButton(text="📢 Join Telegram", url=f"https://t.me/{TELEGRAM_CHANNEL.replace('@','')}")
    btn_unlock = InlineKeyboardButton(text="🔓 Unlock Link", callback_data="check_sub")
    
    markup.add(btn_yt)
    markup.add(btn_tg)
    markup.add(btn_unlock)
    
    bot.reply_to(
        message, 
        "<b>👋 স্বাগতম!</b>\n\n"
        "গোপন লিংকটি আনলক করতে নিচের ধাপগুলো পূরণ করুন:\n\n"
        "১. <b>Subscribe YouTube</b>-এ ক্লিক করে সাবস্ক্রাইব করুন।\n"
        "২. <b>Join Telegram</b>-এ ক্লিক করে চ্যানেলে জয়েন করুন।\n"
        "৩. তারপর <b>Unlock Link</b> বোতামে ক্লিক করুন।",
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.from_user.id
    try:
        check = bot.get_chat_member(TELEGRAM_CHANNEL, user_id)
        if check.status in ['member', 'administrator', 'creator']:
            bot.answer_callback_query(call.id, "ধন্যবাদ! আপনার লিংক আনলক করা হয়েছে।")
            bot.send_message(
                call.message.chat.id, 
                f"🎉 <b>আপনার আনলকড লিংক:</b>\n{LOCKED_LINK}",
                parse_mode="HTML"
            )
        else:
            bot.answer_callback_query(call.id, "⚠️ আপনি এখনো টেলিগ্রাম চ্যানেলে যুক্ত হননি!", show_alert=True)
    except Exception as e:
        bot.answer_callback_query(call.id, "⚠️ বটটি চ্যানেলে অ্যাডমিন করা আছে কিনা যাচাই করুন।", show_alert=True)

if __name__ == '__main__':
    # Web server backend
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # Start telegram bot
    print("Bot is starting...")
    bot.infinity_polling()

