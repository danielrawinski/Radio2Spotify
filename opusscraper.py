from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as soup
import json
import requests
from spotifySecrets import spotify_user_id, spotify_authstring
import pickle

class scraper:

    def __init__(self):
        self.url= "https://www.lrt.lt/mediateka/tiesiogiai/lrt-opus"
        self.id = spotify_user_id
        self.driver = webdriver.Firefox(executable_path=<YOUR PATH HERE AS STRING>)
        self.song_info = {}
        self.playlist_id = <STRING WITH PLAYLIST ID> #created prior to that
        self.authstring = spotify_authstring
        
    def token_refresher(self): #using last token and saving a new one
        
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
        
        
    def now_playing(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(100)
        
        self.soup = soup(self.driver.page_source, 'html.parser')
        self.nowplaying = self.soup.findAll("div", {"class": "channel-program-item__right", "id": "rds"})[0].text[9:-6] # removing "Eteryje:" from the beginning and release year from the end from a resulting string
        # print(self.nowplaying)
        self.artist, self.title = self.nowplaying.split("-", 1) #splitting into artist and song name, max 1 dash in between, assuming other may be a part of song title

        self.song_info = {
                "title": self.title,
                "artist": self.artist,
                "uri": self.get_spotify_uri(self.title, self.artist)
                }
    
        print(self.song_info)
        
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

        # only use the first song if any is found, if not: skip
        try:
            uri = songs[0]["uri"]
        except IndexError:
            uri = None

        return uri
    
    def add_to_playlist(self):
  
        self.token_refresher()
        self.now_playing()

        # add a song into new playlist
        if self.song_info["uri"] is not None:
            request_data = json.dumps([self.song_info["uri"]])
        else:
            pass

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

# playlist creator, used only once in the beginning

class create_playlist:
    
    def __init__(self):
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
    
    def playlist(self):
        
        self.token_refresher()
        
        request_body = json.dumps({
            "name": "LRT Opus automated playlist",
            "description": "A result of exercise in automating a transfer of LRT Opus playlist into Spotify",
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
