# Файл: handlers/feedback.py
from dotenv import load_dotenv
import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .states import FeedbackStates  # Импортируем наши состояния

router = Router()

load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")


# --- Клавиатура для отмены ---
def get_cancel_feedback_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Отменить", callback_data="cancel_feedback")
    return builder.as_markup()


# --- 1. Вход в режим обратной связи ---
@router.callback_query(F.data == "menu_contact")
async def start_feedback(callback: CallbackQuery, state: FSMContext):
    if not ADMIN_ID:
        await callback.answer(
            "Функция обратной связи временно недоступна.", show_alert=True
        )
        return

    await state.set_state(FeedbackStates.WaitingForFeedback)
    await callback.message.answer(
        "Напишите ваше сообщение для администратора. Оно будет передано ему напрямую.",
        reply_markup=get_cancel_feedback_keyboard(),
    )
    await callback.answer()


# --- 2. Обработка сообщения от пользователя и пересылка админу ---
@router.message(FeedbackStates.WaitingForFeedback)
async def process_feedback(message: Message, state: FSMContext, bot):
    # Проверяем, что ID админа задан
    if not ADMIN_ID:
        await message.answer(
            "К сожалению, не удалось отправить сообщение. Попробуйте позже."
        )
        await state.clear()
        return

    # Формируем информационное сообщение для админа
    user_info = (
        f"Новое сообщение от пользователя: {message.from_user.full_name}\n"
        f"Username: @{message.from_user.username}\n"
        f"User ID: `{message.from_user.id}`"
    )

    # Сначала отправляем админу информацию о том, кто пишет
    await bot.send_message(chat_id=ADMIN_ID, text=user_info, parse_mode="MarkdownV2")

    # Затем пересылаем оригинальное сообщение пользователя
    # forward_message сохраняет ссылку на отправителя, позволяя админу ответить
    await bot.forward_message(
        chat_id=ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id
    )

    # Сообщаем пользователю об успехе и выходим из состояния
    await message.answer("Спасибо! Ваше сообщение отправлено администратору.")
    await state.clear()


# --- 3. Обработка отмены ---
@router.callback_query(F.data == "cancel_feedback", FeedbackStates.WaitingForFeedback)
async def cancel_feedback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Действие отменено.")
    await callback.answer()
