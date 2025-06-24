from flask import Flask, request, Response
from yt_dlp import YoutubeDL
import requests
import os

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


# ✅ ADD THIS BLOCK for Render port detection
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
