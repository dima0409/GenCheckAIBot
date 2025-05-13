from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


# Основная клавиатура ас reply-кнопками
keyboard_main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Генерация ✏️"),
            KeyboardButton(text="Детекция 🤖"),
        ],
        [KeyboardButton(text="Помощь проекту 🗃️")],
    ],
)

# Инлайн-клавиатура для загрузки изображений
keyboard_image = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Реальное 📸", callback_data="real")],
        [InlineKeyboardButton(text="Аи 🤖", callback_data="ai")],
    ],
)
