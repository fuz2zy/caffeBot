import asyncio
import asyncpg
import logging
import loader

from loader import bot, dp
from database import Database
from handlers.menu import menu_router
from handlers.start import start_router
from config import DATABASE_URL, LOG_PATH
from middlewares.reg_middleware import RegisterMiddleware
 
logger = logging.getLogger(__name__)


@dp.startup()
async def on_startup():
    logger.info("Бот запускается...")
    
    await loader.db.add_product("Бургер", 10, "Фаст-Фуд", "AgACAgIAAxkBAANFaa6q4dpohMpw8ZXJm6ETjKdYUBUAAn4Vaxt3mXlJklDNS1HNAkwBAAMCAAN4AAM6BA", "это бургер")
    await loader.db.add_product("Нагеттсы", 5, "Фаст-Фуд", "AgACAgIAAxkBAAM9aa6qrgN2891H99UFWVuCK7KW0kgAAnsVaxt3mXlJv-nQVifsZ9EBAAMCAAN5AAM6BA", "Это нагеттсы")
    await loader.db.add_product("Картошка фри", 7, "Фаст-Фуд", "AgACAgIAAxkBAAM-aa6qrpW2kVcI3TA0NqKYdXxs0tYAAnwVaxt3mXlJ5ht2v4VE-qYBAAMCAAN4AAM6BA", "Это картошка фри")
    
    dp.update.middleware(RegisterMiddleware())
    
    logger.info("БД подключена")


@dp.shutdown()
async def on_shutdown():
    logger.info("Бот отключается...")
    
    await loader.db.close_pool()

    logger.info("БД отключена")


async def main():

    pool = await asyncpg.create_pool(DATABASE_URL)
    
    loader.db = Database(pool)
    await loader.db.init_db()

    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_PATH,encoding="utf-8")
        ]
    )
    
    dp.include_router(start_router)
    dp.include_router(menu_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())