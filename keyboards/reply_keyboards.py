# Файл: keyboards/reply_keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_reply_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает Reply-клавиатуру с кнопкой "Главное меню".
    """
    # Создаем кнопку
    main_menu_button = KeyboardButton(text="Главное меню 🎯")

    # Создаем клавиатуру, добавляем кнопку и настраиваем ее
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[main_menu_button]],  # Список списков для рядов кнопок
        resize_keyboard=True,  # Делает клавиатуру компактной
        one_time_keyboard=False,  # Клавиатура не будет скрываться после нажатия
        input_field_placeholder="Нажмите 'Главное меню' для навигации...",  # Текст в поле ввода
    )

    return keyboard
