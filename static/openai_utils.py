import openai
import json
from dotenv import dotenv_values

config = dotenv_values(".env")

openai.api_key = config["OPENAI_API_KEY"]

def generate_ai_playlist(prompt, count=8):
    example_response = """[{"song": 'Shape of You', "artist": 'Ed Sheeran'},
    {"song": "Everybody Hurts", "artist": "R.E.M."},
    {"song": "Nothing Compares 2 U", "artist": "Sinead O'Connor"},
    {"song": "Tears in Heaven", "artist": "Eric Clapton"},
    {"song": "Hurt", "artist": "Johnny Cash"},
    {"song": "Yesterday", "artist": "The Beatles"}]"""

    messages = [
        {
            "role": "system",
            "content": """You are playlist generator. You should generate a list of songs and their artists
        according to a text prompt. You can not repeat songs. You should return the result as a JSON array where each element
        follows this format: {"song" : <song_title>, "artist" : <artist_name>}.""",
        },
        {
            "role": "user",
            "content": "Generate a playlist of exactly 6 song(s) based on this prompt: top hits of today",
        },
        {
            "role": "assistant",
            "content": example_response,
        },
        {
            "role": "user",
            "content": f"Generate a playlist of exactly {count} song(s) based on this prompt: {prompt}",
        },
    ]

    res = openai.ChatCompletion.create(
        messages=messages, model="gpt-3.5-turbo"
    )
    # print(res.choices[0].message.content)
    try:
        return json.loads(res.choices[0].message.content)
    except:
        raise Exception("Sorry I was unable to process your request. Please try adjusting your query.");

def generate_track_queries(json_songs):
    track_queries = []

    for element in json_songs:
        song, artist = element["song"], element["artist"]
        track_queries.append(f"{song} {artist}")
    
    return track_queries