import logging
import os

import requests
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes)

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/api/posts/")
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# Команда /posts
async def posts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(API_URL)
    if response.status_code == 200:
        posts = response.json()
        keyboard = [[InlineKeyboardButton(post['title'], callback_data=str(post['id']))] for post in posts]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Выберите пост:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Ошибка при получении постов.")

# Обработка кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    post_id = query.data
    response = requests.get(f"{API_URL}{post_id}/")
    if response.status_code == 200:
        post = response.json()
        text = f"*{post['title']}*\n\n{post['text']}\n\n🗓 {post['pub_date']}"
        await query.edit_message_text(text=text, parse_mode="Markdown")
    else:
        await query.edit_message_text(text="Ошибка при получении поста.")

# Запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("posts", posts_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
