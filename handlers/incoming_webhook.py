from aiohttp import web
import json
import logging
from aiogram import Bot

from services.database import db
from keyboards.buttons_data import TECH_BUTTONS_DATA
from services.hybrid_category_detector import detect_category

router = web.RouteTableDef()


@router.post("/incoming")
async def handle_webhook(request: web.Request):
    """
    Принимает данные от парсера WhatsApp и самостоятельно определяет категорию техники.
    После этого рассылает сообщение всем подписчикам этой категории.
    """
    bot: Bot = request.app["bot"]

    try:
        data = await request.json()
        logging.info(f"✅ Получен webhook от парсера: {data}")

        message_text = data.get("wa_body", "")
        author = data.get("wa_author", "Неизвестно")

        # --- 1️⃣ Определяем категорию ---
        category_callback = detect_category(message_text)
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

        message_text_formatted = (
            f"📢 **Новое объявление по подписке «{tech_name}»**\n\n"
            f"👤 **Автор:** {author}\n"
            f"📝 **Текст:**\n{message_text}"
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
