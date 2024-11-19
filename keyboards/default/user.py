from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def user_main_menu_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Menu")
            ],
            [
                KeyboardButton(text="My orders"),
                KeyboardButton(text="Our branches"),
            ],
            [
                KeyboardButton(text="Contact"),
                KeyboardButton(text="Settings"),
            ]
        ], resize_keyboard=True
    )

    return markup
