from typing import Any

from pytube import YouTube, StreamQuery, Stream
from pytube.exceptions import RegexMatchError, VideoUnavailable

from src.yt_provider import YtProvider


class App:
    @staticmethod
    def print_stream_infos(stream: StreamQuery, is_video: bool):
        for s in stream:
            if is_video:
                out = f"[ itag='{s.itag}' - format='{s.type}' - resolution='{s.resolution}' - fps='{s.fps}' ]"
            else:
                out = f"[ itag='{s.itag}' - format='{s.type}' - quality='{s.abr}' ]"

            print(out)

    @staticmethod
    def on_progress_handler(stream: Stream, chunk: bytes, bytes_remaining: int):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        pct_completed = bytes_downloaded / total_size * 100
        print(f"Downloading: {round(pct_completed, 2)} %")

    @staticmethod
    def on_complete_handler(stream: Stream, path: str):
        print(f"Download completed;\nTitle: {stream.title}\nPath: {path}")

    def run(self):
        while True:
            print("1- Download video\n"
                  "E- Exit")
            target = input()
            if target.lower() == "e":
                return
            elif target == "1":
                target_url = input("Enter video url: (E for Exit)")
                if target_url.lower() == "e":
                    return

                try:
                    yt = YtProvider.get_yt(
                        url=target_url,
                        progress_handler=self.on_progress_handler,
                        complete_handler=self.on_complete_handler,
                    )
                except Any as err:
                    print(f"Unexpected error: {err}")
                    continue

                print(f"Title: {yt.title}")
                all_streams, video_streams, audio_streams = YtProvider.load_streams(yt)
                result = False
                while not result:
                    print("Available streams;")
                    self.print_stream_infos(video_streams, True)
                    self.print_stream_infos(audio_streams, False)
                    itag_str = input("Input 'itag' of the stream to download: (E for MainMenu)")
                    if itag_str.lower() == "e":
                        break
                    try:
                        itag_target = int(itag_str)
                    except ValueError:
                        print("itag must be number")
                        continue

                    result = YtProvider.download_by_itag(stream_query=all_streams, itag=itag_target)
            else:
                print("Command not found.")
                continue
