from aiogram_dialog import DialogManager

from ....database.orm_query import orm_get_devices, orm_get_places, orm_get_user_sectors, \
    orm_get_types_device, orm_get_types_report, orm_get_users


async def get_devices(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session")
    devices = await orm_get_devices(session)
    return {
        "devices": devices,
        "count": len(devices),
    }


async def get_places(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session")
    places = await orm_get_places(session)
    return {
        "places": places,
        "count": len(places),
    }


async def get_sectors(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session")
    sectors = await orm_get_user_sectors(session)
    return {
        "sectors": sectors,
        "count": len(sectors),
    }


async def get_types_devices(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session")
    types_devices = await orm_get_types_device(session)
    return {
        "types_devices": types_devices,
        "count": len(types_devices),
    }


async def get_types_reports(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session")
    types_reports = await orm_get_types_report(session)
    return {
        "types_reports": types_reports,
        "count": len(types_reports),
    }


async def get_users(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session")
    users = await orm_get_users(session)
    return {
        "users": users,
        "count": len(users),
    }
