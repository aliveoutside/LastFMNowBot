from aiogram import types
from aiogram.dispatcher import FSMContext

import user
from misc import dp


@dp.message_handler(commands=['start'], state="*")
async def command_start(message: types.Message, state: FSMContext):
    await state.finish()
    user.register(message.from_user.id)
    await message.answer(
        "Hello, I'm LastFMNow and I can help you share what you're listening right now. Tap /link to link you account.")


@dp.message_handler(commands=['cancel'], state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Action was cancelled.")


@dp.message_handler(commands=["getname"])
async def command_name(message: types.Message):
    await message.reply(user.get_name(message.get_args().split(' ')[0]))
