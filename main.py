import asyncio
import asyncpg
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, DATABASE_URL, LOG_PATH
from database import Database
from handlers.start import start_router
from middlewares.reg_middleware import RegisterMiddleware
 
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())
db = None


@dp.startup()
async def on_startup():
    
    logger.info("Бот запускается...")
    
    db = await Database()
    
    await db.add_product(pool, "Бургер", 10, "Фаст-Фуд", "AgACAgIAAxkBAANFaa6q4dpohMpw8ZXJm6ETjKdYUBUAAn4Vaxt3mXlJklDNS1HNAkwBAAMCAAN4AAM6BA", "это бургер")
    await db.add_product(pool, "Нагеттсы", 5, "Фаст-Фуд", "AgACAgIAAxkBAAM9aa6qrgN2891H99UFWVuCK7KW0kgAAnsVaxt3mXlJv-nQVifsZ9EBAAMCAAN5AAM6BA", "Это нагеттсы")
    await db.add_product(pool, "Картошка фри", 7, "Фаст-Фуд", "AgACAgIAAxkBAAM-aa6qrpW2kVcI3TA0NqKYdXxs0tYAAnwVaxt3mXlJ5ht2v4VE-qYBAAMCAAN4AAM6BA", "Это картошка фри")
    
    dp.update.middleware(RegisterMiddleware())
    
    logger.info("БД подключена")


@dp.shutdown()
async def on_shutdown():
    logger.info("Бот отключается...")
    pool = dp.get("pool")

    if pool:
        await pool.close()

    logger.info("БД отключена")


async def main():

    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_PATH,encoding="utf-8")
        ]
    )
    
    dp.include_router(start_router)


    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())