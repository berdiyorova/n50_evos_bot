from typing import Union

from aiogram import types

from logging_settings import logger
from main.database import database
from main.models import feedback
from utils.db_commands.user import get_user


async def add_feedback(message: types.Message, data: dict) -> Union[int, None]:
    """Add user to database"""
    try:
        user = await get_user(message.chat.id)
        query = feedback.insert().values(
            text=message.text,
            user_id=user.get('id')
        ).returning(feedback.c.id)
        feedback_id = await database.execute(query=query)
        return feedback_id
    except Exception as e:
        error_text = f"Error adding new user{message.chat.id}: {e}"
        logger.error(error_text)
        return None
