import logging
from uuid import uuid1

import pylast
import requests
from PIL import Image
from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultPhoto

import config
from misc import dp, bot
from photo_uploader import uploadphoto
from picture_generator import generate_picture

network = pylast.LastFMNetwork(
    api_key=config.LASTFM_API_KEY, api_secret=config.LASTFM_API_SECRET)

logger = logging.getLogger("now_inline")


@dp.inline_handler()
async def now_inline(inline_query: InlineQuery):

    # Get last.fm username
    lastfm_username = inline_query.query.split(" ")[0]

    # Check if it exist
    try:
        track = network.get_user(lastfm_username).get_now_playing()
    except:
        logger.exception(f"Exception - user {lastfm_username} does not exist")
        return

    # Get user's profile pictures
    pfps = await bot.get_user_profile_photos(inline_query.from_user.id, limit=1)

    # Check for profile picture availability
    try:
        pfp_id = pfps["photos"][-1][-1]["file_id"]
        try:
            open(f"pictures/cache/{pfp_id}.png")
        except IOError:
            logger.warning(f"Profile picture for {inline_query.from_user.first_name} does not exist. Downloading.")
            await bot.download_file_by_id(pfp_id, f"pictures/cache/{pfp_id}.png")
    # If user does not have profile picture then use the default
    except IndexError:
        logger.warning(f"User {inline_query.from_user.first_name} does not have profile picture. Use default.")
        pfp_id = "default-profile"

    finally:
        logger.info(f"Profile picture for {inline_query.from_user.first_name} is pictures/cache/{pfp_id}.png. Continuing.")

    # Download cover image from Last.FM
    logger.info(f"Downloading cover image for {inline_query.from_user.first_name} ({track.get_cover_image(pylast.SIZE_LARGE)})")
    try:
        Image.open(requests.get(track.get_cover_image(pylast.SIZE_LARGE), stream=True).raw).convert("RGB").save(
        f"pictures/temp/{inline_query.from_user.first_name}-album.jpg")
    except requests.exceptions.MissingSchema:
        # TODO: спасибо ласт фму за сегфолты при скачивании обложки
        return

    try:
        # Generate picture
        logger.info(f"Generating picture for {inline_query.from_user.first_name}")
        generate_picture(pfp_id, track.get_name(), track.get_artist().get_name(),
                         track.get_album().get_name(), inline_query.from_user.first_name)

        kb = types.InlineKeyboardMarkup()
        btn_lastfm = types.InlineKeyboardButton(text="Last.FM", url=track.get_url())
        kb.add(btn_lastfm)

        # Send picture as inline result
        logger.info(f"Sending generated picture to {inline_query.from_user.first_name}")
        uploaded_pics = uploadphoto(f"pictures/temp/{inline_query.from_user.first_name}.png")
        logger.info("Uploaded photos - " + str(uploaded_pics))
        result = [
            InlineQueryResultPhoto(
                id=str(uuid1(clock_seq=0)),
                title="Photo",
                photo_url=uploaded_pics["photo_url"],
                thumb_url=uploaded_pics["thumb_url"],
                photo_width=100,
                photo_height=100,
                reply_markup=kb
            )
        ]
        await bot.answer_inline_query(inline_query.id, result, cache_time=5)


    except:
        logger.exception("Exception in generating")


