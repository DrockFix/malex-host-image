import json
from datetime import datetime
from typing import Union

from aiogram.types import DateTime
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from .models import TypeReport, Device, Place, DeviceType, UserSector, User, Banner, Report


############### Типы отчетов ###############

async def orm_get_types_report(session: AsyncSession):
    query = select(TypeReport)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_type_report(session: AsyncSession, type_report_id: int):
    query = select(TypeReport).where(TypeReport.id == type_report_id)
    result = await session.execute(query)
    return result.scalars().first()


async def orm_add_type_report(session: AsyncSession, data: dict):
    obj = TypeReport(
        name=data["name"],
        description=data["description"],
        on_complex=data["on_complex"],
        on_place=data["on_place"],
        count_images=data["count_images"],
    )
    session.add(obj)
    await session.commit()


async def orm_update_type_report(session: AsyncSession, type_report_id: int, data):
    query = (
        update(TypeReport)
        .where(TypeReport.id == type_report_id)
        .values(
            name=data["name"],
            description=data["description"],
            on_complex=data["on_complex"],
            on_place=data["on_place"],
            count_images=data["count_images"],
        )
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_type_report(session: AsyncSession, type_report_id: int):
    query = delete(TypeReport).where(TypeReport.id == type_report_id)
    await session.execute(query)
    await session.commit()


############### Комплексы ###############
async def orm_get_devices(session: AsyncSession):
    query = select(Device).options(joinedload(Device.type))
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_device(session: AsyncSession, device_id: int):
    query = select(Device).where(Device.id == device_id).options(joinedload(Device.type))
    result = await session.execute(query)
    return result.scalars().first()


async def orm_add_device(session: AsyncSession, data: dict):
    obj = Device(
        type_id=data["type_id"],
        number=data["number"],
    )
    session.add(obj)
    await session.commit()


async def orm_update_device(session: AsyncSession, device_id: int, data):
    query = (
        update(Device)
        .where(Device.id == device_id)
        .values(
            name=data["name"],
            type_id=data["type_id"],
            number=data["number"],
        )
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_device(session: AsyncSession, device_id: int):
    query = delete(Device).where(Device.id == device_id)
    await session.execute(query)
    await session.commit()


############### Места ###############
async def orm_get_places(session: AsyncSession):
    query = select(Place)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_place(session: AsyncSession, place_id: int):
    query = select(Place).where(Place.id == place_id)
    result = await session.execute(query)
    return result.scalars().first()


async def orm_add_place(session: AsyncSession, data: dict):
    obj = Place(
        name=data["name"],
    )
    session.add(obj)
    await session.commit()


async def orm_update_place(session: AsyncSession, place_id: int, data):
    query = (
        update(Place)
        .where(Place.id == place_id)
        .values(
            name=data["name"],
        )
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_place(session: AsyncSession, place_id: int):
    query = delete(Place).where(Place.id == place_id)
    await session.execute(query)
    await session.commit()


############### Типы комплексов ###############

async def orm_get_types_device(session: AsyncSession):
    query = select(DeviceType)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_type_device(session: AsyncSession, type_device_id: int):
    query = select(DeviceType).where(DeviceType.id == type_device_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_add_type_device(session: AsyncSession, data: dict):
    obj = DeviceType(
        name=data["name"],
        description=data["description"],
    )
    session.add(obj)
    await session.commit()


async def orm_update_type_device(session: AsyncSession, type_device_id: int, data):
    query = (
        update(DeviceType)
        .where(DeviceType.id == type_device_id)
        .values(
            name=data["name"],
            description=data["description"],
        )
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_type_device(session: AsyncSession, type_device_id: int):
    query = delete(DeviceType).where(DeviceType.id == type_device_id)
    await session.execute(query)
    await session.commit()


############### Сектора ###############
async def orm_get_user_sectors(session: AsyncSession):
    query = select(UserSector)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_user_sector(session: AsyncSession, sector_id: int):
    query = select(UserSector).where(UserSector.id == sector_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_add_user_sector(session: AsyncSession, data: dict):
    obj = UserSector(
        name=data["name"],
    )
    session.add(obj)
    await session.commit()


async def orm_add_plan_sector(session: AsyncSession, sector_name: str, file_id: str):
    query = (
        update(UserSector)
        .where(UserSector.name == sector_name)
        .values(
            file=file_id,
        )
    )
    await session.execute(query)
    await session.commit()


async def orm_update_user_sector(session: AsyncSession, sector_id: int, data):
    query = (
        update(UserSector)
        .where(UserSector.id == sector_id)
        .values(
            name=data["name"],
        )
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_user_sector(session: AsyncSession, sector_id: int):
    query = delete(UserSector).where(UserSector.id == sector_id)
    await session.execute(query)
    await session.commit()


############### Пользователи ###############

async def orm_get_users(session: AsyncSession):
    query = select(User).options(selectinload(User.sectors))
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_add_user(
        session: AsyncSession,
        data: dict
):
    query = select(User).where(User.user_id == data["user_id"])
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_id=data["user_id"], first_name=data["first_name"], last_name=data["last_name"],
                 phone=data["phone"])
        )
        await session.commit()


async def orm_blocked_user(session: AsyncSession, user_id: int):
    query = update(User).where(User.user_id == user_id).values(is_blocked=True)
    await session.execute(query)
    await session.commit()


async def orm_delete_user(session: AsyncSession, user_id: int):
    query = delete(User).where(User.user_id == user_id)
    await session.execute(query)
    await session.commit()


############### Отчеты ###############

async def orm_add_report(session: AsyncSession, data: dict):
    json.dumps(data["image"])
    place_id = None
    device_id = None
    date_str = data['date']
    date_obj = datetime.fromisoformat(date_str)
    if "place_id" in data:
        if data["place_id"] != 0:
            place_id = data["place_id"]
    if "device_id" in data:
        if data["device_id"] != 0:
            device_id = data["device_id"]
    obj = Report(
        user_id=data["user_id"],
        place_id=place_id,
        device_id=device_id,
        type_id=data["type_id"],
        date=date_obj,
        image=data["image"] if "image" in data else None,
    )
    session.add(obj)
    await session.commit()


async def orm_get_report(session: AsyncSession, report_id: int):
    query = select(Report).where(Report.id == report_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_user_reports(
        session: AsyncSession,
        user_id: int,
):
    query = select(Report).where(Report.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_time_reports(
        session: AsyncSession,
        start_time: datetime,
        end_time: datetime,
):
    query = select(Report).where(Report.time >= start_time).where(Report.time <= end_time).order_by(Report.time.desc())
    result = await session.execute(query)
    return result.scalars().all()


############### Работа с баннерами (информационными страницами) ###############

async def orm_add_banner_description(session: AsyncSession, data: dict):
    # Добавляем новый или изменяем существующий по именам
    # пунктов меню: main, about, cart, shipping, payment, catalog
    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Banner(name=name, description=description) for name, description in data.items()])
    await session.commit()


async def orm_change_banner_image(session: AsyncSession, name: str, image: str):
    query = update(Banner).where(Banner.name == name).values(image=image)
    await session.execute(query)
    await session.commit()


async def orm_get_banner(session: AsyncSession, page: str):
    query = select(Banner).where(Banner.name == page)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_info_pages(session: AsyncSession):
    query = select(Banner)
    result = await session.execute(query)
    return result.scalars().all()
