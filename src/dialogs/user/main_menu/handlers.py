from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def get_plan(callback: CallbackQuery, button: Button,
                   dialog_manager: DialogManager):
    user = dialog_manager.middleware_data.get("user")
    plan_id = user.type.file
    await callback.message.answer_document(document=plan_id, caption="user.type.name")
