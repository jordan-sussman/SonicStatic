import json
import webbrowser
import time
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

# Get track metadata from Spotify API with designated playlist in secrets.py
    def find_songs(self):
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            discover_weekly_id)
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
        response_json = response.json()
        print(response)

# Loop through all tracks in playlist to grab each song's album artwork URL into a list. 
        data = response_json
        for x in data['tracks']['items']:
            print(x['track']['album']['images'][0]['url'])

# Open every track's album artwork into a browser tab with a small delay between each
            urls = str(x['track']['album']['images'][0]['url'])
            webbrowser.open(urls)
            time.sleep(2)

# Call to refresh Spotify authorization token
    def call_refresh(self):
        print("Refreshing token")
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()
        self.find_songs()

a = PlaylistSongs()
a.call_refresh()
