import base64
import os

from aiogram import F
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from aiogram.types import BufferedInputFile
from aiogram.types import CallbackQuery
from aiogram.types import Message
from dotenv import load_dotenv

from api.kandinsky import Text2ImageAPI
import commands.keyboards as kb
from commands.queue_manager import queue
from db import database
from file import file_manager

load_dotenv()

fm = file_manager.FileManager()
db = database.Database()

API_KEY = os.environ["API_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]

router = Router()

text2image = Text2ImageAPI(
    "https://api-key.fusionbrain.ai/", API_KEY, SECRET_KEY
)


class Generate(StatesGroup):
    prompt = State()


class Collecting(StatesGroup):
    dataset = State()


class Training(StatesGroup):
    detect = State()


@router.message(CommandStart())
async def start(message: Message):
    await message.reply(
        "Добро пожаловать в GenCheckAI \n"
        "Данный бот позволяет генерировать изображения"
        ' нейросетью "Кадинский", а также определять,'
        " является ли изображение сгенерированным. \n"
        "Выберите задачу",
        reply_markup=kb.keyboard_main,
    )


@router.message(F.text == "Генерация ✏️")
async def gen(message: Message, state: FSMContext):
    await state.set_state(Generate.prompt)
    await message.answer("Напишите промт для запроса:")


@router.message(Generate.prompt)
async def prompt(message: Message, state: FSMContext):
    await state.update_data(promt=message.text)
    data = await state.get_data()
    await state.clear()
    a = await message.answer("Ожидайте...")
    model_id = await text2image.get_model()
    uuid = await text2image.generate(data["promt"], model_id)
    images = await text2image.check_generation(uuid)
    image = str(images)
    image_bytes = base64.b64decode(image)
    await a.delete()
    await message.answer_photo(
        BufferedInputFile(file=image_bytes, filename="result.png"),
        caption="Ваша картинка \n Выберите задачу",
        reply_markup=kb.keyboard_main,
    )


@router.message(F.text == "Помощь проекту 🗃️")
async def help(message: Message, state: FSMContext):
    await state.set_state(Collecting.dataset)
    help_message = await message.reply(
        "Ты вошёл в режим помощи по сбору датасета для обучения ML-модели. "
        "Загрузи изображение, и я спрошу, "
        "является ли оно реальным или созданным ИИ. \n"
        "Пожалуйста, отвечай правильно."
    )
    await state.update_data(help_message_id=help_message.message_id)


@router.message(Collecting.dataset)
async def dataset(message: Message, state: FSMContext):
    user_id = message.from_user.id
    image = message.photo[-1].file_id
    await state.update_data(user_id=user_id, image=image)
    await message.delete()
    dataset_message = await message.answer_photo(
        caption="Выберите категорию.",
        photo=image,
        reply_markup=kb.keyboard_image,
    )
    await state.update_data(dataset_message_id=dataset_message.message_id)


@router.callback_query(lambda call: call.data == "ai")
async def ai(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    image = data["image"]
    await callback.bot.download(file=image, destination=f"{image}.png")
    await fm.save_image(str(user_id), f"{image}.png", "ai")
    await db.add_image(user_id, "ai", f"images\\{user_id}\\ai\\{image}.png")
    await state.clear()
    await db.close()
    await callback.bot.delete_message(
        chat_id=callback.message.chat.id, message_id=data["help_message_id"]
    )
    await callback.bot.delete_message(
        chat_id=callback.message.chat.id, message_id=data["dataset_message_id"]
    )
    await callback.bot.send_photo(
        chat_id=user_id,
        photo=image,
        caption="Изображение загруженно в 'Аи 🤖'",
    )


@router.callback_query(lambda call: call.data == "real")
async def real(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    image = data["image"]
    await callback.bot.download(file=image, destination=f"{image}.png")
    await fm.save_image(str(user_id), f"{image}.png", "real")
    await db.add_image(
        user_id, "real", f"images\\{user_id}\\real\\{image}.png"
    )
    await state.clear()
    await db.close()
    await callback.bot.delete_message(
        chat_id=callback.message.chat.id, message_id=data["help_message_id"]
    )
    await callback.bot.delete_message(
        chat_id=callback.message.chat.id, message_id=data["dataset_message_id"]
    )
    await callback.bot.send_photo(
        chat_id=user_id,
        photo=image,
        caption="Изображение загруженно в 'Реальное 📸'",
    )


@router.message(F.text == "Детекция 🤖")
async def ml(message: Message, state: FSMContext):
    await state.set_state(Training.detect)
    await message.reply("Отправьте изображение.")


@router.message(Training.detect, F.photo)
async def detect(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await queue.put((file_id, message, state))


@router.message(StateFilter(None))
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await message.answer("Я вас не понял")
