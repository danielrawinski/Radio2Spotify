from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as soup
import json
import requests
from spotifySecrets import spotify_user_id, spotify_authstring
import pickle

class scraper:

    def __init__(self):
        self.archive_url= "https://www.beachfm.co.jp/archive/"
        self.id = spotify_user_id
        # self.spotify_token = spotify_token
        self.driver = webdriver.Firefox(executable_path=<YOUR PATH AS STRING HERE>)
        self.songs_info = {}
        self.playlist_id = <YOUR PLAYLIST ID HERE> #created prior to that
        self.authstring = spotify_authstring
        
    def token_refresher(self):
        
        with open('tokens.pickle', 'rb') as f:
            self.access_token, self.refresh_token = pickle.load(f)
            
        query = f"https://accounts.spotify.com/api/token/"

        response = requests.post(
            query,
            data = {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
                    },
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {self.authstring}"
                }
            )
        
        response_json = response.json()
        print(response_json)
        self.access_token = response_json["access_token"]

        with open('tokens.pickle', 'wb') as f:
            pickle.dump([self.access_token, self.refresh_token], f)
        
        
    def radio_playlist(self):
        self.driver.get(self.archive_url)
        self.driver.implicitly_wait(100)
        
        self.soup = soup(self.driver.page_source, 'html.parser')
        self.titles = self.soup.findAll('td', {"class": "cell-title"})
        self.artists = self.soup.findAll('td', {"class": "cell-artists"})
        
        for item in range(len(self.titles)):
            self.songs_info[item] = {
                "title": self.titles[item].text,
                "artist": self.artists[item].text,
                "uri": self.get_spotify_uri(self.titles[item].text, self.artists[item].text)
                }
    
        print(self.songs_info)
        
    def get_spotify_uri(self, title, artist):

        query = f"https://api.spotify.com/v1/search?query=track%3A{title}+artist%3A{artist}&type=track&offset=0&limit=20"
            
        response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # only use the first song, if any is found at all
        try:
            uri = songs[0]["uri"]
        except IndexError:
            uri = None

        return uri
    
    def add_to_playlist(self):
        # populate dictionary with our liked songs
        self.token_refresher()
        self.radio_playlist()

        # collect all of uri
        uris = []
        for key in self.songs_info:
            if self.songs_info[key]["uri"] is not None:
               uris.append(self.songs_info[key]["uri"])
            else:
                pass
        print(uris)

        # create a new playlist if needed here

        # add all songs into new playlist
        request_data = json.dumps(uris)

        query = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }
        )
        
        return response
        
scrape = scraper()
scrape.add_to_playlist()

# playlist creator, used once in the beginning to create a playlist
class create_playlist:
    
    def __init__(self):
        with open('tokens.pickle', 'rb') as f:
            self.access_token, self.refresh_token = pickle.load(f)
    
    def playlist(self):
        
        request_body = json.dumps({
            "name": "Shonan Beach FM Playlist",
            "description": "A result of exercise in automating a transfer of my favourite Shonan Beach FM into Spotify",
            "public": False
        })

        query = f"https://api.spotify.com/v1/users/{spotify_user_id}/playlists"
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }
        )
        response_json = response.json()

        # playlist id printed so to see which to use
        print(response_json["id"])
        
# newlist = create_playlist()
# newlist.playlist()
    
