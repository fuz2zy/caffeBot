import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards import start_message, start_keyboard

start_router = Router(name=__name__)
logger = logging.getLogger(name=__name__)

@start_router.message(CommandStart())
async def on_cmd_start(message: Message):

    await message.answer(start_message, reply_markup=start_keyboard)


@start_router.callback_query(F.data == "start_message")
async def on_start_message(call: CallbackQuery):

    await call.message.delete()
    await call.message.answer(start_message, reply_markup=start_keyboard)


@start_router.message(F.text)
async def on_text(message: Message):
    logger.info(message.text)


@start_router.message(F.photo)
async def on_text(message: Message):
    logger.info(message.photo[-1].file_id)