from aiogram import Router, types, Bot
from aiogram.filters import Command, ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION, PROMOTED_TRANSITION
from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.orm_query import orm_add_user, orm_blocked_user
from ..filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))
user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))

admins = set()


@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins = await bot.get_chat_administrators(chat_id)
    admins = [
        member.user.id
        for member in admins
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins
    if message.from_user.id in admins:
        await message.delete()


@user_group_router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def new_member(event: ChatMemberUpdated, session: AsyncSession):
    user_id = event.new_chat_member.user.id
    first_name = event.new_chat_member.user.first_name
    last_name = event.new_chat_member.user.last_name
    await orm_add_user(session, user_id=user_id, first_name=first_name, last_name=last_name)
    await event.answer(f"<b>{first_name} {last_name}, добро пожаловать в группу!👋</b>\n"
                       f"Теперь вы можете воспользоваться ботом https://t.me/malex_host_bot",
                       parse_mode="HTML")


@user_group_router.chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def out_member(event: ChatMemberUpdated, session: AsyncSession):
    user_id = event.old_chat_member.user.id
    first_name = event.old_chat_member.user.first_name
    last_name = event.old_chat_member.user.last_name
    await orm_blocked_user(session, user_id)
    await event.answer(f"<b>Пользователь {first_name} {last_name} покинул группу.☹️</b>",
                       parse_mode="HTML")
