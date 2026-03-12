import logging
import loader

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards import get_menu_page_keyboard, get_cart_keyboard, empty_cart_keyboard

# creating router and logger
cart_router = Router()
logger = logging.getLogger(name=__name__)


@cart_router.callback_query(F.data == "open_cart")
async def on_open_cart(call: CallbackQuery):

    user_id = call.from_user.id

    user_cart = await loader.db.get_cart(user_id)

    total_sum = 0
    answer_text = """
🛒 Ваша корзина:
"""
    for product in user_cart:
        if not product["quantity"]:
            continue

        product_total_price = product["price"] * product["quantity"]
        total_sum += product_total_price
        answer_text += f"\n<blockquote>🍽️ {product['name']} - {product['price']} руб. * {product['quantity']} шт. = {product_total_price} руб.</blockquote>"

    answer_text += f"\n\n💵 Итого: {total_sum} руб."
    
    if not total_sum:
        await call.message.edit_text(text="<blockquote>🛒 Ваша корзина пуста</blockquote>\n <b>Выберите кнопку ниже</b>", reply_markup=empty_cart_keyboard)
        return

    await call.message.delete()
    await call.message.answer(answer_text, reply_markup=get_cart_keyboard(user_cart))


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
    product_in_user_cart = await loader.db.get_product_in_user_cart(user_id, product_id)

    quantity_in_cart = product_in_user_cart["quantity"] + quantity

    # adding result in database
    await loader.db.add_to_cart(user_id, product_id, quantity)

    # creating answer keyboard
    keyboard = get_menu_page_keyboard(category, num_product_in_ctg, quantity_product_in_ctg, quantity_in_cart, product_id)

    # edit markup under message
    await call.message.edit_reply_markup(reply_markup=keyboard)