import logging

import pylast
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup

import config
import user

network = pylast.LastFMNetwork(
    api_key=config.LASTFM_API_KEY, api_secret=config.LASTFM_API_SECRET)

logger = logging.getLogger("link")


class Link(StatesGroup):
    waiting_for_name = State()
    waiting_for_lastfm_username = State()


async def link_start(message: types.Message):
    logger.info(f"{message.from_user.id} started account linking")
    await message.answer("Tell me, what should I call you?", allow_sending_without_reply=True)
    await Link.waiting_for_name.set()


async def link_name_entered(message: types.Message, state: FSMContext):
    logger.info(f"{message.from_user.id} named {message.text}")
    await state.update_data(name=message.text)
    await Link.next()
    await message.answer("Now enter your Last.FM username", allow_sending_without_reply=True)


async def link_lastfm_username_entered(message: types.Message, state: FSMContext):
    logger.debug(f"{message.from_user.id} tries to link {message.text} LastFM account")
    try:
        network.get_user(message.text).get_playcount()
        logger.info(f"{message.from_user.id} linked {message.text} successfully!")
    except pylast.WSError:
        await message.reply(f"User {message.text} does not exist!")
        await message.answer("Try to enter your username again.")
        logger.warning(f"{message.from_user.id} entered wrong LastFM username! ({message.text})")
        return

    await state.update_data(lastfm_username=message.text)

    data = await state.get_data()

    user.set_lastfm_username(message.from_user.id, data["lastfm_username"])
    user.set_name(message.from_user.id, data["name"])

    await message.answer(
        f"Account has been linked successfully! Tap /now to share what you're listening to. "
        f"Also you can also use inline mode by typing @LastFMNowBot in any chat.")

    await state.finish()


def register_handlers_link(dp: Dispatcher):
    dp.register_message_handler(link_start, commands="link", state="*")
    dp.register_message_handler(link_start, CommandStart(deep_link="link"), state="*")
    dp.register_message_handler(link_name_entered, state=Link.waiting_for_name)
    dp.register_message_handler(link_lastfm_username_entered, state=Link.waiting_for_lastfm_username)
