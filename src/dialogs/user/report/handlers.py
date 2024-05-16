import asyncio
import os
from datetime import datetime
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram_dialog import DialogManager

from src.constants import NO
from src.database.orm_query import orm_get_type_report, orm_add_report, orm_get_place, orm_get_device
from src.states.user import AddReport
from src.utils.export_files import save_report


async def on_type_report_selected(callback: CallbackQuery, widget: Any,
                                  dialog_manager: DialogManager, item_id: str):
    session = dialog_manager.middleware_data["session"]
    type_report = await orm_get_type_report(session, int(item_id))
    dialog_manager.dialog_data["type_id"] = type_report.id
    dialog_manager.dialog_data["type_name"] = type_report.name
    if type_report.on_place:
        await dialog_manager.switch_to(AddReport.place_id)
    elif type_report.on_complex:
        await dialog_manager.switch_to(AddReport.complex_id)
    else:
        await dialog_manager.switch_to(AddReport.date)


async def on_device_selected(callback: CallbackQuery, widget: Any,
                             dialog_manager: DialogManager, item_id: str):
    session = dialog_manager.middleware_data["session"]
    device = await orm_get_device(session, int(item_id))
    dialog_manager.dialog_data["device_id"] = device.id
    await dialog_manager.next()


async def on_place_selected(callback: CallbackQuery, widget: Any,
                            dialog_manager: DialogManager, item_id: str):
    session = dialog_manager.middleware_data["session"]
    type_id = dialog_manager.dialog_data["type_id"]
    type_report = await orm_get_type_report(session, type_id)
    place = await orm_get_place(session, int(item_id))
    dialog_manager.dialog_data["place_id"] = place.id
    if type_report.on_complex:
        await dialog_manager.switch_to(AddReport.complex_id)
    else:
        await dialog_manager.switch_to(AddReport.date)


async def on_device_text(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    device = message.text.split(sep=' ')
    dialog_manager.dialog_data["custom"] = True
    dialog_manager.dialog_data["device_id"] = 0
    dialog_manager.dialog_data["type_device"] = device[0]
    dialog_manager.dialog_data["number_device"] = device[1]
    await dialog_manager.next()


async def on_place_text(message: Message, widget: Any,
                        dialog_manager: DialogManager):
    dialog_manager.current_context()
    session = dialog_manager.middleware_data["session"]
    type_id = dialog_manager.dialog_data["type_id"]
    type_report = await orm_get_type_report(session, type_id)
    dialog_manager.dialog_data["custom"] = True
    dialog_manager.dialog_data["place_id"] = 0
    dialog_manager.dialog_data["place"] = message.text
    if type_report.on_complex:
        await dialog_manager.switch_to(AddReport.complex_id)
    else:
        await dialog_manager.switch_to(AddReport.date)


async def on_date_selected(callback: CallbackQuery, widget: Any,
                           dialog_manager: DialogManager, selected_date):
    dialog_manager.dialog_data["date"] = selected_date.isoformat()
    await dialog_manager.next()


async def back_report(callback: CallbackQuery, widget: Any,
                      dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    type_id = dialog_manager.dialog_data["type_id"]
    type_report = await orm_get_type_report(session, type_id)
    if type_report.on_place:
        await dialog_manager.switch_to(AddReport.place_id)
    else:
        await dialog_manager.switch_to(AddReport.type_report)


async def image_selected(message: Message, widget: Any, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    type_id = dialog_manager.dialog_data["type_id"]
    type_report = await orm_get_type_report(session, type_id)
    dialog_manager.dialog_data.setdefault("image", []).append(
        message.photo[-1].file_id,
    )
    await message.delete()
    if len(dialog_manager.dialog_data["image"]) == type_report.count_images:
        await dialog_manager.next()


async def send_report_yes_no(
        callback: CallbackQuery, widget: Any,
        dialog_manager: DialogManager, item_id: str, **kwargs,
):
    if item_id == NO:
        await dialog_manager.done()
    session = dialog_manager.middleware_data["session"]
    type_report = await orm_get_type_report(session, dialog_manager.dialog_data["type_id"])
    if "device_id" in dialog_manager.dialog_data:
        if dialog_manager.dialog_data["device_id"] == 0:
            device_str = (dialog_manager.dialog_data["type_device"] + " "
                          + dialog_manager.dialog_data["number_device"])
        else:
            device = await orm_get_device(session, dialog_manager.dialog_data["device_id"])
            device_str = device.type.name + " " + device.number
    else:
        device_str = None
    if "place_id" in dialog_manager.dialog_data:
        place = dialog_manager.dialog_data["place"]
    else:
        place = None

    date = datetime.fromisoformat(dialog_manager.dialog_data["date"])

    await save_report(callback.bot, dialog_manager.dialog_data)
    if not dialog_manager.dialog_data["custom"]:
        await orm_add_report(session, dialog_manager.dialog_data)
    album_builder = MediaGroupBuilder(
        caption=f"Пользователь: {callback.from_user.full_name}\n"
                f"Тип: {type_report.name if type_report else 'Нет данных'}\n"
                f"Место установки: {place if place else 'Нет данных'}\n"
                f"Устройство: {device_str if device_str else 'Нет данных'}\n"
                f"Дата: {date if date else 'Нет данных'}"
    )
    for photo_id in dialog_manager.dialog_data["image"]:
        album_builder.add_photo(
            media=photo_id
        )
    await callback.bot.send_media_group(
        chat_id=os.getenv("CHAT_ID"),
        message_thread_id=int(os.getenv("CHAT_THREAD_REPORT")) if os.getenv("CHAT_THREAD_REPORT") else None,
        media=album_builder.build()
   )
    await dialog_manager.next()
