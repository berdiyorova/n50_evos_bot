from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.common import phone_number_share_keyboard
from keyboards.default.user import user_main_menu_keyboard
from loader import dp
from main.config import ADMINS
from states.user import RegisterState
from utils.db_commands.user import get_user, add_user


@dp.message_handler(commands="start", chat_id=ADMINS, state="*")
async def start_handler(message: types.Message, state: FSMContext):
    await state.finish()
    user = await get_user(chat_id=message.chat.id)
    if user:
        text = "Welcome back my hero 😊"
        await message.answer(text=text, reply_markup=await user_main_menu_keyboard())
    else:
        text = "Sorry, you have to enter your full name"
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
        await RegisterState.full_name.set()


@dp.message_handler(state=RegisterState.full_name)
async def get_full_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)

    text = "Please, enter your phone number by the button below 👇"
    await message.answer(text=text, reply_markup=await phone_number_share_keyboard())
    await RegisterState.phone_number.set()


@dp.message_handler(state=RegisterState.phone_number, content_types=types.ContentTypes.CONTACT)
async def get_phone_number_handler(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    data = await state.get_data()
    new_user = await add_user(message=message, data=data)
    if new_user:
        text = "You have successfully registered ✅"
        await message.answer(text=text, reply_markup=await user_main_menu_keyboard())
    else:
        text = "Sorry, please try again later 😔"
        await message.answer(text=text)
    await state.finish()
