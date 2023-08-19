import spotipy
from dotenv import dotenv_values

config = dotenv_values(".env")

spotify_client = None
user = None

def get_spotify_auth():
    global spotify_client
    global user
    spotify_client = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=config["SPOTIFY_CLIENT_ID"],
            client_secret=config["SPOTIFY_CLIENT_SECRET"],
            redirect_uri=config["REDIRECT_URI"],
            scope="playlist-modify-private playlist-modify-public",
            show_dialog=True
        )
    )
    user = spotify_client.current_user()

def get_spotify_user():
    if user is None:
        get_spotify_auth()
    return user

def get_spotify_client():
    if spotify_client is None:
        get_spotify_auth()
    return spotify_client