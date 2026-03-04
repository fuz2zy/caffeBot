import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, ADMIN_ID


def main():

    logging.basicConfig(lavel=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', handlers=[logging.StreamHandler(), logging.FileHandler("bot_logs.log", encoding="utf-8")])

    logger = logging.getLogger(__name__)

    if not BOT_TOKEN:
        logger.critical("Токен бота не найдет, остановка работы")
        return
    if not ADMIN_ID:
        logger.warning("Айди администратора не найден")

    bot = Bot(BOT_TOKEN=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    