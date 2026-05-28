import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from telegram_bot.buttons.buttons_main import get_main_menu
from telegram_bot.handlers.handler_main import router as main_menu_router

KEY = getenv("TELEGRAM_KEY")

router = Router()
router.include_router(main_menu_router)

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {message.from_user.full_name}!",
        reply_markup=get_main_menu(),
    )

@router.message() 
async def echo_handler(message: Message) -> None:
    await message.send_copy(chat_id=message.chat.id)
    await message.answer("Do not spam!")



