from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = os.getenv("ADMIN_ID", 0)
DATABASE_URL = os.getenv("DATABASE_URL", "")

LOG_PATH = "logs.log"

MESSAGE_COOLDOWN = 3
CALLBACK_COOLDOWN = 1

if ADMIN_ID:
    ADMIN_ID = int(ADMIN_ID)