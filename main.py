import os
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

BOT_TOKEN = '8129929285:AAGmG4eJ4e0d4H205kXp8cR8t2V_y3m2k_0'
MY_CHAT_ID = 6842013894

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return

    sender_id = update.message.from_user.id
    sender_name = update.message.from_user.first_name or "Unknown"

    if sender_id == MY_CHAT_ID:
        return

    user_msg = update.message.text or "[Non-text message]"

    await update.message.reply_text(
        "Assalamu Alaikum! Currently I am offline. Your message has been forwarded to my admin."
    )

    forward_text = f"📩 **New Message!**\n\n👤 **From:** {sender_name} (`{sender_id}`)\n💬 **Message:** {user_msg}"
    await context.bot.send_message(chat_id=MY_CHAT_ID, text=forward_text)

def main():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Secretary Bot is running...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()




