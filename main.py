import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
from handlers import common, button_handlers, subscription_settings, tech_selection
from handlers.incoming_webhook import router as webhook_router
from services.database import db
from keyboards.buttons_data import TECH_BUTTONS_DATA


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(common.router)
dp.include_router(button_handlers.router)
dp.include_router(tech_selection.router)


async def main() -> None:
    if BOT_TOKEN is None:
        logging.error("BOT_TOKEN is not found. Check your .env file.")
        sys.exit(1)

    db.setup()
    db.populate_tech_categories(TECH_BUTTONS_DATA)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    app = web.Application()

    app.add_routes(webhook_router)

    app["bot"] = bot

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    logging.info("======== aiohttp server is running on http://0.0.0.0:8080 ========")

    try:
        logging.info("======== Starting aiogram polling ========")
        await dp.start_polling(bot)
    finally:
        logging.info("======== Shutting down aiohttp server ========")
        await runner.cleanup()
        logging.info("======== Shutting down bot session ========")
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
