import logging

from aiogram import Router
from aiogram.types import Message, CallbackQuery

from database import get_products_by_category

menu_router = Router(name=__name__)
logger = logging.getLogger(name=__name__)


async def get_menu_page(category, num_product_in_category=0, delete_message=False):

    
    products_by_cur_category = await get_products_by_category(category)
    cur_product = products_by_cur_category[num_product_in_category]

    logging.info(cur_product)



