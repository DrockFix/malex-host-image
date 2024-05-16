import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, Cancel, Row, Back
from aiogram_dialog.widgets.text import Jinja, Format, Const

from src.constants import YES_NO
from .getters import get_delete_data_place, get_data_place
from .handlers import delete_place_yes_no, name_selected, add_place_yes_no
from src.dialogs.common import enable_send_mode
from src.states.admin import DeletePlace, AddPlace

add_place_dialog = Dialog(
    Window(
        Const("Введите название места"),
        MessageInput(name_selected),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddPlace.name,
    ),
    Window(
        Const("Вы действительно хотите добавить это место установки?"),
        Jinja(
            '''
Название: {{place.name if place.name else 'Нет данных'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_add_place_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=add_place_yes_no,
        ),
        getter=get_data_place,
        state=AddPlace.confirm,
    ),
    Window(
        Const("Место установки добавлено!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        state=AddPlace.result,
    ),
)

delete_place_dialog = Dialog(
    Window(
        Const("Вы действительно хотите удалить место установки?"),
        Jinja(
            '''
Название места: {{place.name if place.name else 'Нет данных'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_delete_place_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=delete_place_yes_no,
        ),
        getter=get_delete_data_place,
        state=DeletePlace.confirm,
    ),
    Window(
        Const("Место установки удалено!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        state=DeletePlace.result,
    )
)
