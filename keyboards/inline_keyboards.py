from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .buttons_data import TECH_BUTTONS_DATA


def get_menu_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Выбрать спецтехнику 🚜", callback_data="menu_tech")
    builder.button(text="Управление подписками 📖", callback_data="menu_sub_manage")
    builder.button(text="Радиус получения объявлений 📍", callback_data="menu_radius")
    builder.button(text="Написать нам ✏️", callback_data="menu_contact")
    builder.button(text="Помощь ℹ️", callback_data="menu_help")

    builder.adjust(1)

    return builder.as_markup()


def get_menu_tech() -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру для выбора категории спецтехники.
    """
    builder = InlineKeyboardBuilder()

    for text, callback_data in TECH_BUTTONS_DATA:
        builder.button(text=text, callback_data=callback_data)

    builder.adjust(2)

    builder.row(InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="menu_start"))

    return builder.as_markup()
