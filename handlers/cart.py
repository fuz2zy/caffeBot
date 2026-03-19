import logging
import loader

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards import get_menu_page_keyboard, get_cart_keyboard, empty_cart_keyboard

# creating router and logger
cart_router = Router()
logger = logging.getLogger(name=__name__)


def get_cart_text(user_cart):

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
        return "<blockquote>🛒 Ваша корзина пуста</blockquote>\n <b>Выберите кнопку ниже</b>", total_sum

    return answer_text, total_sum


@cart_router.callback_query(F.data == "open_cart")
async def on_open_cart(call: CallbackQuery):

    user_id = call.from_user.id

    user_cart = await loader.db.get_cart(user_id)

    answer_text, total_sum = get_cart_text(user_cart)
    keyboard = get_cart_keyboard(user_cart)

    await call.message.delete()
    if not total_sum:
        await call.message.answer(text=answer_text, reply_markup=empty_cart_keyboard)
    else:
        await call.message.answer(answer_text, reply_markup=keyboard)


# registering handler on prefix call.data "add_to_cart"
@cart_router.callback_query(F.data[:11] == "add_to_cart")
async def add_to_cart(call: CallbackQuery):

    # this fuction needed to add or del quantity product in user cart
    # in split_data first arg after prefix is the adding quantity
    # this arg can will 1 or -1 or any number

    # THIS HANDLER USING ONLY IN MENU, NOT IN CART, IT CHANGING MENU MARKUP

    # getting data from split_data
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



@cart_router.callback_query(F.data[:16] == "remove_from_cart")
async def on_remove_from_cart(call: CallbackQuery):

    user_id = call.from_user.id

    split_data = call.data.split("/")

    product_id = int(split_data[1])
    product_quantity = int(split_data[2])

    await loader.db.add_to_cart(user_id, product_id, -product_quantity)
    user_cart = await loader.db.get_cart(user_id)

    keyboard = get_cart_keyboard(user_cart)
    answer_text, total_sum = get_cart_text(user_cart)
    
    if not total_sum:
        await call.message.edit_text(text="<blockquote>🛒 Ваша корзина пуста</blockquote>\n <b>Выберите кнопку ниже</b>", reply_markup=empty_cart_keyboard)
    else:
        await call.message.edit_text(answer_text, reply_markup=keyboard)

