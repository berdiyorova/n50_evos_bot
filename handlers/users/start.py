from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.common import phone_number_share_keyboard
from keyboards.inline.user import languages
from keyboards.default.user import user_main_menu_keyboard
from loader import _
from loader import dp
from states.user import RegisterState
from utils.db_commands.user import get_user, add_user


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.chat.id)
    if user:
        text = _("Welcome back! Select an option:")
        await select_section(message=message, text=text, state=state)
    else:
        text = "🇺🇿 Tilni tanlang\n🏴󠁧󠁢󠁥󠁮󠁧󠁿 Choose language\n🇷🇺 Выберите язык"
        await message.answer(text=text, reply_markup=languages)
        await RegisterState.language.set()


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
    await message.answer(text=text, reply_markup=await phone_number_share_keyboard(language=language))
    await RegisterState.phone_number.set()


@dp.message_handler(state=RegisterState.phone_number, content_types=types.ContentTypes.CONTACT)
async def get_phone_number_handler(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    data = await state.get_data()
    language = data.get('language')

    new_user = await add_user(message=message, data=data)
    if new_user:
        text = _("You have successfully registered ✅", locale=language)
        await select_section(message=message, text=text, state=state)
    else:
        text = _("Sorry, please try again later 😔", locale=language)
        await message.answer(text=text)



async def select_section(message, text, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    await message.answer(text=text, reply_markup=await user_main_menu_keyboard(language=language))
