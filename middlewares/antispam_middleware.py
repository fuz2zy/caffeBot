import time
import loader

from aiogram import BaseMiddleware
from aiogram.types import User, Update, Message, CallbackQuery

from config import MESSAGE_COOLDOWN, CALLBACK_COOLDOWN

class AntisamMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        
        user: User = data.get("event_from_user")
        user_id = user.id

        if not loader.users_last_actions.get(user_id, 0):
            loader.users_last_actions[user_id] = time.time()
            return await handler(event, data)

        if event.message:
            if time.time() - loader.users_last_actions[user_id] > MESSAGE_COOLDOWN:
                loader.users_last_actions[user_id] = time.time()
                return await handler(event, data)
            else:
                return
        
        elif event.callback_query:
            if time.time() - loader.users_last_actions[user_id] > CALLBACK_COOLDOWN:
                loader.users_last_actions[user_id] = time.time()
                return await handler(event, data)
            else:
                await event.callback_query.answer("Не так быстро!")
                return
        
        return await handler(event, data)