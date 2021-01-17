import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from config import TELEGRAM_TOKEN

storage = RedisStorage2(db=5)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
