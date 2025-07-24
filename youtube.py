from flask import Flask, request, jsonify
from pytube import YouTube
import pytube.request
import os

app = Flask(__name__)

# Patch pytube.request.get to add User-Agent header
original_get = pytube.request.get

def patched_get(url, *args, **kwargs):
    headers = kwargs.get("headers", {})
    headers["User-Agent"] = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Safari/537.36"
    )
    kwargs["headers"] = headers
    return original_get(url, *args, **kwargs)

pytube.request.get = patched_get

@app.route('/')
def home():
    return 'YouTube Downloader API is live!'

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4')\
                           .order_by('resolution')\
                           .desc()\
                           .first()

        if not stream:
            return jsonify({'error': 'No suitable video stream found'}), 404

        filename = stream.default_filename
        stream.download(output_path='downloads')

        return jsonify({
            'message': f"Downloaded '{yt.title}' successfully.",
            'filename': filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
