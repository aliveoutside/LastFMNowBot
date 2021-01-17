import base64

import requests
import config


def uploadphoto(file_path):
    with open(file_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": config.IMGBB_API_KEY,
            "image": base64.b64encode(file.read()),
            "expiration": 300
        }
        response = requests.post(url, payload)
        if response.status_code == 200:
            return {"photo_url": response.json()["data"]["url"], "thumb_url": response.json()["data"]["thumb"]["url"]}
    return None
