import asyncio
import aiogram
from aiogram import Router,types,F,Bot
from aiogram.client import bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging

from telegram_bot.buttons.buttons_main import BTN_HELP,BTN_PROGRESS,BTN_TODAY_TASK, get_main_menu 


from buttons_workload import TaskService



class Handling_buttons_main:


    
    def __init__(self):
        self.task_service = TaskService
        router = Router(name ="handling_main")
        self.handling_button()
    
    def handling_button(self) -> None:
        self.router.message.register(self.handle_progress,
        F.text == BTN_PROGRESS
        )
        self.router.message.register(self.handle_day_progress,
        F.text == BTN_TODAY_TASK
        )
        self.router.message.register(self.handle_help,
        F.text == BTN_HELP
        )

    async def handle_progress(self,message:Message):
            progress = self.task_service.progress_tasks()

            if progress is None:
                logging.error("No progress was found")
                return None

            await message.answer(f"Here is your progress: {progress}")
            


    async def handle_help(self,message:Message):
            #message = message.from_user.id
            help_ticket = self.task_service.helping_workload()

            if help_ticket is None:
                logging.error("No help ticket was found or sent")
                return None
            
            bot.message.send_copy(message:Message,ADMIN_ID)
            

           

            