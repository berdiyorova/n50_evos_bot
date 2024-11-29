from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import select_section
from keyboards.default.user import set_language
from keyboards.inline.user import languages
from loader import dp, _
from states.user import RegisterState


@dp.message_handler(text="⚙️ Settings")
async def select_action(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    text = _("Select_action:", locale=language)
    await message.answer(text=text, reply_markup=await set_language())


@dp.message_handler(text="Set language settings")
async def set_language_settings(message: types.Message, state: FSMContext):
    text = "🇺🇿 Tilni tanlang\n🏴󠁧󠁢󠁥󠁮󠁧󠁿 Choose language\n🇷🇺 Выберите язык"
    await message.answer(text=text, reply_markup=languages)
    await RegisterState.user_language.set()


@dp.callback_query_handler(state=RegisterState.user_language)
async def change_user_language(call: types.CallbackQuery, state: FSMContext):
    language = call.data
    await state.update_data(language=language)
    await select_section(message=call.message, text=call.data)
    await state.finish()
