import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from .models import Base
from ..common.texts_for_db import description_for_info_pages
from .orm_query import orm_add_banner_description, orm_change_banner_image

engine = create_async_engine(os.getenv('DB_URL'), echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        await orm_add_banner_description(session, description_for_info_pages)
        await orm_change_banner_image(session, 'main',  './src/static/user_private/main.jpg')
        await orm_change_banner_image(session, 'report', './src/static/user_private/report.jpg')
        await orm_change_banner_image(session, 'stat', './src/static/user_private/stat.jpg')
        await orm_change_banner_image(session, 'help', './src/static/user_private/help.jpg')
        await orm_change_banner_image(session, 'contact', './src/static/user_private/contact.jpg')
        await orm_change_banner_image(session, 'admin_dict', './src/static/admin/admin_dict.jpg')
        await orm_change_banner_image(session, 'admin_stat', './src/static/admin/admin_stat.jpg')
        await orm_change_banner_image(session, 'admin_settings', './src/static/admin/admin_settings.jpg')
        await orm_change_banner_image(session, 'admin_menu', './src/static/admin/admin_menu.jpg')
        await orm_change_banner_image(session, 'admin_dict_type_report', './src/static/admin/admin_dict_type_report.jpg')
        await orm_change_banner_image(session, 'admin_dict_type_device', './src/static/admin/admin_dict_type_device.jpg')
        await orm_change_banner_image(session, 'admin_dict_device', './src/static/admin/admin_dict_device.jpg')
        await orm_change_banner_image(session, 'admin_dict_place', './src/static/admin/admin_dict_place.jpg')
        await orm_change_banner_image(session, 'admin_dict_sector', './src/static/admin/admin_dict_sector.jpg')
        await orm_change_banner_image(session, 'admin_dict_user', './src/static/admin/admin_dict_user.jpg')


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
