from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from src.database.orm_query import orm_get_banner


async def get_main(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session")
    current_state = kwargs['aiogd_context'].state
    current_state_name = current_state._state
    banner = await orm_get_banner(session, current_state_name)

    if banner.image.startswith('./'):
        photo = MediaAttachment(ContentType.PHOTO, path=banner.image)
    else:
        photo = MediaAttachment(ContentType.PHOTO, file_id=MediaId(banner.image))
    return {
        "photo": photo,
        "caption": banner.description
    }


async def get_user(dialog_manager: DialogManager, **kwargs):
    return {
        "full_name": dialog_manager.middleware_data["event_from_user"].full_name
    }



