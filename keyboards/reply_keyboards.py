from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()


    builder.button(text="Выбрать спецтехнику 🚜")
    builder.button(text="Выбрать нерудку ⛰️")
    builder.button(text="Выбрать отвал ⛺")
    builder.button(text="Выставить заказ ⚒️")
    builder.button(text="Подписка навсегда 🔥")
    builder.button(text="Управление подписками 📖")
    builder.button(text="Выбрать регион 🗺️")
    builder.button(text="Радиус получения объявлений 📍")
    builder.button(text="Написать нам ✏️")
    builder.button(text="Как оплатить? 💵")
    builder.button(text="Помощь ℹ️")
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)