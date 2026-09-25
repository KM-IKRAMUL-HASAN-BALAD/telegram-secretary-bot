import os
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Flask dummy web server for Render port check
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Credentials
BOT_TOKEN = '8129929285:AAGmG4eJ4e0d4H205kXp8cR8t2V_y3m2k_0'
MY_CHAT_ID = 6842013894

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return

    sender_id = update.message.from_user.id
    sender_name = update.message.from_user.first_name or "Unknown"

    # Admin nijoke auto-reply ba forward korbe na
    if sender_id == MY_CHAT_ID:
        return

    user_msg = update.message.text or "[Non-text message]"

    # Sender-ke auto response
    await update.message.reply_text(
        "Assalamu Alaikum! Currently I am offline. Your message has been forwarded to my admin."
    )

    # Admin-ke notification pathano
    forward_text = f"📩 New Message Received!\n\nFrom: {sender_name} ({sender_id})\nMessage: {user_msg}"
    await context.bot.send_message(chat_id=MY_CHAT_ID, text=forward_text)

if __name__ == '__main__':
    # Start Flask Web Server
    Thread(target=run_flask).start()

    # Start Telegram Bot
    print("Secretary Bot is running...")
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()

