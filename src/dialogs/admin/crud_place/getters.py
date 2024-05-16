from aiogram_dialog import DialogManager

from src.database.orm_query import orm_get_place


async def get_delete_data_place(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    place_id = dialog_manager.start_data["place"]
    place = await orm_get_place(session, int(place_id))
    return {
        "place": place
    }


async def get_data_place(dialog_manager: DialogManager, **kwargs):
    place = dict()
    place["name"] = dialog_manager.dialog_data["name"]
    return {
        "place": place
    }
