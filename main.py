from bs4 import BeautifulSoup
import requests
#web scrapping for billboard songs
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL).text

soup = BeautifulSoup(response, "html.parser")
songsList = soup.select("li ul li h3")

song_names = [song.get_text(strip=True) for song in songsList]


#authentication for spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="7991bbd351ee4b67ac4a641e3eec5612",
        client_secret="6a0e39ee45614c96a4b5eb5f105403aa",
        show_dialog=True,
        cache_path="tokens.txt"
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
#searching for tracks
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)
#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
#https://developer.spotify.com/dashboard/applications/7991bbd351ee4b67ac4a641e3eec5612