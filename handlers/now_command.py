import logging

import pylast
import requests
from PIL import Image
from aiogram import types

import config
from misc import dp, bot
from picture_generator import generate_picture

network = pylast.LastFMNetwork(
    api_key=config.LASTFM_API_KEY, api_secret=config.LASTFM_API_SECRET)

logger = logging.getLogger("now_command")


@dp.message_handler(commands=["now"])
async def lastfm_generate(message: types.Message):
    pfps = await bot.get_user_profile_photos(message.from_user.id, limit=1)
    pfp_id = pfps["photos"][-1][-1]["file_id"]

    logger.info(f"Downloading profile picture for {message.from_user.first_name}")
    await bot.download_file_by_id(pfp_id, f"pictures/{message.from_user.first_name}-pfp.png")

    lastfm_username = message.get_args().split()[0]
    track = network.get_user(lastfm_username).get_now_playing()

    logger.info(f"Downloading cover image for {message.from_user.first_name}")
    try:
        Image.open(requests.get(track.get_cover_image(pylast.SIZE_LARGE), stream=True).raw).convert("RGB").save(
            f"pictures/{message.from_user.first_name}-album.jpg")
    except AttributeError:
        logger.info(f"{message.from_user.first_name} is not listening to anything, abort")
        await message.reply("You're not listening to anything, retard")
        return

    try:
        logger.info(f"Generating picture for {message.from_user.first_name}")
        generate_picture(message.from_user.first_name, track.get_name(), track.get_artist().get_name(),
                         track.get_album().get_name())
        with open(f"pictures/{message.from_user.first_name}.png", "rb") as photo:
            logger.info(f"Sending generated picture to {message.from_user.first_name}")
            await message.reply_photo(photo, "success")

    except Exception as e:
        logger.exception("Exception in generating")
