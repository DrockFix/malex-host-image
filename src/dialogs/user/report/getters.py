from datetime import datetime

from aiogram_dialog import DialogManager

from src.database.orm_query import orm_get_types_report, orm_get_places, orm_get_devices, orm_get_type_report, \
    orm_get_device


class Place:
    def __init__(self, name):
        self.name = name


class TypeDevice:
    def __init__(self, name):
        self.name = name


class Device:
    def __init__(self, type, number):
        self.number = number
        self.type = type


async def get_types_report(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    dialog_manager.dialog_data["custom"] = False
    types_report = await orm_get_types_report(session)
    name_types_report = [(name_type_report.id, name_type_report.name, name_type_report.description) for name_type_report in types_report]
    return {
        "types_report": name_types_report
    }


async def get_devices(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    devices = await orm_get_devices(session)
    name_devices = [(name_device.id, name_device.type.name, name_device.number) for name_device in devices]
    return {
        "devices": name_devices
    }


async def get_places(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    places = await orm_get_places(session)
    name_places = [(name_place.id, name_place.name) for name_place in places]
    return {
        "places": name_places
    }


async def get_count_image(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    type_id = dialog_manager.dialog_data["type_id"]
    type_report = await orm_get_type_report(session, type_id)
    count_images = type_report.count_images
    return {
        "count_images": count_images
    }


async def get_data_report(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["user_id"] = dialog_manager.middleware_data["user"].user_id
    session = dialog_manager.middleware_data["session"]
    type_id = dialog_manager.dialog_data["type_id"]
    type_report = await orm_get_type_report(session, type_id)
    report = dict()
    report["user"] = dialog_manager.middleware_data["user"]
    report["type"] = type_report
    if "device_id" in dialog_manager.dialog_data:
        if dialog_manager.dialog_data["device_id"] == 0:
            device = dialog_manager.dialog_data["type_device"] + " " + dialog_manager.dialog_data["number_device"]
        else:
            device_dict = await orm_get_device(session, dialog_manager.dialog_data["device_id"])
            device = device_dict.type.name + " " + device_dict.number
        report["device"] = device
    if "place_id" in dialog_manager.dialog_data:
        report["place"] = dialog_manager.dialog_data["place"]
    report["date"] = datetime.fromisoformat(dialog_manager.dialog_data["date"])
    report["image"] = dialog_manager.dialog_data["image"]
    return {
        "report": report
    }
