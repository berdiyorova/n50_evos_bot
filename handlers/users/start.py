import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.common import phone_number_share_keyboard
from keyboards.inline.user import languages
from keyboards.default.user import user_main_menu_keyboard, user_address_keyboard, set_language_settings
from loader import _
from loader import dp
from states.user import RegisterState
from utils.db_commands.feedback import add_feedback
from utils.db_commands.orders import get_my_orders
from utils.db_commands.user import get_user, add_user


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user = await get_user(chat_id=message.chat.id)
    if user:
        text = _("Welcome back! Select an option:")
        await select_section(message=message, text=text)
    else:
        text = "🇺🇿 Tilni tanlang\n🏴󠁧󠁢󠁥󠁮󠁧󠁿 Choose language\n🇷🇺 Выберите язык"
        await message.answer(text=text, reply_markup=languages)
        await RegisterState.language.set()



async def select_section(message, text):
    await message.answer(text=text, reply_markup=await user_main_menu_keyboard())


@dp.callback_query_handler(state=RegisterState.language)
async def language_handler(call: types.CallbackQuery, state: FSMContext):
    language = call.data
    if not language:
        language = 'en'
    await state.update_data(language=language)
    text = _("Please, enter your full name", locale=language)
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterState.full_name.set()



@dp.message_handler(state=RegisterState.full_name)
async def get_full_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    language = data.get('language')

    text = _("Please, enter your phone number by the button below 👇", locale=language)
    await message.answer(text=text, reply_markup=await phone_number_share_keyboard())
    await RegisterState.phone_number.set()


@dp.message_handler(state=RegisterState.phone_number, content_types=types.ContentTypes.CONTACT)
async def get_phone_number_handler(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    data = await state.get_data()
    language = data.get('language')

    new_user = await add_user(message=message, data=data)
    if new_user:
        text = _("You have successfully registered ✅", locale=language)
        await select_section(message=message, text=text)
    else:
        text = _("Sorry, please try again later 😔", locale=language)
        await message.answer(text=text)



@dp.message_handler(text="🍴 Menu")
async def submit_address(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    await message.answer(text=_("Submit your geolocation 📍 or select a delivery address", locale=language),
                         reply_markup=await user_address_keyboard())


@dp.message_handler(text="🛍 My orders")
async def get_orders(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.chat.id)
    orders = await get_my_orders(user_id=user.get('id'))

    data = await state.get_data()
    language = data.get('language')
    if orders:
        orders_string = '\n'.join(str(order) for order in orders)
        await select_section(message=message, text=orders_string)
    else:
        await select_section(message=message, text=_("You have not ordered anything", locale=language))



@dp.message_handler(text="✍️ Leave feedback")
async def get_feedback_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    text = _("Submit your feedback:", locale=language)
    await select_section(message=message, text=text)
    await RegisterState.feedback.set()


@dp.message_handler(state=RegisterState.feedback)
async def leave_feedback_handler(message: types.Message, state: FSMContext):
    await state.update_data(feedback=message.text)
    data = await state.get_data()
    language = data.get('language')

    new_feedback = await add_feedback(message=message, data=data)
    if new_feedback:
        text = _("Your feedback has successfully submitted ✅", locale=language)
        await select_section(message=message, text=text)
    else:
        text = _("Sorry, please try again later 😔", locale=language)
        await message.answer(text=text)
    await state.finish()


@dp.message_handler(text="⚙️ Settings")
async def select_action(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    text = _("Select_action:", locale=language)
    await message.answer(text=text, reply_markup=await set_language_settings())


@dp.message_handler(text="Set language settings")
async def set_language(message: types.Message, state: FSMContext):
    text = "🇺🇿 Tilni tanlang\n🏴󠁧󠁢󠁥󠁮󠁧󠁿 Choose language\n🇷🇺 Выберите язык"
    await message.answer(text=text, reply_markup=languages)
    await RegisterState.user_language.set()


@dp.callback_query_handler(state=RegisterState.user_language)
async def user_language_handler(call: types.CallbackQuery, state: FSMContext):
    language = call.data
    await state.update_data(language=language)
    await select_section(message=call.message, text=call.data)
    await state.finish()
