import json
import requests

from refresh import Refresh
from secrets import spotify_user_id, discover_weekly_id
from refresh import Refresh

class PlaylistSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""

    def find_songs(self):
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            discover_weekly_id)
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
        response_json = response.json()
        print(response_json)

    def call_refresh(self):
        print("Refreshing token")
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()
        self.find_songs()

a = PlaylistSongs()
a.call_refresh()
