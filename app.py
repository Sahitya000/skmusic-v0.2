from flask import Flask, request, Response
from yt_dlp import YoutubeDL
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "YT-DLP Backend is Live!"

@app.route('/stream')
def stream_audio():
    url = request.args.get("url")
    if not url:
        return "URL required", 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        stream_url = info['url']

    def generate():
        r = requests.get(stream_url, stream=True)
        for chunk in r.iter_content(chunk_size=1024):
            yield chunk

    return Response(generate(), content_type='audio/mpeg')
