from aiogram import BaseMiddleware
from aiogram.types import User

from database import add_user


class RegisterMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        
        user: User = data.get("event_from_user")
        user_id = user.id
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        pool = data["pool"]

        if not user.is_bot:
            await add_user(pool, user_id, username, first_name, last_name)

        return await handler(event, data)