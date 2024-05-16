from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

from src.constants import NO
from src.database.orm_query import orm_delete_device, orm_get_type_device, orm_add_device


async def on_type_device_selected(callback: CallbackQuery, widget: Any,
                                  dialog_manager: DialogManager, item_id: str):
    session = dialog_manager.middleware_data["session"]
    type_device = await orm_get_type_device(session, int(item_id))
    dialog_manager.dialog_data["type_id"] = type_device.id
    await dialog_manager.next()


async def number_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["number"] = message.text
    await message.delete()
    await dialog_manager.next()


async def delete_device_yes_no(
        callback: CallbackQuery, widget: Any,
        dialog_manager: DialogManager, item_id: str, **kwargs
):
    if item_id == NO:
        await dialog_manager.done()
    device_id = dialog_manager.start_data["device"]
    session = dialog_manager.middleware_data.get("session")
    await orm_delete_device(session, int(device_id))
    await dialog_manager.next()
    await callback.answer()


async def add_device_yes_no(
        callback: CallbackQuery, widget: Any,
        dialog_manager: DialogManager, item_id: str, **kwargs
):
    if item_id == NO:
        await dialog_manager.done()
    session = dialog_manager.middleware_data.get("session")
    await orm_add_device(session, dialog_manager.dialog_data)
    await dialog_manager.next()
    await callback.answer()
