from flask import Flask, render_template, request
import os
from static.openai_utils import generate_ai_playlist, generate_track_queries
from static.spotify_utils import get_spotify_auth, get_spotify_client, get_spotify_user

app = Flask("__name__",
            template_folder="templates",
            static_url_path="",
            static_folder="static")

@app.route("/login", methods=["POST"])
def login():
    get_spotify_auth()
    return [True]

@app.route("/logout", methods=["POST"])
def logout():
    if os.path.exists(".cache"):
        os.remove(".cache")
        return[True]
    else:
        return[False]

@app.route("/playlist", methods=["POST"])
def create_playlist():
    spotify_client = get_spotify_client()
    user = get_spotify_user()
    try:
        assert user is not None
    except AssertionError as error:
        return [str(error)]

    prompt = request.form.get("prompt")
    num_songs = request.form.get("num_songs")
    try:
        assert ((prompt is not None) and (prompt != ""))
        assert int(num_songs) >= 1
    except AssertionError as error:
        return [str(error)]

    try:
        ai_playlist = generate_ai_playlist(prompt, num_songs)
    
        track_queries = generate_track_queries(ai_playlist)

        tracks = []

        for query in track_queries:
            searchRes = spotify_client.search(q=query, type="track", limit=10)
            tracks.append(searchRes["tracks"]["items"][0]["id"])


        new_playlist = spotify_client.user_playlist_create(
            user=user["id"],
            name=prompt,
            public=False
        )

        spotify_client.user_playlist_add_tracks(user["id"], new_playlist['id'], tracks)
        return track_queries
    except Exception as error:
        return [str(error)]

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)