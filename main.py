import asyncio
import datetime
import logging
import os

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

from aiogram_dialog import setup_dialogs

from dotenv import load_dotenv, find_dotenv
from redis.asyncio import Redis

from src.middlewares.check_user import UserBannedMiddleware

load_dotenv(find_dotenv())

from src.database.engine import create_db, session_maker, drop_db
from src.dialogs import dialog_router
from src.handlers.admin_private import admin_router
from src.handlers.user_group import user_group_router
from src.handlers.user_private import user_private_router
from src.middlewares.db import DataBaseSession

import locale

locale.setlocale(locale.LC_ALL, "")

bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
redis = Redis(
    host="127.0.0.1",
    port=6379,
)
storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True))
# jobstores = {
#     'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
#                              run_times_key='dispatched_trips_running',
#                              host=os.getenv('REDIS_HOST'),
#                              db=2,
#                              port=os.getenv('REDIS_PORT'))
# }
# scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="Asia/Krasnoyarsk", jobstores=jobstores))
# scheduler.ctx.add_instance(bot, declared_class=Bot)
# scheduler.add_job(apsched.send_message_time, trigger='date',
#                   run_date=datetime.datetime.now() + datetime.timedelta(seconds=10))
# scheduler.add_job(apsched.send_message_cron, trigger='cron', hour=datetime.datetime.now().hour,
#                   minute=datetime.datetime.now().minute + 1, start_date=datetime.datetime.now())
# scheduler.add_job(apsched.send_message_interval, trigger='interval', seconds=60)
bot.my_admins_list = []


async def on_startup(bot):
    # await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот лег')


def setup_dp():
    dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.message.middleware(UserBannedMiddleware())
    dp.include_router(user_private_router)
    dp.include_router(user_group_router)
    dp.include_router(admin_router)
    dp.include_router(dialog_router)
    setup_dialogs(dp)
    return dp


async def main():
    logging.basicConfig(level=logging.INFO)
    dp = setup_dp()
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
