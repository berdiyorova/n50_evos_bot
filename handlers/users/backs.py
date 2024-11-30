from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import select_section
from loader import dp, _


@dp.message_handler(lambda message: message.text in ["⬅️ Back", "⬅️ Orqaga"])
async def go_back_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    await select_section(message=message, text=_("Select an option:", locale=language), state=state)
