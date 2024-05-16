from aiogram import Router

from . import admin
from .admin.add_plan.dialogs import add_plan_dialog
from .admin.crud_device.dialogs import delete_device_dialog, add_device_dialog
from .admin.crud_place.dialogs import add_place_dialog, delete_place_dialog
from .admin.crud_sector.dialogs import delete_sector_dialog, add_sector_dialog
from .admin.crud_type_device.dialogs import add_type_device_dialog, delete_type_device_dialog
from .admin.crud_type_report.dialogs import delete_type_report_dialog, add_type_report_dialog
from .admin.crud_user.dialogs import delete_user_dialog, add_user_dialog
from .admin.main_menu.dialogs import main_menu_dialog
from .user.main_menu.dialogs import main_menu_user
from .user.report.dialogs import report_dialog

dialog_router = Router()
dialog_router.include_routers(
    add_plan_dialog,
    main_menu_dialog,
    main_menu_user,
    delete_device_dialog,
    add_device_dialog,
    add_place_dialog,
    delete_place_dialog,
    delete_sector_dialog,
    add_sector_dialog,
    add_type_device_dialog,
    delete_type_device_dialog,
    add_type_report_dialog,
    delete_type_report_dialog,
    report_dialog,
    add_user_dialog,
    delete_user_dialog
)

