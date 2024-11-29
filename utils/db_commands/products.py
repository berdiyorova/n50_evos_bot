from typing import Union

from logging_settings import logger
from main.database import database
from main.models import category, product


async def get_categories() -> Union[list, None]:
    """Get categories data"""
    try:
        query = category.select()
        rows = await database.fetch_all(query=query)
        return [row['name'] for row in rows] if rows else []
    except Exception as e:
        error_text = str(e)
        logger.error(error_text)
        return None


async def get_category(name: str) -> Union[dict, None]:
    """Get category data by name"""
    try:
        query = category.select().where(category.c.name == name)
        row = await database.fetch_one(query=query)
        return dict(row) if row else None
    except Exception as e:
        error_text = str(e)
        logger.error(error_text)
        return None


async def get_product(product_id: int) -> Union[dict, None]:
    """Get product data by id"""
    try:
        query = product.select().where(product.c.id == product_id)
        row = await database.fetch_one(query=query)
        return dict(row) if row else None
    except Exception as e:
        error_text = str(e)
        logger.error(error_text)
        return None


async def get_products(category_name: str) -> Union[list, None]:
    """Get products data by category name"""
    try:
        cat = await get_category(category_name)
        query = product.select().where(product.c.category_id == cat.get('id'))
        rows = await database.fetch_all(query=query)
        return list(rows) if rows else []
    except Exception as e:
        error_text = str(e)
        logger.error(error_text)
        return None
