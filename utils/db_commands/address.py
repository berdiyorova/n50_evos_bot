from typing import Union

from aiogram import types

from logging_settings import logger
from main.database import database
from main.models import address
from utils.db_commands.user import get_user


async def address_exists(name, latitude, longitude):
    query = address.select().where(
        address.c.name == name,
        address.c.latitude == str(latitude),
        address.c.longitude == str(longitude)
    )
    row = await database.fetch_one(query=query)

    if row:
        return True

    return False


async def get_address_by_name(name: str) -> Union[dict, None]:
    """Get address data by name"""
    try:
        query = address.select().where(address.c.name == name)
        row = await database.fetch_one(query=query)
        return dict(row) if row else None
    except Exception as e:
        error_text = str(e)
        logger.error(error_text)
        return None


async def get_user_address(chat_id: int) -> Union[list, None]:
    """Get address data by chat id"""
    try:
        user_data = await get_user(chat_id)
        query = address.select().where(address.c.user_id == user_data.get('id'))
        rows = await database.fetch_all(query=query)
        return list(rows) if rows else []
    except Exception as e:
        error_text = str(e)
        logger.error(error_text)
        return None


async def add_address(message: types.Message, name: str, latitude: float, longitude: float) -> Union[int, None]:
    """Add address to database"""
    try:
        if not await address_exists(name=name, latitude=latitude, longitude=longitude):
            user = await get_user(message.chat.id)
            query = address.insert().values(
                user_id=user.get('id'),
                name=name,
                latitude=str(latitude),
                longitude=str(longitude),
                created_at=message.date,
                updated_at=message.date
            ).returning(address.c.id)
            new_address_id = await database.execute(query=query)
            return new_address_id
    except Exception as e:
        error_text = str(e)
        logger.error(error_text)
        return None
