from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def user_main_menu_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🍴 Menu")
            ],
            [
                KeyboardButton(text="🛍 My orders")
            ],
            [
                KeyboardButton(text="✍️ Leave feedback"),
                KeyboardButton(text="⚙️ Settings"),
            ]
        ], resize_keyboard=True
    )

    return markup


async def user_address_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🗺 My address")
            ],
            [
                KeyboardButton(text="📍 Submit geolocation"),
                KeyboardButton(text="⬅️ Back"),
            ]
        ], resize_keyboard=True
    )

    return markup


async def set_language_settings():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Set language settings")
            ],
            [
                KeyboardButton(text="⬅️ Back")
            ]
        ], resize_keyboard=True
    )

    return markup


async def my_address_keyboards(addresses):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text=f"address name",
                callback_data=f"name")
            ] for address in addresses
        ]
    )

    return markup
