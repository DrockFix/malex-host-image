from aiogram.fsm.state import StatesGroup, State


class AddBanner(StatesGroup):
    image = State()


class AddTypeReport(StatesGroup):
    name = State()
    description = State()
    settings = State()
    count_image = State()
    confirm = State()
    result = State()


class AddPlace(StatesGroup):
    name = State()
    confirm = State()
    result = State()


class AddDeviceType(StatesGroup):
    name = State()
    description = State()
    confirm = State()
    result = State()


class AddDevice(StatesGroup):
    type_id = State()
    number = State()
    confirm = State()
    result = State()


class AddUser(StatesGroup):
    user_id = State()
    first_name = State()
    last_name = State()
    sectors = State()
    phone = State()
    confirm = State()
    result = State()


class AddSector(StatesGroup):
    name = State()
    confirm = State()
    result = State()


class DeleteTypeReport(StatesGroup):
    confirm = State()
    result = State()


class DeletePlace(StatesGroup):
    confirm = State()
    result = State()


class DeleteDeviceType(StatesGroup):
    confirm = State()
    result = State()


class DeleteDevice(StatesGroup):
    confirm = State()
    result = State()


class DeleteUser(StatesGroup):
    confirm = State()
    result = State()


class DeleteSector(StatesGroup):
    confirm = State()
    result = State()


class AddPlan(StatesGroup):
    name = State()
    document = State()
    confirm = State()
    result = State()


class AdminMenu(StatesGroup):
    menu = State()
    settings = State()
    stat = State()
    dict = State()
    dict_type_report = State()
    dict_type_device = State()
    dict_device = State()
    dict_place = State()
    dict_sector = State()
    dict_user = State()
