from __future__ import annotations

from chat_gpt_api import GeminiService
from Mongo_script import Morning, Mongo_connect

import logging


def main() -> int:
    # 👉 создаём подключение
    client, db = Mongo_connect()

    # 👉 передаём db в класс
    morning = Morning()
    morning.connect(db)

    day_info = morning.morning_script()
    day_info = morning.progress_check(day_info)
    day_info = morning.status_change(day_info)

    print("Result", day_info)

    if not day_info:
        print("No day_info found; skipping Gemini request.")
        logging.error("No day found LINE 25 MAIN")
        client.close()
        return 0

    gpt = GeminiService()
    prompt = gpt.build_prompt(day_info)
    plan = gpt.generate_plan(prompt)

    print("End result:", plan)

    
    client.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())