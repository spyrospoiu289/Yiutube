from flask import Flask, request, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

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

