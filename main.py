import asyncio
import os
import re
from datetime import datetime, timedelta
from urllib.parse import quote

import aiohttp
import aiosqlite
import logging

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dynaconf import Dynaconf
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import locale

locale.setlocale(locale.LC_TIME, 'ru')

# Создаем объект конфигурации
settings = Dynaconf(settings_files=['settings.toml'])
# environments=True,
# env='development')

# Чтение токена из файла settings.toml
token = settings.get('tg.token')
path_image = settings.get('img.path_image')
tmp_image = settings.get('img.tmp_image')
yandex_token = settings.get('yandex.token')
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

sectors = ["Город", "Область"]

bot = Bot(token=token)
storage = MemoryStorage()
router = Router()
dp = Dispatcher(storage=storage)


async def get_user(chat_id):
    async with aiosqlite.connect('db.sqlite') as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM User WHERE id=?", (chat_id,))
            user = await cursor.fetchone()
            return user


async def save_user(chat_id, name, surname, patronymic, sector):
    async with aiosqlite.connect('db.sqlite') as db:
        async with db.cursor() as cursor:
            await cursor.execute("INSERT INTO User (id, name, surname, patronymic, sector) VALUES (?, ?, ?, ?, ?)",
                                 (chat_id, name, surname, patronymic, sector))
            await db.commit()


async def upload_to_yandex_disk(dir, file, yandex_token):
    dir_yandex = dir.replace("./", "/")
    url = f'https://cloud-api.yandex.net/v1/disk/resources?path=disk:{dir_yandex}'
    headers = {
        'Authorization': f'OAuth {yandex_token}'
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(url, headers=headers) as response:
                url = f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={dir_yandex}/{file}&overwrite=true'
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        upload_url = data.get('href')
                        if upload_url:
                            async with session.put(upload_url, data=open(f"{dir}/{file}", 'rb')):
                                pass
        except aiohttp.ClientError as e:
            pass


async def save_report(data, file_id):
    file_path = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file_path.file_path)
    file_dir = f"{path_image}{data['type_image'].upper()}/{data['date'].year}/{data['date'].strftime('%B')}/{data['place']}"
    file_name = f"{data['date'].strftime('%d.%m.%Y')}.jpg"
    file_path = os.path.join(file_dir, file_name)
    os.makedirs(file_dir, exist_ok=True)
    with open(file_path, "wb") as file:
        file.write(downloaded_file.read())
    await upload_to_yandex_disk(file_dir, file_name, yandex_token)

    async with aiosqlite.connect('db.sqlite') as db:
        async with db.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO Image (user_id, type_image, path, place, date_report) VALUES (?, ?, ?, ?, ?)",
                (data['chat_id'],
                 data['type_image'],
                 file_path,
                 data['place'],
                 data['date']))
            await db.commit()


class FormUser(StatesGroup):
    surname = State()
    name = State()
    patronymic = State()
    sector = State()


class Report(StatesGroup):
    type_image = State()
    date = State()
    place = State()
    complex = State()
    path = State()


async def save_dict(data: dict):
    await save_user(data['chat_id'], data['name'], data['surname'], data['patronymic'], data['sector'])


@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if user is not None:
        kb = [
            [
                types.KeyboardButton(text="Отчет"),
                types.KeyboardButton(text="Локации"),
                types.KeyboardButton(text="График"),
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
        )
        await bot.send_message(message.from_user.id, "Регистрация успешно завершена! "
                                                     "Теперь вы можете выбрать нужную функцию,"
                                                     " просто нажав на соответствующую кнопку ниже.",
                               reply_markup=keyboard)
    else:
        await message.answer("Пожалуйста, введите вашу фамилию!")
        await state.set_state(FormUser.surname)


@dp.message(FormUser.surname)
async def form_user_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer(text="Пожалуйста, введите ваше имя!")
    await state.set_state(FormUser.name)


@dp.message(FormUser.name)
async def form_user_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text="Пожалуйста, введите ваше отчество!")
    await state.set_state(FormUser.patronymic)


@dp.message(FormUser.patronymic)
async def form_user_patronymic(message: types.Message, state: FSMContext):
    await state.update_data(patronymic=message.text)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Город", callback_data="город"),
                types.InlineKeyboardButton(text="Область", callback_data="область"))
    await message.answer(text="Пожалуйста, выберите ваш сектор!",
                         reply_markup=builder.as_markup())


@dp.callback_query(F.data.in_({'город', 'область'}))
async def form_user_sector(callback: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    await state.update_data(sector=callback.data, chat_id=callback.from_user.id)
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Да", callback_data="yes_user"),
                types.InlineKeyboardButton(text="Сбросить данные", callback_data="no_user"))
    full_name = f"{user_data['surname']} {user_data['name']} {user_data['patronymic']}"
    sector = user_data['sector']

    confirmation_message = (
        f"Подтвердите введенные данные:\n\n"
        f"ФИО: *{full_name}*\n"
        f"Сектор: *{sector}*\n\n"
        f"Все верно?"
    )

    await bot.send_message(callback.from_user.id, confirmation_message, parse_mode="Markdown",
                           reply_markup=builder.as_markup())

    @dp.callback_query(F.data.in_('yes_user'))
    async def callback_form_user_yes(callback: types.CallbackQuery):
        await bot.answer_callback_query(callback.id)
        await save_dict(user_data)
        await state.clear()
        await cmd_start(callback, state)

    @dp.callback_query(F.data.in_('no_user'))
    async def callback_form_user_no(callback: types.CallbackQuery):
        await bot.answer_callback_query(callback.id)
        await bot.send_message(callback.from_user.id, text="Пожалуйста, введите вашу фамилию!")
        await state.set_state(FormUser.surname)


@dp.message(F.text.in_("Отчет"))
async def handle_report(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Авш", callback_data="авш"),
                types.InlineKeyboardButton(text="Знак", callback_data="знак"),
                types.InlineKeyboardButton(text="Мониторинг", callback_data="мониторинг"))
    await message.answer(text="Выберите тип фотографии!",
                         reply_markup=builder.as_markup())
    await state.set_state(Report.type_image)

    @dp.callback_query(F.data.in_({'авш', 'знак', 'мониторинг'}))
    async def callback_report_type(callback: types.CallbackQuery):
        await bot.answer_callback_query(callback.id)
        await state.update_data(type_image=callback.data)
        await state.update_data(chat_id=callback.from_user.id)
        await state.set_state(Report.date)
        type = callback.data
        now = datetime.now()
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text=(now - timedelta(days=3)).strftime("%d.%m.%Y"), callback_data="3"),
                    types.InlineKeyboardButton(text=(now - timedelta(days=2)).strftime("%d.%m.%Y"), callback_data="2"),
                    types.InlineKeyboardButton(text=(now - timedelta(days=1)).strftime("%d.%m.%Y"), callback_data="1"),
                    types.InlineKeyboardButton(text="Сегодня", callback_data="0"))

        await bot.send_message(callback.from_user.id, text="Пожалуйста, выберите дату отчета!",
                               reply_markup=builder.as_markup())

        @dp.callback_query(F.data.in_({'0', '1', '2', '3'}))
        async def callback_report_data(callback: types.CallbackQuery):
            await bot.answer_callback_query(callback.id)
            await state.update_data(
                date=now - timedelta(days=int(callback.data)))  # Передача текста из колбэка в состояние
            await state.set_state(Report.place)
            if type == 'знак':
                await bot.send_message(callback.from_user.id, text="Пожалуйста, введите локацию!")
            else:
                await bot.send_message(callback.from_user.id, text="Пожалуйста, введите название комплекса!")

    @dp.message(Report.place)
    async def handle_report_place(message: types.Message):
        await state.update_data(place=message.text)
        await message.answer(text="Пожалуйста, загрузите фото!")
        await state.set_state(Report.path)

    @dp.message(F.document, Report.path)
    async def handle_photo_message(message: types.Message):
        await message.answer(text="Нужно загрузить именно фотографию, а не файл!")
        await state.set_state(Report.path)
    @dp.message(F.photo, Report.path)
    async def handle_photo_message(message: types.Message):
        photo = message.photo[-1]
        file_id = photo.file_id
        await process_report_data(file_id, message)

    async def process_report_data(file_id, message):
        report_data = await state.get_data()
        report_message = (
            f"Подтвердите введенные данные:\n\n"
            f"Тип: *{report_data['type_image']}*\n"
            f"Дата: *{report_data['date'].strftime('%B %d, %Y')}\n*"
            f"Локация: *{report_data['place']}*"
        )
        photo_media = types.InputMediaPhoto(media=file_id, caption=report_message, parse_mode="markdown")

        await message.reply_media_group(media=[photo_media])
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Да", callback_data=f"yes_{message.message_id}"),
                    types.InlineKeyboardButton(text="Сбросить данные", callback_data=f"no_{message.message_id}"))
        await message.answer("Все верно?", reply_markup=builder.as_markup())

        @dp.callback_query(F.data.in_(f'yes_{message.message_id}'))
        async def callback_report_yes(callback: types.CallbackQuery):
            await bot.answer_callback_query(callback.id)
            await save_report(report_data, file_id)
            await state.clear()
            report_data.clear()
            await bot.send_message(callback.from_user.id, "Отчет отправлен!")


        @dp.callback_query(F.data.in_(f'no_{message.message_id}'))
        async def callback_report_no(callback: types.CallbackQuery, state: FSMContext):
            await bot.answer_callback_query(callback.id)
            await state.clear()
            report_data.clear()
            await handle_report(callback.message, state)

    @dp.message(F.text.in_("Локации"))
    async def handle_place(message: types.Message):
        # Здесь вы можете добавить логику обработки нажатия кнопки "Локации"
        await message.answer('Функция "Локации" в разработке.')


@dp.message(F.text.in_("График"))
async def handle_chart(message: types.Message):
    input_file = FSInputFile("./files/График.pdf")
    await message.answer_document(input_file)

async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(f"Error: {str(e)}\n")
        await asyncio.sleep(5)
        await main()

if __name__ == "__main__":
    asyncio.run(main())
