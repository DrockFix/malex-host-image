import operator

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Select, ScrollingGroup, Calendar, Row, Back, SwitchTo, Button
from aiogram_dialog.widgets.text import Const, Jinja, Format, Case, Multi, List

from src.constants import YES_NO
from src.dialogs.common import enable_send_mode
from .getters import get_types_report, get_devices, get_places, get_data_report, get_count_image
from .handlers import on_type_report_selected, on_device_selected, on_place_selected, on_date_selected, \
    send_report_yes_no, image_selected, on_device_text, on_place_text, back_report
from src.states.user import AddReport

report_dialog = Dialog(
    Window(
        Const("Выберите тип отчета"),
        List(
            Jinja(
                '''
{{item[1]}}: {{item[2] if item[2] else "Нет описания"}}
'''
            ),
            items="types_report",
            id="l_type_report",
        ),
        ScrollingGroup(
            Select(
                Format("{item[1]}"),  # Изменено здесь
                id="s_type_report",
                item_id_getter=operator.itemgetter(0),
                items="types_report",
                on_click=on_type_report_selected,
            ),
            id="group_s_types_report",
            width=2,
            height=2,
        ),
        Cancel(Const("❌ Отмена")),
        state=AddReport.type_report,
        getter=get_types_report
    ),
    Window(
        Const("Введите место установки или выберите из предложенных."),
        ScrollingGroup(
            Select(
                Format("{item[1]}"),  # Изменено здесь
                id="s_place",
                item_id_getter=operator.itemgetter(0),
                items="places",
                on_click=on_place_selected,
            ),
            id="group_s_places",
            width=1,
            height=4,
        ),
        MessageInput(on_place_text),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddReport.place_id,
        getter=get_places
    ),
    Window(
        Const("Введите название устройства или выберите из предложенных."),
        ScrollingGroup(
            Select(
                Format("{item[1]} {item[2]}"),
                id="s_device",
                item_id_getter=operator.itemgetter(0),
                items="devices",
                on_click=on_device_selected,
            ),
            id="group_s_devices",
            width=1,
            height=4,
        ),
        MessageInput(on_device_text),
        Row(
            Button(
                Const("🔙 Назад"),
                id="back_report",
                on_click=back_report,
            ),
            Cancel(Const("❌ Отмена"))
        ),
        state=AddReport.complex_id,
        getter=get_devices
    ),
    Window(
        Const("Укажите дату отправки отчета"),
        Calendar(
            id='calendar',
            on_click=on_date_selected,
        ),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddReport.date
    ),
    Window(
        Format("Отправьте {count_images} изображения одним сообщением"),
        MessageInput(image_selected, content_types=[ContentType.PHOTO]),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddReport.image,
        getter=get_count_image
    ),
    Window(
        Const("Вы действительно хотите отправить этот отчет?"),
        Jinja(
            '''
Пользователь:{{report.user.first_name}} {{report.user.last_name}}
Тип: {{report.type.name if report.type else 'Нет данных'}}
Место установки: {{report.place.name if report.place else 'Нет данных'}}
Устройство: {{ report.device if report.device else 'Нет данных'}}
Дата: {{report.date if report.date else 'Нет данных'}}
Изображения: {{report.image if report.image else 'Нет данных'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_send_report_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=send_report_yes_no,
        ),
        getter=get_data_report,
        state=AddReport.confirm,
    ),
    Window(
        Const("Отчет отправлен!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        state=AddReport.result,
    ),
)
