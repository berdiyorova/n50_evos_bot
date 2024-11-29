from decimal import Decimal

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.user import categories_keyboards, products_keyboards, payment_method_keyboard, \
    user_main_menu_keyboard
from keyboards.inline.user import create_cart_keyboard, place_order
from loader import dp, _
from utils.db_commands.orders import add_product_to_cart, get_cart, add_order, update_order
from utils.db_commands.products import get_categories, get_products, get_product

categories = []
products = []
delivery = Decimal("12000")

@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def get_categories_handler(message: types.Message, state: FSMContext):
    global categories
    categories = await get_categories()

    await message.answer(text=_("Choose a product category:"),
                         reply_markup=await categories_keyboards(categories))


@dp.message_handler(lambda message: message.text in categories)
async def get_products_handler(message: types.Message, state: FSMContext):
    global products
    category = message.text
    products = await get_products(category)
    await message.answer(text=_(f"Products in {category}:"),
                         reply_markup=await products_keyboards(products))


@dp.message_handler(lambda message: message.text in [product['name'] for product in products])
async def select_product_handler(message: types.Message, state: FSMContext):
    await state.finish()
    quantity = 1
    for product in products:
        if product['name'] == message.text:
            await state.update_data(selected_product_id=product['id'],
                                    selected_product_name=product['name'],
                                    selected_product_price=product['price'],
                                    quantity=quantity)
            text = f"{product['name']}\n{product['price']} so'm\n"
            await message.answer(text=text, reply_markup=await create_cart_keyboard(quantity=quantity))


@dp.callback_query_handler(lambda call: call.data == 'decrease')
async def decrease_quantity_handler(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    product_id = user_data.get('selected_product_id')
    product_name = user_data.get('selected_product_name')
    product_price = user_data.get('selected_product_price')
    quantity = user_data.get('quantity', 1)

    if product_id and product_name:
        if quantity > 1:
            quantity -= 1
            await state.update_data(quantity=quantity)

            text = f"{product_name}\n{product_price} so'm\n"
            await call.message.edit_text(text=text, reply_markup=await create_cart_keyboard(quantity=quantity))
            await call.answer("Quantity decreased!")


@dp.callback_query_handler(lambda call: call.data == 'increase')
async def increase_quantity_handler(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    product_id = user_data.get('selected_product_id')
    product_name = user_data.get('selected_product_name')
    product_price = user_data.get('selected_product_price')
    quantity = user_data.get('quantity', 1)

    if product_id and product_name:
        quantity += 1
        await state.update_data(quantity=quantity)

        text = f"{product_name}\n{product_price} so'm\n"
        await call.message.edit_text(text=text, reply_markup=await create_cart_keyboard(quantity=quantity))
        await call.answer("Quantity increased!")


@dp.callback_query_handler(lambda call: call.data == 'add_to_cart')
async def add_product_to_cart_handler(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    product_id = user_data.get('selected_product_id')
    product_name = user_data.get('selected_product_name')
    quantity = user_data.get('quantity', 1)

    if product_name:
        cart_id = await add_product_to_cart(message=call.message, product_id=product_id, quantity=quantity)
        if cart_id:
            cart = await get_cart(cart_id=cart_id)
            product_id = cart.get('product_id')
            product = await get_product(product_id=product_id)
            quantity = cart.get('quantity')

            await state.update_data(cart_id=cart_id)

            text = (f"{product.get('name')}\n"
                    f"Quantity: {quantity}\n"
                    f"Products: {quantity * product.get('price')} so'm\n\n"
                    f"Delivery: {delivery} so'm\n"
                    f"Total: {quantity * product.get('price') + delivery}")

            await call.answer(f"Added {quantity} of {product_name} to cart!")
            await call.message.answer(text=text, reply_markup=place_order)


@dp.callback_query_handler(lambda call: call.data == 'oder')
async def place_an_order(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    cart_id = user_data.get('cart_id')
    cart = await get_cart(cart_id=cart_id)

    if cart:
        product_id = cart.get('product_id')
        product = await get_product(product_id=product_id)

        product_name = product.get('name')
        product_price = product.get('price')
        quantity = cart.get('quantity')
        user_id = cart.get('user_id')
        total_price = quantity * product_price + delivery

        order_id = await add_order(
            product_name=product_name,
            product_price=product_price,
            quantity=quantity,
            total_price=total_price,
            user_id=user_id)

        await state.update_data(order_id=order_id)

        await call.message.answer(
            text=_("Please, select a payment method:"),
            reply_markup=await payment_method_keyboard())


@dp.message_handler(lambda message: message.text in ["Cash", "Naqd to'lov"])
async def cash_payment_handler(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    order_id = user_data.get('order_id')

    if order_id:
        await update_order(order_id=order_id, status=True)
        await message.answer(text=_("Order received😊. We will deliver soon.🚚"),
                             reply_markup=await user_main_menu_keyboard())


@dp.message_handler(lambda message: message.text in ["Click", "Payme"])
async def cash_payment_handler(message: types.Message, state: FSMContext):
    await message.answer(text=_("Not working"))

