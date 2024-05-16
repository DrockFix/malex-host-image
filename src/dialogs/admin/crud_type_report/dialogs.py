import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, Cancel, Row, Back, Multiselect, Button
from aiogram_dialog.widgets.text import Jinja, Const, Format

from src.constants import YES_NO
from src.states.admin import DeleteTypeReport, AddTypeReport
from .handlers import (delete_type_report_yes_no, count_image_selected, name_selected, description_selected,
                       settings_selected, add_type_report_yes_no)
from src.dialogs.common import enable_send_mode
from .getters import get_delete_data_type_report, get_settings, get_data_type_report

add_type_report_dialog = Dialog(
    Window(
        Const("Введите название типа отчета"),
        MessageInput(name_selected),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddTypeReport.name,
    ),
    Window(
        Const("Введите описание типа отчета"),
        MessageInput(description_selected),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddTypeReport.description
    ),
    Window(
        Const("Укажите настройки отчета"),
        Multiselect(
            Format("✓ {item[0]}"),
            Format("{item[0]}"),
            id="m_settings_type_report",
            item_id_getter=operator.itemgetter(1),
            items="settings",
        ),
        Button(
            Const("Дальше"),
            id="s_add_settings",
            on_click=settings_selected
        ),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddTypeReport.settings,
        getter=get_settings
    ),
    Window(
        Const("Введите число требуемых изображений"),
        MessageInput(count_image_selected),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddTypeReport.count_image,
    ),
    Window(
        Const("Вы действительно хотите добавить этот тип отчета?"),
        Jinja(
            '''
Название: {{type_report.name if type_report.name else 'Нет данных'}}
Поле комплекса: {{'Да' if type_report.on_complex else 'Нет'}}
Поле места установки: {{'Да' if type_report.on_place else 'Нет'}}
Количество изображений: {{type_report.count_images if type_report.count_images else 'Нет данных'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_add_type_report_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=add_type_report_yes_no,
        ),
        getter=get_data_type_report,
        state=AddTypeReport.confirm,
    ),
    Window(
        Const("Тип отчета добавлен!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        state=AddTypeReport.result,
    ),
)

delete_type_report_dialog = Dialog(
    Window(
        Const("Вы действительно хотите удалить тип отчета?"),
        Jinja(
            '''
Название: {{type_report.name if type_report.name else 'Нет данных'}}
Поле комплекса: {{'Да' if type_report.on_complex else 'Нет'}}
Поле места установки: {{'Да' if type_report.on_place else 'Нет'}}
Количество изображений: {{type_report.count_images if type_report.count_images else 'Нет данных'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_delete_type_report_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=delete_type_report_yes_no,
        ),
        getter=get_delete_data_type_report,
        state=DeleteTypeReport.confirm
    ),
    Window(
        Const("Тип отчета удален!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        state=DeleteTypeReport.result,
    )
)
