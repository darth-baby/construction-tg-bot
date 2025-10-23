from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    return builder.as_markup(resize_keyboard=True)
