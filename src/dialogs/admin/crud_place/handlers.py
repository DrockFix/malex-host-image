from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

from src.constants import NO
from src.database.orm_query import orm_delete_place, orm_add_place


async def delete_place_yes_no(
        callback: CallbackQuery, widget: Any,
        dialog_manager: DialogManager, item_id: str, **kwargs
):
    if item_id == NO:
        await dialog_manager.done()
    place_id = dialog_manager.start_data["place"]
    session = dialog_manager.middleware_data.get("session")
    await orm_delete_place(session, int(place_id))
    await dialog_manager.next()
    await callback.answer()


async def name_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["name"] = message.text
    await message.delete()
    await dialog_manager.next()


async def add_place_yes_no(
        callback: CallbackQuery, widget: Any,
        dialog_manager: DialogManager, item_id: str, **kwargs
):
    if item_id == NO:
        await dialog_manager.done()
    session = dialog_manager.middleware_data.get("session")
    await orm_add_place(session, dialog_manager.dialog_data)
    await dialog_manager.next()
    await callback.answer()
