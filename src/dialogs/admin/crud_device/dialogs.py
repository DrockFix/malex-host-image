import operator

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel, Back, Row
from aiogram_dialog.widgets.text import Const, Format, Jinja

from src.constants import YES_NO
from src.states.admin import AddDevice, DeleteDevice
from .getters import get_data_device, get_types_device, get_delete_data_device, get_data_type_device
from .handlers import delete_device_yes_no, on_type_device_selected, number_selected, add_device_yes_no
from ...common import enable_send_mode

add_device_dialog = Dialog(
    Window(
        Const("Выберите тип устройства"),
        ScrollingGroup(
            Select(
                Format("{item[1]}"),  # Изменено здесь
                id="s_type_device",
                item_id_getter=operator.itemgetter(0),
                items="types_devices",
                on_click=on_type_device_selected,
            ),
            id="group_s_types_devices",
            width=2,
            height=2,
        ),
        state=AddDevice.type_id,
        getter=get_types_device
    ),
    Window(
        Const("Введите номер устройства"),
        Jinja(
            '''
Тип устройства: {{device.type.name if device.type.name else 'Нет данных'}}
'''
        ),
        MessageInput(number_selected),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddDevice.number,
        getter=get_data_type_device,
    ),
    Window(
        Const("Вы действительно хотите добавить это устройство?"),
        Jinja(
            '''
Тип устройства: {{device.type.name if device.type.name else 'Нет данных'}}
Номер: {{device.number if device.number else 'Нет данных'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_add_device_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=add_device_yes_no,
        ),
        getter=get_data_device,
        state=AddDevice.confirm,
    ),
    Window(
        Const("Устройство добавлено!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        state=AddDevice.result,
    ),
)

delete_device_dialog = Dialog(
    Window(
        Const("Вы действительно хотите удалить устройство?"),
        Jinja(
            '''
Тип устройства: {{device.type.name if device.type.name else 'Нет данных'}}
Номер: {{device.number if device.number else 'Нет данных'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_delete_device_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=delete_device_yes_no,
        ),
        getter=get_delete_data_device,
        state=DeleteDevice.confirm,
    ),
    Window(
            Const("Устройство удалено!"),
            Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
            state=DeleteDevice.result,

    )
)
