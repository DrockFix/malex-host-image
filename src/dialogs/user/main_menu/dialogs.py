from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Button, SwitchTo, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Jinja

from src.states.user import MenuUser, AddReport
from .getters import get_main
from .getters import get_user
from .handlers import get_plan

main_menu_user = Dialog(
    Window(
        DynamicMedia("photo"),
        Jinja(
            '''
{{full_name}}, {{caption}}
'''
        ),
        Row(
            Start(
                Const("Отчет"),
                id="start_report",
                state=AddReport.type_report
            ),
            Button(
                Const("План-график"),
                id="get_plan",
                on_click=get_plan,
            ),
        ),
        Row(
            SwitchTo(
                Const("Помощь"),
                id="help",
                state=MenuUser.help,
            ),
            SwitchTo(
                Const("Контакты"),
                id="contact",
                state=MenuUser.contact,
            ),
        ),
        Row(
            SwitchTo(
                Const("Статистика"),
                id="stat",
                state=MenuUser.stat,
            ),
            # SwitchTo(
            #     Const("Профиль"),
            #     id="stat",
            #     state=MenuUser.profile,
            # ),
        ),
        state=MenuUser.main,
        getter=(get_main, get_user)
    ),
    Window(
        DynamicMedia("photo"),
        Format("{caption}"),
        SwitchTo(Const("🔙 Назад"),
                 id="back_main_menu",
                 state=MenuUser.main),
        state=MenuUser.help,
        getter=get_main
    ),
    Window(
        DynamicMedia("photo"),
        Format("{caption}"),
        SwitchTo(Const("🔙 Назад"),
                 id="back_main_menu",
                 state=MenuUser.main),
        state=MenuUser.stat,
        getter=get_main
    ),
    Window(
        DynamicMedia("photo"),
        Format("{caption}"),
        SwitchTo(Const("🔙 Назад"),
                 id="back_main_menu",
                 state=MenuUser.main),
        state=MenuUser.contact,
        getter=get_main
    )
)
