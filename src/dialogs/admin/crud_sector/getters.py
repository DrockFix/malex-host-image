from aiogram_dialog import DialogManager

from src.database.orm_query import orm_get_user_sector


async def get_delete_data_sector(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    sector_id = dialog_manager.start_data["sector"]
    sector = await orm_get_user_sector(session, int(sector_id))
    return {
        "sector": sector
    }


async def get_data_sector(dialog_manager: DialogManager, **kwargs):
    sector = dict()
    sector["name"] = dialog_manager.dialog_data["name"]
    return {
        "sector": sector
    }
