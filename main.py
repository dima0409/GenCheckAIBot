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
    db = database.Database()
    await db.create_db()
    await db.close()


async def main():
    await init_db()
    dp.include_router(router)
    await start_worker(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(" ")
