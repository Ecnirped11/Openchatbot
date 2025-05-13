import os
import re
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
from chbot2 import ChatBotResponse
from geoChat import GeoInformationProvider
from flask import Flask
import threading

load_dotenv()

access_token = os.getenv('BOT_TOKEN')
print(access_token)

valid_text_pattern = re.compile(r"[a-zA-Z0-9.]+")
valid_phone_pattern = re.compile(r'\+[0-9]+')

introduction = """
Hello!
I'm here to assist you with any type of question you may have. Whether it's a general inquiry or something specific, feel free to ask.

Additionally, I can help determine the location of your phone number by analyzing the country code, just provide the number without any letters or special characters.

Example: +124357490245 ✔️
"""

information = [introduction]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        username = update.effective_user.username
        await update.message.reply_text(f"Welcome, @{username}! If you need assistance, just type /help.")
    except Exception as e:
        print(f'Error: {e}')
    except TelegramError as e:
        print(f'Telegram error: {e}')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for element in information:
        await update.message.reply_text(f'{element}')

async def aiversion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text

    if valid_text_pattern.search(prompt) and not valid_phone_pattern.search(prompt):
        pass_user_prompt = ChatBotResponse(prompt)
        response = pass_user_prompt.response()
        await update.message.reply_text(response)
    elif valid_phone_pattern.search(prompt):
        pass_num_prompt = GeoInformationProvider(prompt)
        num_response = pass_num_prompt.provide_location()
        await update.message.reply_text(f'{num_response}')

def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    app = ApplicationBuilder().token(access_token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(MessageHandler(filters.TEXT, aiversion))
    print('Bot is running...')
    app.run_polling()

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return "Bot is running."

if __name__ == "__main__":
    
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    port = int(os.environ.get('PORT', 5000))
    flask_app.run(host='0.0.0.0', port=port)