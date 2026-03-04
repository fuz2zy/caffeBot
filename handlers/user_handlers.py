from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards.inline import start_keyboard

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    
    await message.answer("""start""", reply_markup=start_keyboard)

