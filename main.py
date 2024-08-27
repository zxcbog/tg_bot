import sys
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from utils import *
import routers
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.mongo import MongoStorage

storage = MongoStorage(m_db)
dp = Dispatcher(storage=storage)
scheduler = AsyncIOScheduler()


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(routers.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    loop.run_until_complete(main())