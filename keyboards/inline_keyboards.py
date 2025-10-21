from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_menu_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Выбрать спецтехнику 🚜", callback_data="menu_tech")
    builder.button(text="Управление подписками 📖", callback_data="menu_sub_manage")
    builder.button(text="Выбрать регион 🗺️", callback_data="menu_region")
    builder.button(text="Радиус получения объявлений 📍", callback_data="menu_radius")
    builder.button(text="Написать нам ✏️", callback_data="menu_contact")
    builder.button(text="Помощь ℹ️", callback_data="menu_help")

    builder.adjust(1) 

    return builder.as_markup()