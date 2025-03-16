from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup

keyboard_main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Генерация ✏️"),
            KeyboardButton(text="Детекция 🤖"),
        ],
        [KeyboardButton(text="Помощь проекту 🗃️")],
    ]
)

keyboard_image = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Реальное 📸", callback_data="real")],
        [InlineKeyboardButton(text="Аи 🤖", callback_data="ai")],
    ]
)
