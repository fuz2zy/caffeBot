import logging
import loader

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from keyboards import verifi_phone_keyboard, start_keyboard, empty_cart_keyboard

order_router = Router()


@order_router.callback_query(F.data == "create_order")
async def on_create_order(call: CallbackQuery):

    user_id = call.from_user.id

    user_phone = await loader.db.get_user_phone(user_id)

    print(user_phone)

    if not user_phone:
        await call.message.delete()
        await call.message.answer("<i><b>Вы еще не верифицировали свой номер телефона, для этого нажмите на кнопку ниже и поделитесь своим номером телефона</b></i>", reply_markup=verifi_phone_keyboard)
        return

    user_cart = await loader.db.get_cart(user_id)

    if not user_cart:
        await call.message.edit_text(text="<blockquote>🛒 Ваша корзина пуста</blockquote>\n <b>Выберите кнопку ниже</b>", reply_markup=empty_cart_keyboard)
        return


    total_sum = 0
    answer_text = """
Ваш Заказ:
"""
    for product in user_cart:
        if not product["quantity"]:
            continue

        product_total_price = product["price"] * product["quantity"]
        total_sum += product_total_price
        answer_text += f"\n<blockquote>🍽️ {product['name']} - {product['price']} руб. * {product['quantity']} шт. = {product_total_price} руб.</blockquote>"

    answer_text += f"\n\n💵 Итого: {total_sum} руб."


    await call.message.edit_text(answer_text)


@order_router.message(F.contact)
async def on_get_contact(message: Message):

    contact = message.contact
    user_id = message.from_user.id

    if contact.user_id and contact.user_id == user_id:
        phone = contact.phone_number

        await loader.db.add_user_phone(user_id, phone)

        await message.answer("Вы были успешно верифицированны, теперь вы можете заказывать.", reply_markup=ReplyKeyboardRemove())

        user_cart = await loader.db.get_cart(user_id)

        if not user_cart:
            await message.answer(text="<blockquote>🛒 Ваша корзина пуста</blockquote>\n <b>Выберите кнопку ниже</b>", reply_markup=empty_cart_keyboard)
            return


    total_sum = 0
    answer_text = """
Ваш Заказ:
"""
    for product in user_cart:
        if not product["quantity"]:
            continue

        product_total_price = product["price"] * product["quantity"]
        total_sum += product_total_price
        answer_text += f"\n<blockquote>🍽️ {product['name']} - {product['price']} руб. * {product['quantity']} шт. = {product_total_price} руб.</blockquote>"

    answer_text += f"\n\n💵 Итого: {total_sum} руб."


    await message.answer(answer_text)

    
