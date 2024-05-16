from aiogram_dialog import DialogManager

from src.database.orm_query import orm_get_type_device


async def get_delete_data_type_device(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    type_device_id = dialog_manager.start_data["type_device"]
    type_device = await orm_get_type_device(session, int(type_device_id))
    return {
        "type_device": type_device
    }


async def get_data_type_device(dialog_manager: DialogManager, **kwargs):
    type_device = dict()
    type_device["name"] = dialog_manager.dialog_data["name"]
    type_device["description"] = dialog_manager.dialog_data["description"]
    return {
        "type_device": type_device
    }
