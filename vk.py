import vk_audio, vk_api

import config


def auth_handler():
    """
    2FA handler
    """

    key = input("Enter authentication code: ")
    remember_device = True

    return key, remember_device


vk_session = vk_api.VkApi(login=config.VK_LOGIN, password=config.VK_PASSWORD,
                          auth_handler=auth_handler)

try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)

vk = vk_audio.VkAudio(vk=vk_session)

def search(query: str) -> str:
    data = vk.search(query)
    audio = data.Audios[0]
    return f"https://vk.com/audio{audio.owner_id}_{audio.id}"
