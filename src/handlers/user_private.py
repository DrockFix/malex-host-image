from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram_dialog import StartMode, DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from ..filters.chat_types import ChatTypeFilter
from ..states.user import MenuUser

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(MenuUser.main, mode=StartMode.RESET_STACK)
#
#     await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)
#
#
# async def send_plan(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
#     await callback.answer("Ваш план график:")
#
#
# async def get_names(session: AsyncSession):
#     return [x.name for x in await orm_get_types_device(session)]
#
#
# @user_private_router.callback_query(MenuCallBack.filter())
# async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
#     if callback_data.menu_name == "plan":
#         await send_plan(callback, callback_data, session)
#         return
#     elif callback_data.menu_name in await get_names(session):
#         await add_report(callback.message, None, callback_data, session)
#         return
#
#     media, reply_markup = await get_menu_content(
#         session,
#         level=callback_data.level,
#         menu_name=callback_data.menu_name,
#         user_id=callback.from_user.id,
#         type_id=callback_data.type_id,
#     )
#
#     await callback.message.edit_media(media=media, reply_markup=reply_markup)
#     await callback.answer()
#
#
# async def add_report(message: types.Message, state: FSMContext, callback_data: MenuCallBack, session: AsyncSession):
#     type_report = callback_data.type_report
#     await state.update_data(
#         user_id=message.from_user.id,
#         type_report=type_report,
#     )
#     if type_report.on_place:
#         places = await orm_get_places(session)
#         btns_places = {place.name: str(place.id) for place in places}
#         await message.answer(
#             "Выберите место", reply_markup=get_callback_btns(btns=btns_places)
#         )
#         await state.set_state(AddReport.place_id)
#     elif type_report.on_complex:
#         devices = await orm_get_devices(session)
#         btns_devices = {device.name: str(device.id) for device in devices}
#         await message.answer(
#             "Выберите комплекс", reply_markup=get_callback_btns(btns=btns_devices)
#         )
#         await state.set_state(AddReport.complex_id)
#     else:
#         await message.answer("Выберите дату")
#         await state.set_state(AddReport.date)
#
#
# @user_private_router.message(StateFilter("*"), Command("отмена"))
# @user_private_router.message(StateFilter("*"), F.text.casefold() == "отмена")
# async def cancel_handler(message: types.Message, state: FSMContext) -> None:
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.clear()
#     await message.answer("Действия отменены")
#
#
# # Вернутся на шаг назад (на прошлое состояние)
# @user_private_router.message(StateFilter("*"), Command("назад"))
# @user_private_router.message(StateFilter("*"), F.text.casefold() == "назад")
# async def back_step_handler(message: types.Message, state: FSMContext) -> None:
#     current_state = await state.get_state()
#
#     if current_state == AddReport.place_id:
#         await message.answer(
#             'Предыдущего шага нет, или введите место или напишите "отмена"'
#         )
#         return
#
#     previous = None
#     for step in AddReport.__all_states__:
#         if step.state == current_state:
#             await state.set_state(previous)
#             await message.answer(
#                 f"Ок, вы вернулись к прошлому шагу \n {AddReport.texts[previous.state]}"
#             )
#             return
#         previous = step
#
#
# # Ловим данные для состояние name и потом меняем состояние на description
# @user_private_router.message(AddReport.place_id, F.text)
# async def add_report_place(message: types.Message, state: FSMContext, session: AsyncSession):
#     await state.update_data(place_id=message.text)
#     report = await state.get_data()
#     if report.type_report.on_complex:
#         devices = await orm_get_devices(session)
#         btns_devices = {device.name: str(device.id) for device in devices}
#         await message.answer(
#             "Выберите комплекс", reply_markup=get_callback_btns(btns=btns_devices)
#         )
#         await state.set_state(AddReport.complex_id)
#     else:
#         await message.answer("Выберите дату")
#         await state.set_state(AddReport.date)
#
#
# @user_private_router.message(AddReport.place_id)
# async def check_add_report_place(message: types.Message, state: FSMContext):
#     await message.answer("Вы ввели не допустимые данные, введите текст названия товара")
#
#
# # Ловим данные для состояния description и потом меняем состояние на price
# @user_private_router.message(AddReport.complex_id, F.text)
# async def add_report_complex(message: types.Message, state: FSMContext):
#     await state.update_data(complex_id=message.text)
#     await message.answer(
#         "Укажите дату", reply_markup=types.ReplyKeyboardRemove()
#     )
#     await state.set_state(AddReport.date)
#
#
# # Хендлер для отлова некорректных вводов для состояния description
# @user_private_router.message(AddReport.complex_id)
# async def check_add_report_complex(message: types.Message):
#     await message.answer("Вы ввели не допустимые данные, введите текст описания товара")
#
#
# # Ловим callback выбора категории
# @user_private_router.message(AddReport.date, F.text)
# async def add_report_date(message: types.Message, state: FSMContext):
#     await state.update_data(date=message.text)
#     await message.answer(
#         "Укажите дату", reply_markup=types.ReplyKeyboardRemove()
#     )
#     await state.set_state(AddReport.image)
#
#
# # Ловим любые некорректные действия, кроме нажатия на кнопку выбора категории
# @user_private_router.message(AddReport.date)
# async def check_add_report_date(message: types.Message, state: FSMContext):
#     await message.answer("Введите дату")
#
#
# @user_private_router.message(AddReport.image, F.text)
# async def add_report_image(message: types.Message, state: FSMContext, session: AsyncSession):
#     if message.photo:
#         await state.update_data(image=message.photo[-1].file_id)
#     else:
#         await message.answer("Отправьте фото отчета")
#         return
#     data = await state.get_data()
#     try:
#         await orm_add_report(session, data)
#         await message.answer("Товар добавлен/изменен")
#         await state.clear()
#     except Exception as e:
#         await message.answer(
#             f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет"
#         )
#         await state.clear()
#
#
# # Ловим все прочее некорректное поведение для этого состояния
# @user_private_router.message(AddReport.image)
# async def check_add_report_image(message: types.Message):
#     await message.answer("Отправьте фото отчета")
