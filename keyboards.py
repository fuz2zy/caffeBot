from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# func creates keyboard by args, 1: category of page, 2: product number in category
# 3: quantity products in category, 4: quantity this product in user cart
def get_menu_page_keyboard(category: str, num_product_in_ctg: int, quantity_product_in_ctg: int, quantity_in_cart: int) -> InlineKeyboardMarkup:

    # check if the user has in cart some product and create buttons based on result 
    if not quantity_in_cart:
        buttons = [[InlineKeyboardButton(text="🛒 Добавить в корзину", callback_data="add_to_cart")]]
    else:
        buttons = [
            [
                InlineKeyboardButton(text="-", callback_data="del_from_cart"), 
                InlineKeyboardButton(text=f"🛒 | {quantity_in_cart}", callback_data="open_cart"),
                InlineKeyboardButton(text="+", callback_data="add_to_cart")
            ]
        ]
    
    # append base buttons for change menu page
    buttons.append([
        InlineKeyboardButton(text="«Назад", callback_data=f"show_menu_page/{category}/{num_product_in_ctg-1}/0"),
        InlineKeyboardButton(text=f"☰ {num_product_in_ctg+1}/{quantity_product_in_ctg}", callback_data=f"change_category"),
        InlineKeyboardButton(text="Вперед»", callback_data=f"show_menu_page/{category}/{num_product_in_ctg+1}/0")

    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# text and keyboard for command start
start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Меню 📝", callback_data="show_menu_page/Фаст-Фуд/0/1")],
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