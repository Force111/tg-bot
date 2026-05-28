from aiogram.utils.keyboard import ReplyKeyboardBuilder,ReplyKeyboardMarkup

def tasks_menu_buttons():
    builder = ReplyKeyboardBuilder()

    builder.button(text = "Send Task!")
    builder.button(text = "My Task!")
    builder.button(text = "Get some help!")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard = True)

    