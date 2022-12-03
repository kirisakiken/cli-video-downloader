from pytube import YouTube, StreamQuery


class YtProvider:
    @staticmethod
    def get_yt(url: str, progress_handler, complete_handler):
        return YouTube(
            url=url,
            on_progress_callback=progress_handler,
            on_complete_callback=complete_handler,
        )

    @staticmethod
    def load_streams(yt: YouTube):
        print("Loading streams. . .")
        streams = yt.streams
        video_streams = streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc()
        audio_streams = streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc()
        return streams, video_streams, audio_streams

    @staticmethod
    def download_by_itag(stream_query: StreamQuery, itag: int, output_path: str = ""):
        try:
            stream_query.get_by_itag(itag).download(output_path=output_path)
        except:
            print("Download failed")
            return False

        return True
