from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def phone_number_share_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text="Share phone number ☎️", request_contact=True)
        ]], resize_keyboard=True
    )
    return markup
