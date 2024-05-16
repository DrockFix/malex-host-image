import operator

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, Cancel, Select, Back, ScrollingGroup, NumberedPager
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from src.states.admin import AddPlan
from .getters import get_sectors, get_data_sector_name, \
    get_data_sector_file, get_main
from .handlers import on_sector_selected, file_selected, add_plan_yes_no
from ...common import enable_send_mode
from ....constants import YES_NO

add_plan_dialog = Dialog(
    Window(
        DynamicMedia("photo"),
        Const("Выберите сектор"),
        ScrollingGroup(
            Select(
                Format("{item[0]}"),  # Изменено здесь
                id="s_sector",
                item_id_getter=operator.itemgetter(0),
                items="name_sectors",
                on_click=on_sector_selected,
            ),
            id="group_s_sector",
            width=2,
            height=2,
        ),
        NumberedPager(
            scroll="group_s_sector",
        ),
        Cancel(Const("❌ Отмена")),
        state=AddPlan.name,
        getter=(get_sectors, get_main),
        preview_data=(get_sectors, get_main),
    ),
    Window(
        DynamicMedia("photo"),
        Multi(
            Format("Сектор: {sector_name}"),
            Const("Прикрепите файл с графиком в формате PDF"),
        ),
        MessageInput(file_selected, content_types=[ContentType.DOCUMENT]),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddPlan.document,
        getter=(get_data_sector_name, get_main),
        preview_data=(get_data_sector_name, get_main),
    ),
    Window(
        Format("Сектор: {sector_name}"),
        DynamicMedia("sector_file"),
        Const("Все верно?"),
        Select(
            Format("{item[0]}"),
            id="s_yes_no_plan",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=add_plan_yes_no,
        ),
        getter=get_data_sector_file,
        state=AddPlan.confirm,
        preview_data=get_data_sector_file
    ),
    Window(
        Format("Сектор: {sector_name}"),
        DynamicMedia("sector_file"),
        Const("Данные сохранены!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        getter=get_data_sector_file,
        state=AddPlan.result,
        preview_data=get_data_sector_file

    )
)

