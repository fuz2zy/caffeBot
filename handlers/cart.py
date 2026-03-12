import logging
import loader

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards import get_menu_page_keyboard

cart_router = Router()
logger = logging.getLogger(name=__name__)

# registering handler on prefix call.data "add_to_cart"
@cart_router.callback_query(F.data[:11] == "add_to_cart")
async def add_to_cart(call: CallbackQuery):

    # this fuction needed to add or del quantity product in user cart
    # in split_data first arg after prefix is the adding quantity
    # this arg can will 1 or -1 or any number

    # getting data from slit_data
    split_data = call.data.split("/")

    user_id = call.from_user.id

    quantity = int(split_data[1])
    product_id = int(split_data[2])
    category = split_data[3]
    num_product_in_ctg = int(split_data[4])

    # getting data from database
    quantity_product_in_ctg = len(await loader.db.get_products_by_category(category))
    quantity_in_cart = int((await loader.db.get_product_in_user_cart(user_id, product_id))["quantity"] + quantity)

    # adding result in database
    await loader.db.add_to_cart(user_id, product_id, quantity)

    # creating answer keyboard
    keyboard = get_menu_page_keyboard(category, num_product_in_ctg, quantity_product_in_ctg, quantity_in_cart, product_id)

    # edit markup under message
    await call.message.edit_reply_markup(reply_markup=keyboard)