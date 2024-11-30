from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _
from aiogram.dispatcher import FSMContext

from utils.get_language import get_lang_by_text


async def user_main_menu_keyboard(language: str):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("🍴 Menu", locale=language))
            ],
            [
                KeyboardButton(text=_("🛍 My orders", locale=language))
            ],
            [
                KeyboardButton(text=_("✍️ Leave feedback", locale=language)),
                KeyboardButton(text=_("⚙️ Settings", locale=language)),
            ]
        ], resize_keyboard=True
    )

    return markup


async def user_address_keyboard(language: str):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("🗺 My addresses", locale=language))
            ],
            [
                KeyboardButton(text=_("📍 Submit geolocation", locale=language), request_location=True),
                KeyboardButton(text=_("⬅️ Back", locale=language)),
            ]
        ], resize_keyboard=True
    )

    return markup


async def set_language(language: str):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Set language settings", locale=language))
            ],
            [
                KeyboardButton(text=_("⬅️ Back", locale=language))
            ]
        ], resize_keyboard=True
    )

    return markup


async def my_address_keyboards(addresses, language: str):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for address in addresses:
        markup.add(KeyboardButton(text=address['name']))
    markup.add(KeyboardButton(text=_("⬅️ Back", locale=language)))
    return markup


async def categories_keyboards(categories, language: str):
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

    markup.add(KeyboardButton(text=_("⬅️ Back", locale=language)))
    return markup


async def products_keyboards(products, language: str):
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

    markup.add(KeyboardButton(text=_("⬅️ Back", locale=language)))
    return markup


async def payment_method_keyboard(language: str):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Cash", locale=language))
            ],
            [
                KeyboardButton(text="Click", locale=language)
            ],
            [
                KeyboardButton(text="Payme", locale=language)
            ],
            [
                KeyboardButton(text=_("⬅️ Back", locale=language))
            ]
        ], resize_keyboard=True
    )

    return markup
