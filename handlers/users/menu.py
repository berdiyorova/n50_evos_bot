from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.user import test_callback_data
from keyboards.inline.user import test_callback_keyboard
from loader import dp
from main.config import ADMINS


@dp.message_handler(commands="test", chat_id=ADMINS, state="*")
async def test_handler(message: types.Message, state: FSMContext):
    text = "Test"
    await message.answer(text=text, reply_markup=await test_callback_keyboard())


@dp.callback_query_handler(test_callback_data.filter(action="general_button"))
async def test_callback_handler(call: types.CallbackQuery, callback_data: dict):
    product_id = callback_data.get("product_id")
    await call.answer(text=product_id)
