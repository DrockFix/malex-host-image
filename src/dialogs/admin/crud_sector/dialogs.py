import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Row, Select
from aiogram_dialog.widgets.text import Const, Jinja, Format

from src.constants import YES_NO
from src.states.admin import AddSector, DeleteSector
from .getters import get_data_sector, get_delete_data_sector
from .handlers import name_selected, add_sector_yes_no, delete_sector_yes_no
from ...common import enable_send_mode

add_sector_dialog = Dialog(
    Window(
        Const("Введите название сектора"),
        MessageInput(name_selected),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddSector.name,
    ),
    Window(
        Const("Вы действительно хотите добавить этот сектор?"),
        Jinja(
            '''
Название: {{sector.name if sector.name else 'Нет данных'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_add_sector_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=add_sector_yes_no,
        ),
        getter=get_data_sector,
        state=AddSector.confirm,
    ),
    Window(
        Const("Сектор добавлен!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        state=AddSector.result,
    ),
)

delete_sector_dialog = Dialog(
    Window(
        Const("Вы действительно хотите удалить сектор?"),
        Jinja(
            '''
Название сектора: {{sector.name if sector.name else 'Нет данных'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_delete_sector_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=delete_sector_yes_no,
        ),
        getter=get_delete_data_sector,
        state=DeleteSector.confirm,
    ),
    Window(
        Const("Сектор удален!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        state=DeleteSector.result,
    )
)