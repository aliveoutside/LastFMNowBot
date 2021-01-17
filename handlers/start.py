import logging

from aiogram import types

from main import rate_limit
from misc import dp


@dp.message_handler(commands=['start'])
@rate_limit(5, 'start')
async def command_start(message: types.Message):
    logging.info(f"{message.from_user.username} clicked start")
    await message.answer("лайк если тестишь в проде")
