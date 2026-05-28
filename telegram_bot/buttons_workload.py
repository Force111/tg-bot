# telegram_bot/services/task_service.py

from os import getenv

from aiogram import Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from Mongo_script import Morning
from chat_gpt_api import GeminiService

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class TaskService:
    def __init__(self, db) -> None:
        self.morning = Morning()
        if db is not None:
            self.morning.connect(db)

        self.gpt = GeminiService()

    async def get_today_task(self) -> str | None:
        day_info = self.morning.morning_script()
        day_info = self.morning.progress_check(day_info)
        day_info = self.morning.status_change(day_info)

        if not day_info:
            logging.error("No day info found line 29 BWL.py")
            return None
            

        prompt = self.gpt.build_prompt(day_info)
        task_text = await self.gpt.generate_plan(prompt)

        return task_text
    
    def progress_tasks(self) -> str | None:
        total_days = self.morning.collection.count_documents({})
        current_day = self.morning.collection.find_one({"status":"in_progress"})
        day_count = self.morning.collection.count_documents({"status":"done"})


        if total_days == 0:
            print("no days found workload 33l")
            logging.error("No days were found LINE 33")
            return "No days were found"
        else:
            print("Day number",current_day)
        
        if current_day:
            current_day_number = current_day.get("day", "unknown")
            current_topic = current_day.get("topic", "unknown topic")
        else:
            current_day_number = "no active day"
            current_topic = "no active topic"
            logging.error("There is no active day LINE 38 BWL.py")
            

        return (
            f"Progress: {current_day}/{total_days}"
            f"Current day is: {current_day}"
            f"Today's topic: {current_topic}"
        )
        
            
    
    class Help(StatesGroup):
        #help_day = State()
        #extra_field = State()
        waiting_for_assistance = State() #Создаем статус для опроса юзера


    async def helping_workload(self, bot: Bot, message:Message):
        
        ADMIN_ID = getenv("ADMIN_ID")

        if not ADMIN_ID: 
            logging.error("No admin id")
            return False

        user = message.from_user

        user_report_text = message.text or message.caption or "user failed to make a correct report FALLBACK!"

        report_text = (
            "NEW REPORT TICKET ALERT \n\n"
            f"user id: {user.id}\n"
            f"Username: @{user.username}\n"
            f"Full name: {user.full_name}\n"
            f"Problem: {user_report_text}\n" 

        )
        
        await bot.send_message(chat_id = int(ADMIN_ID),text = report_text)

        await message.send_copy(chat_id = int(ADMIN_ID))

        print("The message was sent succesfully")




