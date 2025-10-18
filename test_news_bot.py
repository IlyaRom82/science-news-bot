# test_news_bot.py
import logging
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
# ===== Токен бота =====
TOKEN = "8258197340:AAG1z4Bfcs6AhL7sWMXTREYvSlQFdDos7i8"

# ===== User-Agent для обхода защиты сайтов =====
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0"
    )
}

# ===== Функция для парсинга новостей =====
def fetch_news():
    news_list = []
    rss_sources = {
        "N+1": "https://nplus1.ru/rss",
        "Naked Science": "https://naked-science.ru/feed",
        "Habr": "https://habr.com/ru/rss/all/all/",
        "Popular Science": "https://www.popsci.com/feed/"
    }

    for source, url in rss_sources.items():
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, "xml")
            items = soup.find_all("item")[:3]
            for item in items:
                title = item.title.text if item.title else "Без заголовка"
                link = item.link.text if item.link else ""
                pub_date = item.pubDate.text if item.pubDate else "Без даты"
                news_list.append(f"🗞 <b>{source}</b>\n📅 {pub_date}\n🔗 {title}\n{link}")
        except Exception as e:
            news_list.append(f"⚠️ Ошибка при получении новостей с {source}: {e}")

    return news_list

# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Последние новости", callback_data="news")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я бот Science News 🧠\n"
        "Можешь написать /news или нажать кнопку ниже:",
        reply_markup=reply_markup
    )

# ===== /news =====
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ищу последние новости...")
    news_items = fetch_news()
    if news_items:
        await update.message.reply_text("\n\n".join(news_items), parse_mode="HTML")
    else:
        await update.message.reply_text("Не удалось найти новости.")

# ===== Callback кнопка =====
async def news_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Ищу последние новости...")
    news_items = fetch_news()
    if news_items:
        for item in news_items:
            await query.message.reply_text(item, parse_mode="HTML")
    else:
        await query.message.reply_text("Не удалось найти новости.")

# ===== Точка входа =====
if __name__ == "__main__":
    # Создаём приложение
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем хэндлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CallbackQueryHandler(news_button, pattern="news"))

    print("Бот запущен. Ctrl+C для остановки.")
    # Запуск polling без asyncio.run()
    app.run_polling(drop_pending_updates=True)
