import logging
import os
import shutil

import pylast
import requests
from PIL import Image
from aiogram import types

import config
import song_link
from misc import dp, bot
from photo_uploader import uploadphoto
from picture_generator import generate_picture

network = pylast.LastFMNetwork(
    api_key=config.LASTFM_API_KEY, api_secret=config.LASTFM_API_SECRET)

logger = logging.getLogger("now_command")


@dp.message_handler(commands=["now"])
async def lastfm_generate(message: types.Message):
    # Get last.fm username
    lastfm_username = message.text.split(" ")[1]

    # Check if it exist
    try:
        track = network.get_user(lastfm_username).get_now_playing()
    except:
        logger.exception(f"Exception - user {lastfm_username} does not exist")
        return

    # Get user's profile pictures
    pfps = await bot.get_user_profile_photos(message.from_user.id, limit=1)

    # Check for profile picture availability
    try:
        pfp_id = pfps["photos"][-1][-1]["file_id"]
        try:
            open(f"pictures/cache/{pfp_id}.png")
        except IOError:
            logger.warning(f"Profile picture for {message.from_user.first_name} does not exist. Downloading.")
            await bot.download_file_by_id(pfp_id, f"pictures/cache/{pfp_id}.png")
    # If user does not have profile picture then use the default
    except IndexError:
        logger.warning(f"User {message.from_user.first_name} does not have profile picture. Use default.")
        pfp_id = "default-profile"

    finally:
        logger.info(
            f"Profile picture for {message.from_user.first_name} is pictures/cache/{pfp_id}.png. Continuing.")

    # Download cover image from Last.FM
    logger.info(
        f"Downloading cover image for {message.from_user.first_name} ({track.get_cover_image(pylast.SIZE_LARGE)})")
    try:
        Image.open(requests.get(track.get_cover_image(pylast.SIZE_LARGE), stream=True).raw).convert("RGB").save(
            f"pictures/temp/{message.from_user.first_name}-album.jpg")
    # If album cover fucked up
    except requests.exceptions.MissingSchema:
        logger.info("Copying default album picture to temp folder")
        shutil.copy("pictures/default-album.jpg", f"pictures/temp/{message.from_user.first_name}-album.jpg")

    # Get album name
    try:
        album_name = track.get_album().get_name()
    except AttributeError:
        album_name = track.get_name()

    try:
        # Generate picture
        logger.info(f"Generating picture for {message.from_user.first_name}")
        generate_picture(pfp_id, track.get_name(), track.get_artist().get_name(),
                         album_name, message.from_user.first_name)

        # Inline buttons
        kb = types.InlineKeyboardMarkup()
        btn_lastfm = types.InlineKeyboardButton(text="Last.FM", url=track.get_url())

        try:
            btn_song_link = types.InlineKeyboardButton(text="song.link", url=song_link.get(
                track.get_name() + " " + track.get_artist().get_name()))
            kb.row(btn_lastfm,  btn_song_link)
        except IndexError:
            kb.row(btn_lastfm)

        # Send picture as inline result
        logger.info(f"Sending generated picture to {message.from_user.first_name}")
        uploaded_pics = uploadphoto(f"pictures/temp/{message.from_user.first_name}.png")

        await message.reply_photo(uploaded_pics["photo_url"], reply_markup=kb)

        # Remove temp pictures
        os.remove(f"pictures/temp/{message.from_user.first_name}.png")
        os.remove(f"pictures/temp/{message.from_user.first_name}-album.jpg")

        logger.info("Success!")

    except:
        logger.exception("Exception in generating")
