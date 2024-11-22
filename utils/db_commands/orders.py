from typing import Union

from logging_settings import logger
from main.database import database
from main.models import order


async def get_my_orders(user_id: int) -> Union[list[dict], None]:
    """Get orders data by user id"""
    try:
        query = order.select().where(order.c.user_id == user_id)
        rows = await database.fetch_all(query=query)
        return [dict(row) for row in rows] if rows else []
    except Exception as e:
        error_text = f"Error retrieving user with ID {user_id}: {e}"
        logger.error(error_text)
        return None
