from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import Database

bot: Bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp: Dispatcher = Dispatcher(storage=MemoryStorage())
db: Database | None = None