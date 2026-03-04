from dotenv import load_dotenv
import logging
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = os.getenv("ADMIN_ID", 0)



if __name__ == "__main__":

    if not BOT_TOKEN:
        logging.critical("Токен бота не найден, бот не может быть запущен")
    if not ADMIN_ID:
        logging.warning("Айди администратора бота не найден")