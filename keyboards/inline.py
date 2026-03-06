from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Меню", callback_data="show_menu")],
    [InlineKeyboardButton(text="Корзина", callback_data="open_cart")],
    [InlineKeyboardButton(text="Помощь", callback_data="get_help")],
    [InlineKeyboardButton(text="Открыть Приложение", callback_data="open_mini_app")]
])