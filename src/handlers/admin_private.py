import os

from aiogram import Router, types, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.orm_query import orm_add_user
from ..filters.chat_types import ChatTypeFilter, IsAdmin
from ..states.admin import AdminMenu
from ..utils.chat_members import get_chat_members

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


@admin_router.message(Command("admin"))
async def admin_features(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminMenu.menu, mode=StartMode.RESET_STACK)
    # await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(Command("members"))
async def get_members(message: types.Message, session: AsyncSession):
    members = await get_chat_members(os.getenv("CLIENT_NAME"),
                                     os.getenv("TELEGRAM_API_ID"),
                                     os.getenv("TELEGRAM_API_HASH"),
                                     os.getenv("TOKEN"),
                                     int(os.getenv("CHAT_ID")))
    text = "Список участников:\n"
    for member in members:
        text += (f"{member.user.id}: {member.user.first_name if member.user.first_name else ''}"
                 f" {member.user.last_name if member.user.last_name else ''}\n")
        await orm_add_user(session, member.user)
    await message.answer(text)
