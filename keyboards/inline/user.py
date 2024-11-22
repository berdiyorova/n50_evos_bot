from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

test_callback_data = CallbackData("general_button", "action", "product_id")

#
# async def test_callback_keyboard():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="Button1",
#                                      callback_data=test_callback_data.new(
#                                          action="general_button", product_id=1
#                                      )),
#                 InlineKeyboardButton(text="Button2",
#                                      callback_data=test_callback_data.new(
#                                          action="general_button", product_id=2
#                                      )),
#                 InlineKeyboardButton(text="Button3",
#                                      callback_data=test_callback_data.new(
#                                          action="general_button", product_id=3
#                                      )),
#             ]
#         ]
#     )
#     return markup

languages = InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton(text="🇺🇿 Uzbek", callback_data='uz'),
            InlineKeyboardButton(text="🏴󠁧󠁢󠁥󠁮󠁧󠁿 Russian", callback_data='ru'),
            InlineKeyboardButton(text="🇷🇺 English", callback_data='en')
)
