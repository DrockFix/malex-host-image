from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.common import sync_scroll
from aiogram_dialog.widgets.kbd import Start, SwitchTo, Row, ScrollingGroup, NumberedPager, Select
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const, Jinja, List, Case

from src.states.admin import *
from .getters import get_sectors, get_types_devices, \
    get_types_reports, get_users, get_places, get_devices
from .handlers import delete_device, delete_place, delete_sector, delete_user, delete_type_report, delete_type_device
from ...common import get_main

main_menu_dialog = Dialog(
    Window(
        DynamicMedia("photo"),
        Format("{caption}"),
        SwitchTo(
            Const("Статистика"),
            id="stat",
            state=AdminMenu.stat,
        ),
        Start(
            Const("План-график"),
            id="plan",
            state=AddPlan.name
        ),
        SwitchTo(
            Const("Справочники"),
            id="list_dict",
            state=AdminMenu.dict
        ),
        SwitchTo(
            Const("Настройки"),
            id="settings",
            state=AdminMenu.settings,
        ),
        state=AdminMenu.menu,
        getter=get_main,
    ),
    Window(
        DynamicMedia("photo"),
        Format("{caption}"),
        SwitchTo(Const("🔙 Назад"),
                 id="back_main_menu",
                 state=AdminMenu.menu),
        state=AdminMenu.settings,
        getter=get_main,
    ),
    Window(
        DynamicMedia("photo"),
        Format("{caption}"),
        SwitchTo(Const("🔙 Назад"),
                 id="back_main_menu",
                 state=AdminMenu.menu),
        state=AdminMenu.stat,
        getter=get_main,
    ),
    Window(
        DynamicMedia("photo"),
        Format("{caption}"),
        SwitchTo(
            Const("Типы отчетов"),
            id="type_report_list",
            state=AdminMenu.dict_type_report
        ),
        SwitchTo(
            Const("Пользователи"),
            id="user_list",
            state=AdminMenu.dict_user
        ),
        Row(
            SwitchTo(
                Const("Типы комплексов"),
                id="type_device_list",
                state=AdminMenu.dict_type_device
            ),
            SwitchTo(
                Const("Места установки"),
                id="place_list",
                state=AdminMenu.dict_place
            ),
        ),
        Row(
            SwitchTo(
                Const("Сектора"),
                id="sector_list",
                state=AdminMenu.dict_sector
            ),
            SwitchTo(
                Const("Комплексы"),
                id="device_list",
                state=AdminMenu.dict_device
            ),
        ),
        SwitchTo(Const("🔙 Назад"),
                 id="back_main_menu",
                 state=AdminMenu.menu),
        state=AdminMenu.dict,
        getter=get_main,
    ),
    # Справочники
    Window(
        DynamicMedia("photo"),
        Case(
            {
                0: Const("😔 Нет данных о комплексах"),
                ...: List(
                    Jinja(
                        '''
Тип устройства: {{item.type.name if item.type.name else 'Нет данных'}}
Номер: {{item.number if item.number else 'Нет данных'}}
    '''
                    ),
                    items="devices",
                    id="list_devices",
                    page_size=1,
                    on_page_changed=sync_scroll("group_s_delete_device")
                ),
            },
            selector="count"
        ),
        ScrollingGroup(
            Select(
                Const("❌ Удалить устройство"),
                id="delete_device_button",
                item_id_getter=lambda x: x.id,
                items="devices",
                on_click=delete_device
            ),
            id="group_s_delete_device",
            width=1,
            height=1,
            hide_pager=True
        ),
        NumberedPager(
            scroll="list_devices"
        ),
        Row(
            Start(
                Const("➕ Добавить устройство"),
                id="add_device",
                state=AddDevice.type_id
            ),
            SwitchTo(Const("🔙 Назад"), id="back_dicts", state=AdminMenu.dict)
        ),
        state=AdminMenu.dict_device,
        getter=(get_devices, get_main)
    ),
    Window(
        DynamicMedia("photo"),
        Case(
            {
                0: Const("Нету данных о местах установки"),
                ...: List(
                    Jinja(
                        '''
Место установки: {{item.name if item.name else 'Нет данных'}}
'''
                    ),
                    items="places",
                    id="list_places",
                    page_size=1,
                    on_page_changed=sync_scroll("group_s_delete_place")
                ),
            },
            selector="count"
        ),
        ScrollingGroup(
            Select(
                Const("❌ Удалить место"),
                id="delete_place_button",
                item_id_getter=lambda x: x.id,
                items="places",
                on_click=delete_place
            ),
            id="group_s_delete_place",
            width=1,
            height=1,
            hide_pager=True
        ),
        NumberedPager(
            scroll="list_places"
        ),
        Row(
            Start(
                Const("➕ Добавить место"),
                id="add_place",
                state=AddPlace.name
            ),
            SwitchTo(Const("🔙 Назад"), id="back_dicts", state=AdminMenu.dict)
        ),
        state=AdminMenu.dict_place,
        getter=(get_places, get_main)
    ),
    Window(
        DynamicMedia("photo"),
        Case(
            {
                0: Const("Нету данных о секторах"),
                ...: List(
                    Jinja(
                        '''
Cектор: {{item.name if item.name else 'Нет данных'}}
'''
                    ),
                    items="sectors",
                    id="list_sectors",
                    page_size=1,
                    on_page_changed=sync_scroll("group_s_delete_sectors")
                )
            },
            selector="count"
        ),
        ScrollingGroup(
            Select(
                Const("❌ Удалить сектор"),
                id="delete_sector_button",
                item_id_getter=lambda x: x.id,
                items="sectors",
                on_click=delete_sector
            ),
            id="group_s_delete_sectors",
            width=1,
            height=1,
            hide_pager=True
        ),
        NumberedPager(
            scroll="list_sectors",
        ),
        Row(
            Start(
                Const("➕ Добавить сектор"),
                id="add_sector",
                state=AddSector.name
            ),
            SwitchTo(Const("🔙 Назад"), id="back_dicts", state=AdminMenu.dict)
        ),
        state=AdminMenu.dict_sector,
        getter=(get_sectors, get_main)
    ),
    Window(
        DynamicMedia("photo"),
        Case(
            {
                0: Const("Нету данных о типах устройств"),
                ...: List(
                    Jinja(
                        '''
Название: {{item.name if item.name else 'Нет данных'}}
Описание: {{item.description if item.description else 'Нет данных'}}
'''
                    ),
                    items="types_devices",
                    id="list_types_devices",
                    page_size=1,
                    on_page_changed=sync_scroll("group_s_delete_types_devices")
                )
            },
            selector="count",
        ),
        ScrollingGroup(
            Select(
                Const("❌ Удалить тип устройства"),
                id="delete_type_device_button",
                item_id_getter=lambda x: x.id,
                items="types_devices",
                on_click=delete_type_device
            ),
            id="group_s_delete_types_devices",
            width=1,
            height=1,
            hide_pager=True
        ),
        NumberedPager(
            scroll="list_types_devices",
        ),
        Row(
            Start(
                Const("➕ Добавить тип устройства"),
                id="add_type_device",
                state=AddDeviceType.name
            ),
            SwitchTo(Const("🔙 Назад"), id="back_dicts", state=AdminMenu.dict)
        ),
        state=AdminMenu.dict_type_device,
        getter=(get_types_devices, get_main)
    ),
    Window(
        DynamicMedia("photo"),
        Case(
            {
                0: Const("Нету данных о типах отчетов"),
                ...: List(
                    Jinja(
                        '''
Название: {{item.name if item.name else 'Нет данных'}}
Описание {{item.description if item.description else 'Нет данных'}}
Поле комплекса: {{'Да' if item.on_complex else 'Нет'}}
Поле места установки: {{'Да' if item.on_place else 'Нет'}}
Количество изображений: {{item.count_images if item.count_images else 'Нет данных'}}
'''
                    ),
                    items="types_reports",
                    id="list_types_reports",
                    page_size=1,
                    on_page_changed=sync_scroll("group_s_delete_types_reports")
                )
            },
            selector="count"
        ),
        ScrollingGroup(
            Select(
                Const("❌ Удалить тип отчета"),
                id="delete_type_report_button",
                item_id_getter=lambda x: x.id,
                items="types_reports",
                on_click=delete_type_report
            ),
            id="group_s_delete_types_reports",
            width=1,
            height=1,
            hide_pager=True
        ),
        NumberedPager(
            scroll="list_types_reports",
        ),
        Row(
            Start(
                Const("➕ Добавить тип отчета"),
                id="add_type_report",
                state=AddTypeReport.name
            ),
            SwitchTo(Const("🔙 Назад"), id="back_dicts", state=AdminMenu.dict)
        ),
        state=AdminMenu.dict_type_report,
        getter=(get_types_reports, get_main)
    ),
    Window(
        DynamicMedia("photo"),
        Case(
            {
                0: Const("Нету данных о пользователях"),
                ...: List(
                    Jinja(
                        '''
ID: {{item.user_id if item.user_id else 'Нет данных'}}
Имя: {{item.first_name if item.first_name else 'Нет данных'}}
Фамилия: {{item.last_name if item.last_name else 'Нет данных'}}
Сектор: {% for sector in item.sectors %}
{{sector.name}}{% if not loop.last %}, {% endif %}{% endfor %}\n
Телефон: {{item.phone if item.phone else 'Нет данных'}}
Блокировка: {{'Да' if item.is_blocked else 'Нет'}}
'''
                    ),
                    items="users",
                    id="list_users",
                    page_size=1,
                    on_page_changed=sync_scroll("group_s_delete_users")
                )
            },
            selector="count"
        ),
        ScrollingGroup(
            Select(
                Const("❌ Удалить пользователя"),
                id="delete_user_button",
                item_id_getter=lambda x: x.user_id,
                items="users",
                on_click=delete_user
            ),
            id="group_s_delete_users",
            width=1,
            height=1,
            hide_pager=True
        ),
        NumberedPager(
            scroll="list_users",
        ),
        Row(
            Start(
                Const("➕ Добавить пользователя"),
                id="add_user",
                state=AddUser.user_id
            ),
            SwitchTo(Const("🔙 Назад"), id="back_dicts", state=AdminMenu.dict)
        ),
        state=AdminMenu.dict_user,
        getter=(get_users, get_main)
    ),
)
