from decimal import Decimal

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import select_section
from keyboards.default.user import payment_method_keyboard, user_main_menu_keyboard
from keyboards.inline.user import create_cart_keyboard, place_order
from loader import dp, _
from utils.db_commands.orders import get_my_orders, add_product_to_cart, get_cart, add_order, update_order
from utils.db_commands.products import get_product
from utils.db_commands.user import get_user


delivery = Decimal("12000")


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
            data = await state.get_data()
            language = data.get('language')
            await call.message.edit_text(text=text,
                                         reply_markup=await create_cart_keyboard(quantity=quantity, language=language))
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
        data = await state.get_data()
        language = data.get('language')
        await call.message.edit_text(text=text,
                                     reply_markup=await create_cart_keyboard(quantity=quantity, language=language))
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
            data = await state.get_data()
            language = data.get('language')

            await call.answer(f"Added {quantity} of {product_name} to cart!")
            await call.message.answer(text=text, reply_markup=await place_order(language=language))


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
        data = await state.get_data()
        language = data.get('language')

        await call.message.answer(
            text=_("Please, select a payment method:"),
            reply_markup=await payment_method_keyboard(language=language))


@dp.message_handler(lambda message: message.text in ["Cash", "Naqd to'lov"])
async def cash_payment_handler(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    order_id = user_data.get('order_id')

    if order_id:
        data = await state.get_data()
        language = data.get('language')
        await update_order(order_id=order_id, status=True)
        await message.answer(text=_("Order received. We deliver in 25-30 minutes. 🚚"),
                             reply_markup=await user_main_menu_keyboard(language=language))


@dp.message_handler(lambda message: message.text in ["Click", "Payme"])
async def cash_payment_handler(message: types.Message):
    await message.answer(text=_("Currently not working"))


@dp.message_handler(lambda message: message.text in ["🛍 My orders", "🛍 Mening buyurtmalarim"])
async def get_orders(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.chat.id)
    orders = await get_my_orders(user_id=user.get('id'))
    orders_string = ""

    data = await state.get_data()
    language = data.get('language')
    if orders:
        for order in orders:
            orders_string += (f"ID:   {order['id']}\n"
                              f"Product:   {order['product_name']}\n"
                              f"Price:   {order['product_price']}\n"
                              f"Quantity:   {order['quantity']}\n"
                              f"Total:   {order['total_price']}\n"
                              f"Status:   {order['status']}\n\n")
        await select_section(message=message, text=orders_string, state=state)
    else:
        await select_section(message=message, text=_("You have not ordered anything", locale=language), state=state)
