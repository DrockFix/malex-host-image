import operator

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, Cancel, Row, Back, ScrollingGroup, Multiselect, Button, RequestContact, \
    Next
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Jinja, Const, Format

from src.constants import YES_NO
from .getters import get_delete_data_user, get_data_user, get_sectors
from .handlers import delete_user_yes_no, user_id_selected, first_name_selected, last_name_selected, sectors_selected, \
    contact_selected, add_user_yes_no
from src.dialogs.common import enable_send_mode
from src.states.admin import DeleteUser, AddUser

add_user_dialog = Dialog(
    Window(
        Const("Введите телеграмм ID пользователя"),
        MessageInput(user_id_selected, content_types=ContentType.TEXT),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddUser.user_id,
    ),
    Window(
        Const("Введите имя пользователя"),
        MessageInput(first_name_selected, content_types=ContentType.TEXT),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddUser.first_name,
    ),
    Window(
        Const("Введите фамилию пользователя"),
        MessageInput(last_name_selected, content_types=ContentType.TEXT),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddUser.last_name,
    ),
    Window(
        Const("Выберите сектора для пользователя(можно выбрать несколько)"),
        Multiselect(
            Format("✓ {item.name}"),
            Format("{item.name}"),
            id="m_sectors",
            item_id_getter=lambda x: x.id,
            items="sectors",
        ),
        Button(
            Const("Дальше"),
            id="s_add_settings",
            on_click=sectors_selected
        ),
        Next(Const("Пропустить")),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddUser.sectors,
        getter=get_sectors
    ),
    Window(
        Const("Отправьте контакт пользователя"),
        MessageInput(contact_selected, content_types=ContentType.CONTACT),
        # RequestContact(Const("Укажите номер телефона пользователя")),
        Next(Const("Пропустить")),
        Row(Back(Const("🔙 Назад")), Cancel(Const("❌ Отмена"))),
        state=AddUser.phone,
        # markup_factory=ReplyKeyboardFactory()
    ),
    Window(
        Const("Вы действительно хотите добавить этого пользователя?"),
        Jinja(
            '''
ID: {{user.user_id if user.user_id else 'Нет данных'}}
Имя: {{user.first_name if user.first_name else 'Нет данных'}}
Фамилия: {{user.last_name if user.last_name else 'Нет данных'}}
Сектор: {% for sector in user.sectors %}
{{sector.name}}{% if not loop.last %}, {% endif %}{% endfor %}\n
Телефон: {{user.phone if user.phone else 'Нет данных'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_add_user_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=add_user_yes_no,
        ),
        getter=get_data_user,
        state=AddUser.confirm,
    ),
    Window(
        Const("Пользователь добавлен!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        state=AddUser.result,
    ),
)

delete_user_dialog = Dialog(
    Window(
        Const("Вы действительно хотите удалить пользователя?"),
        Jinja(
            '''
ID: {{user.user_id if user.user_id else 'Нет данных'}}
Имя: {{user.first_name if user.first_name else 'Нет данных'}}
Фамилия: {{user.last_name if user.last_name else 'Нет данных'}}
Телефон: {{user.phone if user.phone else 'Нет данных'}}
Блокировка: {{'Да' if user.is_blocked else 'Нет'}}
'''
        ),
        Select(
            Format("{item[0]}"),
            id="s_delete_user_yes_no",
            item_id_getter=operator.itemgetter(1),
            items=YES_NO,
            on_click=delete_user_yes_no,
        ),
        getter=get_delete_data_user,
        state=DeleteUser.confirm,
    ),
    Window(
        Const("Пользователь удален!"),
        Cancel(Const("❌ Закрыть"), on_click=enable_send_mode),
        state=DeleteUser.result,
    )
)