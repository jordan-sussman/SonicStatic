import requests
import jinja2
import http.server
import socketserver

from refresh import Refresh
from secrets import spotify_user_id, discover_weekly_id
from refresh import Refresh

# Bring in variables from secrets.py
class PlaylistSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""

# Get track metadata from Spotify API
    def find_songs(self):
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            discover_weekly_id)
        response = requests.get(query,
            headers={"Content-Type": "application/json",
             "Authorization": "Bearer {}".format(self.spotify_token)})
        response_json = response.json()
        print(response)

# Loop through all tracks in playlist to grab each track's album artwork URL
        data = response_json
        for x in data['tracks']['items']:
            urls = str(x['track']['album']['images'][0]['url'])
            print(urls)

# Create .html file through Jinja template then append the file for each loop
            outputfile = 'gallery.html'
            subs = jinja2.Environment( 
                loader=jinja2.FileSystemLoader('./')      
                ).get_template('template.html').render(albumartwork=urls)
            with open(outputfile,'a') as f: f.write(subs)

# Refresh Spotify authorization token
    def call_refresh(self):
        print("Refreshing token")
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()
        self.find_songs()

a = PlaylistSongs()
a.call_refresh()

# Starts server to view all album artwork at port 8000
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/gallery.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

PORT = 8000
handler_object = MyHttpRequestHandler
my_server = socketserver.TCPServer(("", PORT), handler_object)
my_server.serve_forever()
