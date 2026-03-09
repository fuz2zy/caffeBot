import asyncio
import asyncpg
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, DATABASE_URL, LOG_PATH
from database import init_db
from handlers.user_handlers import user_router
from middlewares.reg_middleware import RegisterMiddleware
 
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())


@dp.startup()
async def on_startup():
    logger.info("Бот запускается...")
    pool = await asyncpg.create_pool(DATABASE_URL)

    await init_db(pool)

    dp["pool"] = pool
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
    
    dp.include_router(user_router)


    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())