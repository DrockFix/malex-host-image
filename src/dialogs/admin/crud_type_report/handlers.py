from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

from src.constants import NO
from src.database.orm_query import orm_delete_type_report, orm_add_type_report


async def delete_type_report_yes_no(
        callback: CallbackQuery, widget: Any,
        dialog_manager: DialogManager, item_id: str, **kwargs
):
    if item_id == NO:
        await dialog_manager.done()
    type_report_id = dialog_manager.start_data["type_report"]
    session = dialog_manager.middleware_data.get("session")
    await orm_delete_type_report(session, int(type_report_id))
    await dialog_manager.next()
    await callback.answer()


async def add_type_report_yes_no(
        callback: CallbackQuery, widget: Any,
        dialog_manager: DialogManager, item_id: str, **kwargs
):
    if item_id == NO:
        await dialog_manager.done()
    session = dialog_manager.middleware_data.get("session")
    await orm_add_type_report(session, dialog_manager.dialog_data)
    await dialog_manager.next()
    await callback.answer()


async def name_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["name"] = message.text
    await message.delete()
    await dialog_manager.next()


async def description_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["description"] = message.text
    await message.delete()
    await dialog_manager.next()


async def count_image_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["count_images"] = int(message.text)
    await message.delete()
    await dialog_manager.next()


async def settings_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    settings_type_report = dialog_manager.find("m_settings_type_report")
    settings_list = settings_type_report.get_checked()
    dialog_manager.dialog_data["on_complex"] = False
    dialog_manager.dialog_data["on_place"] = False
    for item in settings_list:
        dialog_manager.dialog_data[item] = True
    await dialog_manager.next()
