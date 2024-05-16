from aiogram_dialog import DialogManager

from src.database.orm_query import orm_get_device, orm_get_types_device, orm_get_type_device


async def get_delete_data_device(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    device_id = dialog_manager.start_data["device"]
    device = await orm_get_device(session, int(device_id))
    return {
        "device": device
    }


async def get_data_type_device(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    type_id = dialog_manager.dialog_data["type_id"]
    type_device = await orm_get_type_device(session, int(type_id))
    device = dict()
    device["type"] = type_device
    return {
        "device": device
    }


async def get_data_device(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    type_id = dialog_manager.dialog_data["type_id"]
    type_device = await orm_get_type_device(session, int(type_id))
    device = dict()
    device["type"] = type_device
    device["number"] = dialog_manager.dialog_data["number"]
    return {
        "device": device
    }


async def get_types_device(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    types_devices = await orm_get_types_device(session)
    name_types_devices = [(name_type.id, name_type.name) for name_type in types_devices]
    return {
        "types_devices": name_types_devices
    }
