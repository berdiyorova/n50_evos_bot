from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import select_section
from loader import dp, _
from utils.db_commands.orders import get_my_orders
from utils.db_commands.user import get_user


@dp.message_handler(text="🛍 My orders")
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
        await select_section(message=message, text=orders_string)
    else:
        await select_section(message=message, text=_("You have not ordered anything", locale=language))
