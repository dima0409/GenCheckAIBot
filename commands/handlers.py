import base64

from aiogram import F, Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.state import StatesGroup, State
from  aiogram.fsm.context import FSMContext

import commands.keyboards as kb
from api.kandinsky import Text2ImageAPI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ["API_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]

router = Router()

text2image = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)


class Generate(StatesGroup):
    prompt = State()




@router.message(CommandStart())
async def start(message: Message):
    await message.reply('Добро пожаловать в GenCheckAI \n'
                        'Данный бот позволяет генерировать изображения нейросетью "Кадинский", а также определять, является ли изображение сгенерированным. \n'
                        'Выберите задачу',
                        reply_markup=kb.keyboard1)


@router.message(F.text == 'Генерация')
async def gen(message: Message, state: FSMContext):
    await state.set_state(Generate.prompt)
    await message.answer('Напишите промт для запроса:')


@router.message(Generate.prompt)
async def prompt(message: Message, state: FSMContext):
    await state.update_data(promt=message.text)
    data = await state.get_data()
    await state.clear()
    a = await message.answer('Ожидайте...')
    model_id = text2image.get_model()
    uuid = text2image.generate(data, model_id)
    images = text2image.check_generation(uuid)
    image = str(images)
    image_bytes = base64.b64decode(image)
    await a.delete()
    await message.answer_photo(BufferedInputFile(file=image_bytes,filename='result.png'),
                               caption='Ваша картинка \n Выберите задачу',
                               reply_markup=kb.keyboard1)


@router.message(F.text == 'Детекция')
async def detect(message: Message):
    await message.answer('В разработке')

@router.message(StateFilter(None))
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await message.answer('Я вас не понял')