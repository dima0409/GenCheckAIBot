import asyncio
import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from dotenv import load_dotenv

from commands.handlers import router
from commands.queue_manager import start_worker
from db import database

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def init_db():
    """Иницилизация БД.

    Создает необходимые таблицы в БД при старте приложения.

    Выполняет:
        1. Подключение к БД.
        2. Создание таблиц(если их нет).
        3. Закрытие соединения.
    """
    db = database.Database()
    await db.create_db()
    await db.close()


async def main():
    """Основная асинхронная функция запуска бота.

    Выполняет:
        1. Инициализацию БД
        2. Подключение роутера с обработчиками
        3. Запуск фонового ворерка для очереди
        4. Старт бота
    """
    await init_db()
    dp.include_router(router)
    await start_worker(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    """Точка входа в приложение.

    Настраивает логирование и запускает основную асинхронную функцию
    """
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(" ")
