from pytube import YouTube

def download_youtube_video():
    url = input("Enter the YouTube video URL: ").strip()

    try:
        yt = YouTube(url)
        print(f"Title: {yt.title}")

        stream = yt.streams.filter(progressive=True, file_extension='mp4')\
            .order_by('resolution')\
            .desc()\
            .first()

        print(f"Downloading: {stream.default_filename} at {stream.resolution}")
        stream.download()
        print("Download completed!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_youtube_video()
