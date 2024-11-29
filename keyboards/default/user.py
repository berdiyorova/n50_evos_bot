from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


async def user_main_menu_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("🍴 Menu"))
            ],
            [
                KeyboardButton(text=_("🛍 My orders"))
            ],
            [
                KeyboardButton(text=_("✍️ Leave feedback")),
                KeyboardButton(text=_("⚙️ Settings")),
            ]
        ], resize_keyboard=True
    )

    return markup


async def user_address_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("🗺 My addresses"))
            ],
            [
                KeyboardButton(text=_("📍 Submit geolocation"), request_location=True),
                KeyboardButton(text=_("⬅️ Back")),
            ]
        ], resize_keyboard=True
    )

    return markup


async def set_language():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Set language settings"))
            ],
            [
                KeyboardButton(text=_("⬅️ Back"))
            ]
        ], resize_keyboard=True
    )

    return markup


async def my_address_keyboards(addresses):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for address in addresses:
        markup.add(KeyboardButton(text=address['name']))
    markup.add(KeyboardButton(text=_("⬅️ Back")))
    return markup


async def categories_keyboards(categories):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    temp_category = list()

    for cat in categories:
        temp_category.append(cat)
        if len(temp_category) == 2:
            markup.add(
                KeyboardButton(text=temp_category[0]),
                KeyboardButton(text=temp_category[1])
            )
            temp_category.clear()

    if temp_category:
        markup.add(KeyboardButton(text=temp_category[0]))

    markup.add(KeyboardButton(text=_("⬅️ Back")))
    return markup


async def products_keyboards(products):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    temp_product = list()

    for product in products:
        temp_product.append(product)
        if len(temp_product) == 2:
            markup.add(
                KeyboardButton(text=temp_product[0]['name']),
                KeyboardButton(text=temp_product[1]['name'])
            )
            temp_product.clear()

    if temp_product:
        markup.add(KeyboardButton(text=temp_product[0]['name']))

    markup.add(KeyboardButton(text=_("⬅️ Back")))
    return markup


async def payment_method_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Cash"))
            ],
            [
                KeyboardButton(text="Click")
            ],
            [
                KeyboardButton(text="Payme")
            ],
            [
                KeyboardButton(text=_("⬅️ Back"))
            ]
        ], resize_keyboard=True
    )

    return markup
