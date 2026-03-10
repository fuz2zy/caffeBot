from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Меню 📝", callback_data="show_menu")],
    [InlineKeyboardButton(text="Корзина 🛒", callback_data="open_cart")],
    [InlineKeyboardButton(text="Помощь ❓", callback_data="get_help")],
    [InlineKeyboardButton(text="Наше приложение 📱", callback_data="open_mini_app")]
])

start_message = """
<i><b>Приветсвую!</b> Я телеграм боте кафе <b>DEJAVU☕</b></i>

<b>Тут ты можешь:</b>

<blockquote>-Ознакомиться с нашим меню 📝</blockquote>
<blockquote>-Первым получать уведомления об акциях 🗞️</blockquote>
<blockquote>-Делать заказы прямо из Telegram! 🛒</blockquote>

<i><b>Что вы хотите посмотреть?</b></i>
"""