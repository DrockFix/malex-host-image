from aiogram_dialog import DialogManager

from src.database.orm_query import orm_get_user, orm_get_user_sectors


async def get_delete_data_user(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session"]
    user_id = dialog_manager.start_data["user"]
    user = await orm_get_user(session, int(user_id))
    return {
        "user": user

    }


async def get_sectors(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session")
    sectors = await orm_get_user_sectors(session)
    return {
        "sectors": sectors,
        "count": len(sectors),
    }


async def get_data_user(dialog_manager: DialogManager, **kwargs):
    user = dict()
    user["user_id"] = dialog_manager.dialog_data["user_id"]
    user["first_name"] = dialog_manager.dialog_data["first_name"]
    user["last_name"] = dialog_manager.dialog_data["last_name"]
    user["sectors"] = dialog_manager.dialog_data["sectors"]
    user["phone"] = dialog_manager.dialog_data["phone"]
    return {
        "user": user
    }
