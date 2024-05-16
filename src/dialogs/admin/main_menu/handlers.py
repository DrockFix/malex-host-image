from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from src.states.admin import DeleteDevice, DeletePlace, DeleteUser, DeleteDeviceType, DeleteTypeReport, DeleteSector


async def delete_device(callback: CallbackQuery, widget: Any,
                        dialog_manager: DialogManager, item: int):
    await dialog_manager.start(DeleteDevice.confirm, data={"device": item})


async def delete_type_device(callback: CallbackQuery, widget: Any,
                             dialog_manager: DialogManager, item: int):
    await dialog_manager.start(DeleteDeviceType.confirm, data={"type_device": item})


async def delete_type_report(callback: CallbackQuery, widget: Any,
                             dialog_manager: DialogManager, item: int):
    await dialog_manager.start(DeleteTypeReport.confirm, data={"type_report": item})


async def delete_sector(callback: CallbackQuery, widget: Any,
                        dialog_manager: DialogManager, item: int):
    await dialog_manager.start(DeleteSector.confirm, data={"sector": item})


async def delete_place(callback: CallbackQuery, widget: Any,
                       dialog_manager: DialogManager, item: int):
    await dialog_manager.start(DeletePlace.confirm, data={"place": item})


async def delete_user(callback: CallbackQuery, widget: Any,
                      dialog_manager: DialogManager, item: int):
    await dialog_manager.start(DeleteUser.confirm, data={"user": item})
