import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Render এ এনভায়রনমেন্ট ভ্যারিয়েবল ব্যবহার করা ভালো, তবে আপনি চাইলে সরাসরি টোকেন ও চ্যাট আইডি বসাতে পারেন
BOT_TOKEN = os.getenv("BOT_TOKEN", "8703315848:AAHgpmb0xH58vedt3hAE7R6lgXUhsKXOO9U")
MY_CHAT_ID = int(os.getenv("MY_CHAT_ID", "8989638281"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == MY_CHAT_ID:
        await update.message.reply_text("স্বাগতম স্যার! সেক্রেটারী মোড সক্রিয় আছে।")
    else:
        await update.message.reply_text(
            f"হ্যালো {update.effective_user.first_name}!\n\n"
            "আমি স্যারের সিক্রেটারি। স্যার বর্তমানে ব্যস্ত আছেন। "
            "আপনার মেসেজটি স্যারের কাছে পৌঁছে দেওয়া হয়েছে।"
        )

async def secretary_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    incoming_text = update.message.text

    if user.id == MY_CHAT_ID:
        await update.message.reply_text("স্যার, আমি আপনার নতুন নির্দেশনার জন্য প্রস্তুত।")
        return

    # ভিজিটরকে মেসেজ
    await update.message.reply_text(
        f"ধন্যবাদ {user.first_name}! আপনার মেসেজটি স্যারকে জানানো হয়েছে।"
    )

    # আপনাকে (মালিককে) মেসেজ ফরওয়ার্ড
    forward_message = (
        f"📩 **নতুন মেসেজ!**\n\n"
        f"👤 **প্রেরক:** {user.full_name} (@{user.username})\n"
        f"🆔 **User ID:** `{user.id}`\n"
        f"💬 **মেসেজ:** {incoming_text}"
    )
    await context.bot.send_message(
        chat_id=MY_CHAT_ID, 
        text=forward_message, 
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), secretary_handler))
    print("বট সফলভাবে চালু হয়েছে...")
    app.run_polling()

