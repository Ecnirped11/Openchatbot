import os
import re
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import (
  ApplicationBuilder,
  CommandHandler,
  MessageHandler,
  ContextTypes,
  filters,
)

from chbot2 import ChatBotResponse
from geoChat import GeoInformationProvider

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/{BOT_TOKEN}"
PUBLIC_URL = os.getenv("PUBLIC_URL") 
PORT = int(os.environ.get("PORT", 5000))

# patterns
valid_text = re.compile(r"[a-zA-Z0-9.]+")
valid_phone = re.compile(r"\+[0-9]+")

# Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username or "there"
    await update.message.reply_text(f"Welcome, @{username}! Send /help to get started.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
Hello!
Ask me anything, or send a phone number like +1234567890 to get its country info.
""")

async def aiversion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if valid_phone.search(text):
        location = GeoInformationProvider(text).provide_location()
        await update.message.reply_text(location)
    elif valid_text.search(text):
        response = ChatBotResponse(text).response()
        await update.message.reply_text(response)

flask_app = Flask(__name__)

@flask_app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), Bot(BOT_TOKEN))
    flask_app.bot_app.update_queue.put(update)
    return "OK"
    
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), aiversion))

    app.bot.set_webhook(f"{PUBLIC_URL}{WEBHOOK_PATH}")
    flask_app.bot_app = app

  
    flask_app.run(host="0.0.0.0", port=PORT)