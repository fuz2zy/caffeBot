import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from loader import db

menu_router = Router(name=__name__)
logger = logging.getLogger(name=__name__)


async def get_menu_page(call: CallbackQuery):
    
    split_data = call.data.split("/")

    category = split_data[1]
    num_product_in_category = int(split_data[2])
    delete_message = bool(split_data[3])

    products_by_cur_category = await db.get_products_by_category(category)
    cur_product = products_by_cur_category[num_product_in_category]

    page_text = f"""
<blockquote expandable>

</blockqoute>"""

    logger.info(category)

    # if delete_message:
    #     await call.message.delete()
    
    # await call.message.answer()


menu_router.callback_query.register(get_menu_page, F.data[:9]=="show_menu")
