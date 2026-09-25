import os
import asyncio
from threading import Thread
from flask import Flask
from telethon import TelegramClient, events

# Render port binding dummy web server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Telegram Bot Setup
API_ID = 26569107  # Apnar API ID
API_HASH = '1f440a33a38cdca3efec50c764e5256e'  # Apnar API Hash
BOT_TOKEN = '8129929285:AAGmG4eJ4e0d4H205kXp8cR8t2V_y3m2k_0'  # Apnar Bot Token
MY_CHAT_ID = 6842013894  # Apnar Personal Telegram ID

bot = TelegramClient('secretary_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage)
async def handle_new_message(event):
    if event.is_private:
        sender = await event.get_sender()
        sender_name = sender.first_name if sender else "Unknown"
        sender_id = event.sender_id
        
        if sender_id == MY_CHAT_ID:
            return

        user_msg = event.text or "[Non-text message]"
        
        # Auto-reply to sender
        await event.reply("Assalamu Alaikum! Currently I am offline. Your message has been forwarded to my admin.")
        
        # Forward message to Admin
        forward_text = f"📩 **New Message Received!**\n\n👤 **From:** {sender_name} (`{sender_id}`)\n💬 **Message:** {user_msg}"
        await bot.send_message(MY_CHAT_ID, forward_text)

if __name__ == '__main__':
    # Start Web server in background thread for Render Port check
    Thread(target=run_flask).start()
    
    # Start Telegram Bot
    print("Secretary Bot is running...")
    bot.run_until_disconnected()

