from flask import Flask, request, Response, jsonify
from yt_dlp import YoutubeDL
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🎵 YT-DLP API is Live"

# 🔍 /api/search?query=songname
@app.route('/api/search')
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "query required"}), 400

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
        entry = info['entries'][0]
        return jsonify({
            "title": entry.get("title"),
            "webpage_url": entry.get("webpage_url"),
            "duration": entry.get("duration"),
            "thumbnail": entry.get("thumbnail"),
            "uploader": entry.get("uploader"),
            "id": entry.get("id")
        })

# 🎧 /api/stream?query=songname OR ?url=https://youtube.com/...
@app.route('/api/stream')
def stream():
    query = request.args.get("query")
    url = request.args.get("url")

    if not query and not url:
        return jsonify({"error": "query or url required"}), 400

    search = f"ytsearch1:{query}" if query else url

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search, download=False)
        stream_url = info['url'] if query else info.get('url')

    def generate():
        r = requests.get(stream_url, stream=True)
        for chunk in r.iter_content(chunk_size=1024):
            yield chunk

    return Response(generate(), content_type='audio/mpeg')

# ✅ Required for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
