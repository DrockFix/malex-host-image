from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import TelegramObject

from src.database.orm_query import orm_get_users


class UserBannedMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        users = await orm_get_users(data["session"])
        for user in users:
            if event.from_user.id == user.user_id:
                if user.is_blocked:
                    await event.answer("Вы заблокированы")
                    raise CancelHandler
                data['user'] = user
                return await handler(event, data)
        raise CancelHandler
