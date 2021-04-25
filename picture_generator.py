import logging

from PIL import Image, ImageFont, ImageDraw

# region Text and images settings
pfp_coordinates = (52, 20, 132, 100)
pfp_size = (80, 80)

album_pic_coordinates = (26, 144, 158, 276)
album_pic_size = (132, 132)

name_coordinates = (185, 20)

listening_to_coordinates = (185, 55)

track_coordinates = (185, 140)

artist_coordinates = (185, 178)

album_coordinates = (185, 216)

head_text_font_size = 36
head_text_font = ImageFont.truetype("fonts/gsans-emoji.ttf", head_text_font_size)

under_text_font_size = 29
under_text_font = ImageFont.truetype("fonts/Nunito-Regular.ttf", under_text_font_size)
# endregion

logger = logging.getLogger("picture_generator")


def generate_picture(pfp_id: str, track: str, artist: str, album: str, user_name: str, user_id: str):
    """
    Picture generator

    :param pfp_id: profile pic id
    :param track: Track name
    :param artist: Artist name
    :param album: Album name
    :param user_name: User name
    :param user_id: User id
    :return: nothing
    """
    # Opening background
    logger.info(f"Opening background for {user_name}")
    img = Image.open("pictures/background.png")

    # Adding profile and album pictures to result pic
    logger.info(f"Pasting profile picture for {user_name}")
    img.paste(Image.open(f"pictures/cache/{pfp_id}.png").resize(pfp_size), pfp_coordinates, None)
    logger.info(f"Pasting album picture for {user_id}")
    img.paste(Image.open(f"pictures/temp/{user_id}-album.jpg").resize(album_pic_size), album_pic_coordinates, None)

    # I don't remember why is it here but okay
    img_editable = ImageDraw.Draw(img)

    # Adding text like username, track etc. to picture
    img_editable.text(name_coordinates, user_name, (255, 255, 255), font=head_text_font)  # Username
    img_editable.text(listening_to_coordinates, "is now listening to", (255, 255, 255), font=head_text_font)  # Now listening
    img_editable.text(track_coordinates, track, (255, 255, 255), font=ImageFont.truetype("fonts/gsans-emoji.ttf", 29))  # Track
    img_editable.text(artist_coordinates, artist, (255, 255, 255), font=under_text_font)  # Artist
    img_editable.text(album_coordinates, album, (255, 255, 255), font=under_text_font)  # Album

    # Saving picture
    logger.info(f"Saving photo to pictures/temp/{user_id}.png")
    img.save(f"pictures/temp/{user_id}.png")
