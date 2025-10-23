# Файл: handlers/subscriptions.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.database import db  # <-- Импортируем нашу базу

# Создаем роутер для этого модуля
router = Router()

# --- Обработчики ---


@router.callback_query(F.data == "menu_sub_manage")
async def handle_subscription_manage(callback: CallbackQuery):
    """
    Обрабатывает нажатие на "Управление подписками".
    Динамически создает клавиатуру с активными подписками пользователя.
    """
    user_id = callback.from_user.id
    active_subs = db.get_user_active_subscriptions(user_id)

    builder = InlineKeyboardBuilder()

    # Создаем кнопки для каждой активной подписки
    if active_subs:
        text = "Ваши активные подписки. Нажмите на подписку, чтобы отменить ее:"
        for sub_name, sub_callback in active_subs:
            # Создаем новый callback для отмены, например, "unsubscribe:tech:autocrane"
            unsubscribe_callback = f"unsubscribe:{sub_callback}"
            builder.button(text=f"❌ {sub_name}", callback_data=unsubscribe_callback)
    else:
        text = "У вас пока нет активных подписок."
        # Можно добавить кнопку для перехода к выбору техники
        builder.button(text="➕ Выбрать технику", callback_data="menu_tech")

    # Добавляем кнопку "Назад в меню"
    builder.button(text="⬅️ Назад в меню", callback_data="menu_start")

    # Выстраиваем кнопки в один столбец
    builder.adjust(1)

    # Проверяем, что сообщение доступно для редактирования
    if isinstance(callback.message, Message):
        await callback.message.edit_text(text, reply_markup=builder.as_markup())

    await callback.answer()


@router.callback_query(F.data.startswith("unsubscribe:"))
async def handle_unsubscribe(callback: CallbackQuery):
    """
    Обрабатывает отмену подписки.
    """
    user_id = callback.from_user.id
    # Вытаскиваем оригинальный callback категории: "tech:autocrane"
    category_callback = callback.data.split(":", 1)[1]

    # Удаляем подписку из БД
    success = db.remove_subscription(user_id, category_callback)

    if success:
        await callback.answer("Подписка успешно отменена!", show_alert=True)
        # После отмены нужно обновить сообщение со списком подписок.
        # Для этого мы просто "вызываем" предыдущий хендлер заново.
        await handle_subscription_manage(callback)
    else:
        await callback.answer("Произошла ошибка при отмене подписки.", show_alert=True)
