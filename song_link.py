import requests
import spotipy
from spotipy import SpotifyClientCredentials

import config

client_credentials_manager = SpotifyClientCredentials(client_id=config.SPOTIPY_CLIENT_ID, client_secret=config.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get(query) -> str:
    spotify_link = sp.search(query)["tracks"]['items'][0]["external_urls"]["spotify"]
    r = requests.get("https://api.song.link/v1-alpha.1/links", params={
        "url": spotify_link
    })
    return r.json()["pageUrl"]