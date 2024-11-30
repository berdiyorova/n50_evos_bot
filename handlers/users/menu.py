from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.user import categories_keyboards, products_keyboards
from keyboards.inline.user import create_cart_keyboard
from loader import dp, _
from utils.db_commands.products import get_categories, get_products


categories = []
products = []


@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def get_categories_handler(message: types.Message, state: FSMContext):
    global categories
    categories = await get_categories()
    data = await state.get_data()
    language = data.get('language')

    await message.answer(text=_("Choose a product category:"),
                         reply_markup=await categories_keyboards(categories, language=language))


@dp.message_handler(lambda message: message.text in categories)
async def get_products_handler(message: types.Message, state: FSMContext):
    global products
    category = message.text
    data = await state.get_data()
    language = data.get('language')

    products = await get_products(category)
    await message.answer(text=f"Products in {category}:",
                         reply_markup=await products_keyboards(products, language=language))


@dp.message_handler(lambda message: message.text in [product['name'] for product in products])
async def select_product_handler(message: types.Message, state: FSMContext):
    await state.finish()
    quantity = 1
    data = await state.get_data()
    language = data.get('language')

    for product in products:
        if product['name'] == message.text:
            await state.update_data(selected_product_id=product['id'],
                                    selected_product_name=product['name'],
                                    selected_product_price=product['price'],
                                    quantity=quantity)
            text = f"{product['name']}\n{product['price']} so'm\n"
            await message.answer(text=text,
                                 reply_markup=await create_cart_keyboard(quantity=quantity, language=language))
