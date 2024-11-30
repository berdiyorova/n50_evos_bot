from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import select_section
from loader import dp, _
from states.user import RegisterState
from utils.db_commands.feedback import add_feedback


@dp.message_handler(lambda message: message.text in ["✍️ Leave feedback", "✍️ Fikr qoldiring"])
async def get_feedback_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    text = _("Submit your feedback:", locale=language)
    await select_section(message=message, text=text, state=state)
    await RegisterState.feedback.set()


@dp.message_handler(state=RegisterState.feedback)
async def leave_feedback_handler(message: types.Message, state: FSMContext):
    await state.update_data(feedback=message.text)
    data = await state.get_data()
    language = data.get('language')

    new_feedback = await add_feedback(message=message, data=data)
    if new_feedback:
        text = _("Your feedback has successfully submitted ✅", locale=language)
        await select_section(message=message, text=text, state=state)
    else:
        text = _("Sorry, please try again later 😔", locale=language)
        await message.answer(text=text)
    await state.finish()
