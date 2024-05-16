from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

from src.constants import NO
from src.database.orm_query import orm_delete_user, orm_add_user


async def delete_user_yes_no(
        callback: CallbackQuery, widget: Any,
        dialog_manager: DialogManager, item_id: str, **kwargs
):
    if item_id == NO:
        await dialog_manager.done()
    user_id = dialog_manager.start_data["user"]
    session = dialog_manager.middleware_data.get("session")
    await orm_delete_user(session, int(user_id))
    await dialog_manager.next()
    await callback.answer()


async def add_user_yes_no(
        callback: CallbackQuery, widget: Any,
        dialog_manager: DialogManager, item_id: str, **kwargs
):
    if item_id == NO:
        await dialog_manager.done()
    session = dialog_manager.middleware_data.get("session")
    await orm_add_user(session, dialog_manager.dialog_data)
    await dialog_manager.next()
    await callback.answer()


async def user_id_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["user_id"] = int(message.text)
    await message.delete()
    await dialog_manager.next()


async def first_name_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["first_name"] = message.text
    await message.delete()
    await dialog_manager.next()


async def last_name_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["last_name"] = message.text
    await message.delete()
    await dialog_manager.next()


async def sectors_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    sectors = dialog_manager.find("m_sectors")
    sectors_list = sectors.get_checked()
    dialog_manager.dialog_data["sectors"] = sectors_list
    await dialog_manager.next()


async def contact_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["phone"] = message.contact.phone_number
    await dialog_manager.next()
