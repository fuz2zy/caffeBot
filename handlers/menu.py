import logging
import loader

from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, InputMediaVideo

from keyboards import get_menu_page_keyboard

# create router and logger
menu_router = Router(name=__name__)
logger = logging.getLogger(name=__name__)

# registering the callback handler on call.data prefix "show_menu_page" 
@menu_router.callback_query(F.data[:14]=="show_menu_page")
async def get_menu_page(call: CallbackQuery) -> None:
    
    # getting data from string of call.data where data is split by "/"
    # where first arg is prefix, second arg is the product number in its category
    # third arg is a flag indicating whether to delete the message 

    user_id = call.from_user.id

    split_data = call.data.split("/")

    category = str(split_data[1])
    num_product_in_ctg = int(split_data[2])
    flag_del_msg = bool(int(split_data[3]))

    products_by_cur_ctg = await loader.db.get_products_by_category(category)

    # setting the boundaries of the product feed
    if num_product_in_ctg > len(products_by_cur_ctg) - 1:
        num_product_in_ctg = 0
    elif num_product_in_ctg < 0:
        num_product_in_ctg = len(products_by_cur_ctg) - 1
    
    # getting product page info by its number from list of products such category
    cur_product = products_by_cur_ctg[num_product_in_ctg]

    # making a query to the db to get list of products by category
    # number of products with this category in user cart
    products_by_cur_ctg = await loader.db.get_products_by_category(category)
    quantity_in_cart = (await loader.db.get_product_in_user_cart(user_id, cur_product["id"]))["quantity"]
    
    # create text of answer
    page_text = f"""
<blockquote expandable>🍽️ {cur_product["name"]}
💵 Стоимость: {cur_product["price"]} руб.
📝 Описание:
{cur_product["description"]}
</blockquote>"""

    # getting keyboard from keyboards.get_menu_page_keyboard 
    keyboard = get_menu_page_keyboard(category, num_product_in_ctg, len(products_by_cur_ctg), quantity_in_cart, cur_product["id"])

    # process different cases of media availability
    if flag_del_msg or (not call.message.photo and not call.message.video):
        await call.message.delete()
        await call.message.answer_photo(photo=cur_product["telegram_id_image"], caption=page_text, reply_markup=keyboard)

    elif call.message.photo:
        await call.message.edit_media(media=InputMediaPhoto(media=cur_product["telegram_id_image"], caption=page_text), reply_markup=keyboard)

    elif call.message.video:
        await call.message.edit_media(media=InputMediaVideo(media=cur_product["telegram_id_image"], caption=page_text), reply_markup=keyboard)
