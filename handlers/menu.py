import logging
import loader

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaVideo

from keyboards import get_menu_page_keyboard

menu_router = Router(name=__name__)
logger = logging.getLogger(name=__name__)


async def get_menu_page(call: CallbackQuery):
    
    split_data = call.data.split("/")

    category = str(split_data[1])
    num_product_in_category = int(split_data[2])
    flag_delete_message = bool(split_data[3])

    products_by_cur_category = await loader.db.get_products_by_category(category)
    total_product_this_category_in_user_cart = await loader.db.get_product_total_in_cart_by_category(call.from_user.id, category)
    cur_product = products_by_cur_category[num_product_in_category]

    page_text = f"""
<blockquote expandable>🍽️ {cur_product["name"]}
💵 Стоимость: {cur_product["price"]} руб.
📝 Описание:
{cur_product["description"]}
</blockquote>"""

    keyboard = get_menu_page_keyboard(category, num_product_in_category, total_product_this_category_in_user_cart)

    if flag_delete_message or (not call.message.photo and not call.message.video):
        await call.message.delete()
        await call.message.answer_photo(photo=cur_product["telegram_id_image"], caption=page_text, reply_markup=keyboard)

    elif call.message.photo:
        await call.message.edit_media(media=InputMediaPhoto(media=cur_product["telegram_id_image"], caption=page_text), reply_markup=keyboard)

    elif call.message.video:
        await call.message.edit_media(media=InputMediaVideo(media=cur_product["telegram_id_image"], caption=page_text), reply_markup=keyboard)


menu_router.callback_query.register(get_menu_page, F.data[:14]=="show_menu_page")
