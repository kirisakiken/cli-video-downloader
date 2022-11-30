from pytube import YouTube


class YtProvider:
    @staticmethod
    def get_yt(url: str, progress_handler: classmethod, complete_handler: classmethod):
        return YouTube(
            url=url,
            on_progress_callback=progress_handler,
            on_complete_callback=complete_handler,
        )