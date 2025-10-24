from aiohttp import web
import json
import logging
from aiogram import Bot
import os
import secrets
from dotenv import load_dotenv
from services.database import db
from keyboards.buttons_data import TECH_BUTTONS_DATA
from services.hybrid_category_detector import detect_category
import datetime
from aiogram.utils.markdown import hbold, hitalic

router = web.RouteTableDef()

load_dotenv()
SECRET_TOKEN_SERVER = os.getenv("INCOMING_WEBHOOK_TOKEN")


@router.post("/incoming")
async def handle_webhook(request: web.Request):
    """
    Принимает данные от парсера WhatsApp, проверяет токен и рассылает сообщения.
    """
    bot: Bot = request.app["bot"]
    if SECRET_TOKEN_SERVER:
        auth_header = request.headers.get("Authorization")

        # 1. Проверяем наличие заголовка
        if not auth_header:
            logging.warning("Запрос без заголовка Authorization.")
            return web.json_response(
                {"status": "error", "message": "Authorization header missing"},
                status=401,
            )

        # 2. Проверяем формат заголовка (должен быть "Bearer <token>")
        try:
            auth_type, token = auth_header.split(" ", 1)
            if auth_type.lower() != "bearer":
                raise ValueError("Invalid authorization type")
        except ValueError:
            logging.warning(f"Неверный формат заголовка Authorization: {auth_header}")
            return web.json_response(
                {"status": "error", "message": "Invalid Authorization header format"},
                status=401,
            )

        # 3. Сравниваем токен (безопасным способом, чтобы избежать атак по времени)
        if not secrets.compare_digest(token, SECRET_TOKEN_SERVER):
            logging.warning("Получен неверный токен.")
            return web.json_response(
                {"status": "error", "message": "Forbidden: Invalid token"}, status=403
            )

        logging.info("✅ Токен успешно верифицирован.")

    try:
        data = await request.json()
        logging.info(f"✅ Получен webhook от парсера: {data}")

        message_text = data.get("wa_body", "")
        author = data.get("wa_author", "Неизвестно")

        text_for_model = message_text.replace('\n', ' ')
        category_callback = detect_category(text_for_model)
        if not category_callback:
            logging.info("⚠️ Категория не определена — сообщение пропущено.")
            return web.json_response(
                {"status": "ok", "message": "no category detected"}, status=200
            )

        # --- 2️⃣ Находим подписчиков ---
        subscribers = db.get_subscribers_for_category(category_callback)
        if not subscribers:
            logging.info(
                f"Подписчики на категорию {category_callback} не найдены. Рассылка не требуется."
            )
            return web.json_response(
                {"status": "ok", "message": "no subscribers found"}, status=200
            )

        tech_name = next(
            (name for name, cb in TECH_BUTTONS_DATA if cb == category_callback),
            "Спецтехника",
        )

        tstamp = data.get("timestamp")
        if tstamp:
            dt_str = datetime.datetime.fromtimestamp(tstamp).strftime(
                "%d.%m.%Y в %H:%M"
            )
        else:
            dt_str = "не указано"

        message_text_formatted = (
            f"📢 {hbold(f'Новое объявление по подписке «{tech_name}»')}\n\n"
            f"👤 {hbold('Номер:')} {author}\n"
            f"📝 {hbold('Текст:')}\n{message_text}\n\n"  # Добавили отступы
            f"🕓 {hbold('Время:')} {dt_str}\n\n"
            f"❗️ {hitalic('Чем больше времени прошло с момента появления объявления, тем больше вероятность, что оно уже не актуально.')}"
        )

        # --- 3️⃣ Рассылаем подписчикам ---
        logging.info(
            f"Начинаю рассылку {len(subscribers)} пользователям по категории {category_callback}..."
        )

        successful_sends = 0
        for user_id in subscribers:
            try:
                await bot.send_message(user_id, message_text_formatted)
                successful_sends += 1
            except Exception as e:
                logging.error(
                    f"Не удалось отправить сообщение пользователю {user_id}: {e}"
                )

        logging.info(
            f"Рассылка завершена. Успешно отправлено: {successful_sends}/{len(subscribers)}"
        )

        return web.json_response(
            {
                "status": "success",
                "message": f"sent to {successful_sends} users",
                "category": category_callback,
            }
        )

    except json.JSONDecodeError:
        return web.json_response(
            {"status": "error", "message": "Invalid JSON"}, status=400
        )
    except Exception as e:
        logging.error(f"❌ Критическая ошибка в обработчике webhook: {e}")
        return web.json_response(
            {"status": "error", "message": "Internal server error"}, status=500
        )
