import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.error import TelegramError
from handlers.pattern.validatorpattern import *
from telegram.ext import (
  ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
  )
from handlers.chbot2 import ChatBotResponse
from geoChat import GeoInformationProvider
from handlers.contents import text_value

load_dotenv()
access_token = os.getenv('BOT_TOKEN')
information = [text_value.introduction]

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
    app = ApplicationBuilder().token(access_token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(MessageHandler(filters.TEXT, aiversion))
    print('Bot is running...')
    app.run_polling()
    
    
if __name__ == "__main__":
    run_bot()



