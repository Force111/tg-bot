import os
from typing import Any, Mapping, Optional
from google import genai
from dotenv import load_dotenv
load_dotenv()

import logging

class GeminiService:
    def __init__(self, *, model: Optional[str] = None):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in environment")

        self.client = genai.Client(api_key=api_key)
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

    async def generate_plan(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            logging.error("No prompt line 18 chat api")
            raise ValueError("Prompt is empty")
            

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        text = getattr(response, "text", None)
        if not text:
            raise ValueError("Empty response from Gemini API")

        return text

    @staticmethod
    def _as_str_list(value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, (list, tuple)):
            return [str(x) for x in value if str(x).strip()]
        return [str(value)]

    @staticmethod
    async def build_prompt(day_info: Mapping[str, Any]) -> str:
        reading = day_info.get("reading") or {}
        commands = GeminiService._as_str_list(day_info.get("commands_for_day"))
        tasks = GeminiService._as_str_list(day_info.get("tasks_for_day"))

        commands_text = ", ".join(commands) if commands else "(none)"
        tasks_text = "\n- " + "\n- ".join(tasks) if tasks else "\n- (none)"

        return f"""
You are a Linux mentor.

Create a daily study plan.

Day: {day_info.get("day")}
Topic: {day_info.get("topic")}
Pages: {reading.get("page_start")} - {reading.get("page_end")}
Commands: {commands_text}
Tasks:
-{tasks_text}
Exercise source: {day_info.get("exercise_source")}
Practical case: {day_info.get("practical_case")}

Format:
1. Short theory explanation
2. Commands checklist
3. 3 practical tasks
4. 1 exercise from the source
5. 1 real practical case
6. Completion criteria
""".strip()


   
