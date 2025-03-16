import asyncio
import logging

from aiogram import Bot

from ml import model

queue = asyncio.Queue()
ml_model = model.ModelInf()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def worker(bot: Bot):
    while True:
        file_id, message, state = await queue.get()
        try:
            file_info = await bot.get_file(file_id)
            file_bytes = await bot.download_file(file_info.file_path)

            prediction = ml_model.predict(file_bytes)

            await message.answer(prediction)
            await state.clear()
        except Exception as e:
            logger.error(f"Ошибка при обработке файла {file_id}: {e}")
            await message.answer("Произошла ошибка при обработке фотографии.")
            await state.clear()
        finally:
            queue.task_done()
            logger.info(
                f"Файл {file_id} обработан. Размер очереди: {queue.qsize()}"
            )


async def start_worker(bot: Bot):
    asyncio.create_task(worker(bot))
