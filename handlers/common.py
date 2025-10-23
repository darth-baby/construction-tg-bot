from aiogram import Router, F
from aiogram.filters import CommandStart, or_f
from aiogram.types import Message
from keyboards.inline_keyboards import get_menu_inline_keyboard
from keyboards.reply_keyboards import get_main_menu_reply_keyboard

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    reply_kb = get_main_menu_reply_keyboard()
    start_text = (
        f"Привет, {message.from_user.first_name}! Я бот Строитель! 🚜\n\n"
        "Здесь вы сможете получать заказы на спецтехнику, объявления об отвалах и продаже нерудки по подписке. Бот работает по Москве и МО.\n\n"
        """Как работает бот:
1. Нажмите на кнопку Выбрать спецтехнику
2. Выберите спецтехнику, на которую хотите получать заказы и нажмите на нее

Готово! Теперь вы будете получать заказы на выбранную спецтехнику."""
    )

    await message.answer(start_text, reply_markup=reply_kb)


@router.message(F.text == "Главное меню 🎯")
async def command_go_to_menu_handler(message: Message) -> None:
    inline_kb = get_menu_inline_keyboard()
    start_text = """Добро пожаловать в Главное Меню!🚜
    Кнопки:
⏺️Выбрать спецтехнику - Выбор спецтехники, на которую необходимо получать заказы
⏺️Управление подписками - Информация по текущим подпискам
⏺️Радиус получения объявлений - Настройка для получения заявок только в нужном вам районе
⏺️Написать нам - Обращение в поддержку, если у вас возникли вопросы 
⏺️Помощь - Информация по работе бота и стоимости подписки"""

    await message.answer(start_text, reply_markup=inline_kb)


@router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.answer("Введите команду /start если потерялись.")
    except TypeError:
        await message.answer("Введите команду /start если потерялись.")
