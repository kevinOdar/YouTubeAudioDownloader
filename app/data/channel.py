import os
import sys

from model.channel import Channel
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
parent_dir = os.path.join(parent_dir, "..")
sys.path.insert(0, parent_dir)

from downloader import get_videos_from_channel, download_audio_as_mp3

class ChannelData:
    def __init__(self) -> None:
        self.videos_to_download = []

    def get_videos(self, channel: Channel):
        search = {
            "specific_word": "",
            "search_title": "",
            "channel_url": f"https://www.youtube.com/@{channel._channel_name}/videos",
        }
        return get_videos_from_channel(search)

    def download_videos(self, output_directory, show_message):
        for title, video_url, _ in self.videos_to_download:
            try:
                download_audio_as_mp3(title, video_url, output_directory)
            except Exception as e:
                # print(str(e))
                show_message(str(e))
                # raise Exception(str(e))

            print("-" * 50)
