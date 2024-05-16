import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, Cancel, Row, Back
from aiogram_dialog.widgets.text import Jinja, Const, Format

from src.constants import YES_NO
from src.states.admin import DeleteDeviceType, AddDeviceType
from .getters import get_delete_data_type_device, get_data_type_device
from .handlers import delete_type_device_yes_no, description_selected, name_selected, add_type_device_yes_no
from src.dialogs.common import enable_send_mode

add_type_device_dialog = Dialog(
    Window(
        Const("Введите название типа устройства"),
        MessageInput(name_selected),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddDeviceType.name,
    ),
    Window(
        Const("Введите описание типа устройства"),
        MessageInput(description_selected),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddDeviceType.description,
    ),
    Window(
        Const("Вы действительно хотите добавить этот тип устройства?"),
        Jinja(
            '''
Название: {{type_device.name if type_device.name else 'Нет данных'}}
Описание: {{type_device.description if type_device.description else 'Нет данных'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_add_type_device_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=add_type_device_yes_no,
        ),
        getter=get_data_type_device,
        state=AddDeviceType.confirm,
    ),
    Window(
        Const("Тип устройства добавлен!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        state=AddDeviceType.result,
    ),
)

delete_type_device_dialog = Dialog(
    Window(
        Const("Вы действительно хотите удалить тип устройства?"),
        Jinja(
            '''
Название: {{type_device.name if type_device.name else 'Нет данных'}}
Описание: {{type_device.description if type_device.description else 'Нет данных'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_delete_type_device_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=delete_type_device_yes_no,
        ),
        getter=get_delete_data_type_device,
        state=DeleteDeviceType.confirm,
    ),
    Window(
        Const("Тип устройства удален!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        state=DeleteDeviceType.result,
    )
)