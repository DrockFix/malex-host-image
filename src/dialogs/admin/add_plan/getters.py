from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from ....database.orm_query import orm_get_user_sectors, orm_get_banner


async def get_sectors(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session")
    sectors = await orm_get_user_sectors(session)
    name_sectors = [(sector.name, sector.id) for sector in sectors]
    return {
        "name_sectors": name_sectors,
        "count": len(name_sectors),
    }


async def get_data_sector_name(dialog_manager: DialogManager, **kwargs):
    sector_name = dialog_manager.dialog_data.get("sector_name")
    return {
        "sector_name": sector_name,
    }


async def get_data_sector_file(dialog_manager: DialogManager, **kwargs):
    sector_name = dialog_manager.dialog_data.get("sector_name")
    sector_file_id = dialog_manager.dialog_data.get("file")
    sector_file = MediaAttachment(ContentType.DOCUMENT, file_id=MediaId(sector_file_id))
    return {
        "sector_name": sector_name,
        "sector_file": sector_file,
    }


async def get_main(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session")
    banner = await orm_get_banner(session, "admin_menu")

    if banner.image.startswith('./'):
        photo = MediaAttachment(ContentType.PHOTO, path=banner.image)
    else:
        photo = MediaAttachment(ContentType.PHOTO, file_id=MediaId(banner.image))
    return {
        "photo": photo,
        "caption": banner.description
    }
