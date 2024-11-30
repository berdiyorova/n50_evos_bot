from loader import _

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
            InlineKeyboardButton(text=_("🇺🇿 Uzbek"), callback_data='uz'),
            InlineKeyboardButton(text=_("󠁧󠁢󠁥󠁮󠁧󠁿🇷🇺 Russian"), callback_data='ru'),
            InlineKeyboardButton(text=_("🏴 English"), callback_data='en')
)


async def create_cart_keyboard(quantity, language: str):
    markup = InlineKeyboardMarkup()

    row1 = [
        InlineKeyboardButton(text="-", callback_data="decrease"),
        InlineKeyboardButton(text=str(quantity), callback_data="quantity"),
        InlineKeyboardButton(text="+", callback_data="increase")
    ]
    row2 = [
        InlineKeyboardButton(text=_("🛒 Add to cart", locale=language), callback_data="add_to_cart")
    ]

    markup.add(*row1)
    markup.add(*row2)
    return markup


async def place_order(language: str):
    InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(
        text=_("Place order", locale=language), callback_data="oder"))
