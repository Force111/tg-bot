import asyncio
import logging
from os import getenv
from pathlib import Path
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Mongo_script import Mongo_connect
from telegram_bot.buttons_workload import TaskService
from telegram_bot.handlers.handler_main import Handling_buttons_main
from telegram_bot.handlers.handler_start import router as start_router


load_dotenv()
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

TOKEN = getenv("TELEGRAM_KEY")


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    if not TOKEN:
        raise RuntimeError("TELEGRAM_KEY is not set in environment")

    client, db = Mongo_connect()

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    task_service = TaskService(db=db)
    Handling_buttons_main(task_service=task_service)

    dp.include_router(start_router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("Telegram bot polling started")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        client.close()


if __name__ == "__main__":
    asyncio.run(main())
