from aiogram.fsm.state import State, StatesGroup


class MenuUser(StatesGroup):
    main = State()
    help = State()
    contact = State()
    stat = State()
    profile = State()


class AddReport(StatesGroup):
    type_report = State()
    place_id = State()
    complex_id = State()
    date = State()
    image = State()
    confirm = State()
    result = State()


