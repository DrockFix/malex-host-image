from aiogram_dialog import DialogManager

from src.database.orm_query import orm_get_type_report


async def get_settings(**kwargs):
    settings = [
        ("Выбор устройства", 'on_complex'),
        ("Выбор места", 'on_place'),
    ]
    return {
        "settings": settings,
        "count": len(settings),
    }


async def get_delete_data_type_report(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    type_report_id = dialog_manager.start_data["type_report"]
    type_report = await orm_get_type_report(session, int(type_report_id))
    return {
        "type_report": type_report
    }


async def get_data_type_report(dialog_manager: DialogManager, **kwargs):
    type_report = dict()
    type_report["name"] = dialog_manager.dialog_data["name"]
    type_report["on_complex"] = dialog_manager.dialog_data["on_complex"]
    type_report["on_place"] = dialog_manager.dialog_data["on_place"]
    type_report["count_images"] = dialog_manager.dialog_data["count_images"]
    return {
        "type_report": type_report
    }
