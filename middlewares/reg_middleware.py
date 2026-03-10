from aiogram import BaseMiddleware
from aiogram.types import User

import loader

class RegisterMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        
        user: User = data.get("event_from_user")
        user_id = user.id
        username = user.username
        first_name = user.first_name
        last_name = user.last_name

        if not user.is_bot:
            await loader.db.add_user(user_id, username, first_name, last_name)

        return await handler(event, data)