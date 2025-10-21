from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.inline_keyboards import get_menu_inline_keyboard
router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    inline_kb = get_menu_inline_keyboard()
    await message.answer("""Привет! Я бот Строитель! 🚜

Здесь вы сможете получать заказы на спецтехнику, объявления об отвалах и продаже нерудки по подписке. Бот работает по Москве и МО.

Как работает бот:
1. Нажмите на кнопку Выбрать спецтехнику
2. Выберите спецтехнику, на которую хотите получать заказы и нажмите на нее

Готово! Теперь вы будете получать заказы на выбранную спецтехнику.
Когда закончатся бесплатные просмотры номеров телефонов - бот сам предложит вам оформить платную подписку. Просто следуйте инструкции.
""",
reply_markup=inline_kb)


@router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.answer("Введите команду /help если потерялись.")
    except TypeError:
        await message.answer("Введите команду /help если потерялись.")