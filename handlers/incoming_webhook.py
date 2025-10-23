# Файл: handlers/incoming_webhooks.py

from aiohttp import web
import json
from aiogram import Bot

router = web.RouteTableDef()


@router.post("/incoming")
async def handle_webhook(request: web.Request):
    """
    Обрабатывает входящие POST-запросы от парсера WhatsApp.
    """
    bot: Bot = request.app["bot"]

    try:
        data = await request.json()
        print(f"✅ Получен webhook от парсера: {data}")

        wa_chat_id = data.get("wa_chat_id")
        wa_body = data.get("wa_body")

        response_data = {"status": "success", "message": "data received"}
        return web.json_response(response_data, status=200)

    except json.JSONDecodeError:
        error_response = {"status": "error", "message": "Invalid JSON"}
        return web.json_response(error_response, status=400)
    except Exception as e:
        print(f"❌ Ошибка в обработчике webhook: {e}")
        error_response = {"status": "error", "message": "Internal server error"}
        return web.json_response(error_response, status=500)
