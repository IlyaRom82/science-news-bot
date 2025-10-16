#!/usr/bin/env python3
"""
Скрипт запуска Science News Telegram Bot
"""

import sys
from pathlib import Path


def check_requirements():
    """Проверка наличия необходимых файлов и зависимостей"""
    required_files = ['bot.py', 'news_client.py', 'requirements.txt']
    missing_files = []

    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"❌ Отсутствуют файлы: {', '.join(missing_files)}")
        return False

    # Проверяем .env файл
    if not Path('.env').exists():
        print("⚠️  Файл .env не найден!")
        print("📄 Создайте файл .env на основе .env.example")
        print("🔑 Добавьте ваш TELEGRAM_BOT_TOKEN")
        return False

    return True


def check_dependencies():
    """Проверка установленных зависимостей"""
    try:
        import telegram
        import requests
        import feedparser
        import dotenv
        print("✅ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        print("📦 Установите зависимости: pip install -r requirements.txt")
        return False


def main():
    """Основная функция"""
    print("🔧 Science News Telegram Bot")
    print("=" * 40)

    # Проверяем наличие нужных файлов
    if not check_requirements():
        sys.exit(1)

    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)

    # Запускаем бота
    try:
        print("🚀 Запуск бота...")
        from bot import ScienceNewsBot
        bot = ScienceNewsBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
