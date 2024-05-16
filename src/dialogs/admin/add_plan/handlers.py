from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

from src.constants import NO
from ....database.orm_query import orm_add_plan_sector
from ....states.admin import AddPlan


async def on_sector_selected(callback: CallbackQuery, widget: Any,
                             dialog_manager: DialogManager, item_name: str):
    dialog_manager.dialog_data["sector_name"] = item_name
    await dialog_manager.next()


async def file_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["file"] = message.document.file_id
    await message.delete()
    await dialog_manager.next()


async def add_plan_yes_no(
        callback: CallbackQuery, widget: Any,
        dialog_manager: DialogManager, item_id: str, **kwargs
):
    if item_id == NO:
        await dialog_manager.switch_to(AddPlan.document)
        return
    file = dialog_manager.dialog_data.get("file"),
    sector_name = dialog_manager.dialog_data.get("sector_name")

    session = dialog_manager.middleware_data.get("session")
    await orm_add_plan_sector(session, sector_name, file[0])
    await dialog_manager.next()
    await callback.answer()
