from typing import Union
from aiogram import types

from logging_settings import logger
from main.database import database
from main.models import order, cart
from utils.db_commands.user import get_user


async def add_product_to_cart(message: types.Message, product_id: int, quantity=1) -> Union[int, None]:
    """Add cart to database with product"""
    try:
        user = await get_user(message.chat.id)
        query = cart.insert().values(
            product_id=product_id,
            quantity=quantity,
            user_id=user.get('id')
        ).returning(cart.c.id)
        new_cart_id = await database.execute(query=query)
        return new_cart_id
    except Exception as e:
        error_text = str(e)
        logger.error(error_text)
        return None


async def add_order(product_name, product_price, total_price, user_id, quantity=1, status=False) -> Union[int, None]:
    """Add order to database"""
    try:
        query = order.insert().values(
            product_name=product_name,
            product_price=product_price,
            quantity=quantity,
            total_price=total_price,
            status=status,
            user_id=user_id
        ).returning(order.c.id)
        new_order_id = await database.execute(query=query)
        return new_order_id
    except Exception as e:
        error_text = str(e)
        logger.error(error_text)
        return None


async def update_order(order_id: int, status: bool) -> Union[int, None]:
    """Add order to database"""
    try:
        query = order.update().where(order.c.id == order_id).values(status=status).returning(order.c.id)
        order_id = await database.execute(query=query)
        return order_id
    except Exception as e:
        error_text = str(e)
        logger.error(error_text)
        return None


async def get_cart(cart_id: int) -> Union[dict, None]:
    """Get cart data by id"""
    try:
        query = cart.select().where(cart.c.id == cart_id)
        row = await database.fetch_one(query=query)
        return dict(row) if row else None
    except Exception as e:
        error_text = str(e)
        logger.error(error_text)
        return None


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
