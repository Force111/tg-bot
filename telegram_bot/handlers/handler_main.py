from aiogram import F, Router
from aiogram.types import Message
import logging

from telegram_bot.buttons.buttons_main import BTN_HELP, BTN_PROGRESS, BTN_TODAY_TASK

from telegram_bot.buttons_workload import TaskService


router = Router(name="handling_main")


class Handling_buttons_main:
    def __init__(self, task_service: TaskService | None = None):
        self.task_service = task_service or TaskService()
        self.router = router
        self.handling_button()

    def handling_button(self) -> None:
        self.router.message.register(
            self.handle_progress,
            F.text == BTN_PROGRESS,
        )
        self.router.message.register(
            self.handle_todays_task,
            F.text == BTN_TODAY_TASK,
        )
        self.router.message.register(
            self.handle_help,
            F.text == BTN_HELP,
        )

    async def handle_progress(self, message: Message):
        progress = self.task_service.progress_tasks()

        if progress is None:
            logging.error("No progress was found")
            await message.answer("Progress is not available right now.")
            return

        await message.answer(f"Here is your progress: {progress}")

    async def handle_help(self, message: Message):
        help_ticket = await self.task_service.helping_workload(message.bot, message)

        if not help_ticket:
            logging.error("No help ticket was found or sent")
            await message.answer("Help request could not be sent right now.")
            return

        await message.answer("Help request was sent.")

    async def handle_todays_task(self, message: Message):
        today_task = await self.task_service.get_today_task()

        if today_task is None:
            logging.error("No task day was found")
            await message.answer("Today's task is not available right now.")
            return

        await message.answer(f"Today's task is: {today_task}")
