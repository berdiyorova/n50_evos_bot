from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import select_section
from loader import dp, _


@dp.message_handler(text="⬅️ Back")
async def go_back_handler(message: types.Message, state: FSMContext):
    await select_section(message=message, text=_("Select an option:"))
