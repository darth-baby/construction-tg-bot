from aiogram import Router, F
from aiogram.types import CallbackQuery

from services.database import db  # Импортируем наш объект БД
from keyboards.buttons_data import (
    TECH_BUTTONS_DATA,
)  # Импортируем список для поиска имени

router = Router()


@router.callback_query(F.data.startswith("tech:"))
async def handle_tech_selection(callback: CallbackQuery):
    """Обрабатывает нажатие на кнопку с выбором техники."""
    user = callback.from_user
    category_callback = callback.data

    # 1. Добавляем пользователя в БД (безопасно, т.к. INSERT OR IGNORE)
    db.add_user(user_id=user.id, username=user.username, first_name=user.first_name)

    # 2. Добавляем подписку
    success = db.add_or_update_subscription(
        user_id=user.id, category_callback=category_callback
    )

    # 3. Отвечаем пользователю
    if success:
        # Ищем понятное имя техники для ответа пользователю
        tech_name = next(
            (name for name, cb in TECH_BUTTONS_DATA if cb == category_callback),
            "Неизвестная техника",
        )

        await callback.answer(
            f"✅ Вы подписались на категорию: «{tech_name}»", show_alert=True
        )
    else:
        await callback.answer(
            "❌ Произошла ошибка при оформлении подписки. Попробуйте позже.",
            show_alert=True,
        )
