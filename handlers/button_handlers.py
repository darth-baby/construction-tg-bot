from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline_keyboards import get_menu_tech, get_menu_inline_keyboard

router = Router()


@router.callback_query(F.data == "menu_tech")
async def handle_subscription_manage(callback: CallbackQuery):
    """
    Обрабатывает нажатие на кнопку "Выбор спецтехники".
    """
    if callback.message:
        await callback.message.edit_text(
            "Выберите категорию по которой вы хотите получать объявления",
            reply_markup=get_menu_tech(),
        )
    await callback.answer()


@router.callback_query(F.data == "menu_start")
async def handle_back_to_menu(callback: CallbackQuery):
    """
    Обрабатывает нажатие на кнопку "Назад в меню".
    """
    if callback.message:
        await callback.message.edit_text(
            "Вы вернулись в главное меню",
            reply_markup=get_menu_inline_keyboard(),
        )
    await callback.answer()
