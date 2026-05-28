from aiogram.utils.keyboard import ReplyKeyboardBuilder

BTN_TODAY_TASK = "📚 Сегодняшнее задание"
BTN_PROGRESS = "📈 Мой прогресс"
BTN_HELP = "❓ Помощь"


def get_main_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text=BTN_TODAY_TASK)
    builder.button(text=BTN_PROGRESS)
    builder.button(text=BTN_HELP)

    builder.adjust(2)

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выбери действие"
    )