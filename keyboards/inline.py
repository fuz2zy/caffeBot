from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("Меню", callback_data="show_menu")]
])