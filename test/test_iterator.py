import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

import iterator

current_directory = os.path.dirname(os.path.abspath(__file__))
# Output directory for MP3 files
output_directory = os.path.join(parent_dir, "mp3_output")


def test_load_channels():
    expected_json = [
        {
            "specific_word": "Tiny Desk",
            "search_title": "PJ Harvey: Tiny Desk Concert",
            "channel_url": "https://www.youtube.com/c/nprmusic/videos",
        },
        {
            "specific_word": "Full Performance",
            "search_title": "Jungle - Full Performance (Live on KEXP)",
            "channel_url": "https://www.youtube.com/@kexp/videos",
        },
    ]
    assert (
        iterator.load_channels(os.path.join(current_directory, "config_test.json"))
        == expected_json
    )


def test_download_videos_from_each_channel():
    original_channels = [
        {
            "channel_url": "file:///"
            + os.path.join(current_directory, "fake_youtube_channel.html"),
            "search_title": "Caroline Polachek: Tiny Desk Concert",
            "specific_word": "Tiny Desk",
        }
    ]

    assert iterator.download_videos_from_each_channel(original_channels) == [
        {
            "channel_url": "file:///"
            + os.path.join(current_directory, "fake_youtube_channel.html"),
            "search_title": "Ivy Queen: Tiny Desk Concert",
            "specific_word": "Tiny Desk",
        }
    ]

    os.remove(os.path.join(output_directory, "Ivy Queen Tiny Desk Concert.mp3"))


def test_save_first_titles():
    expected_json = [
        {
            "channel_url": "file:///"
            + os.path.join(current_directory, "fake_youtube_channel.html"),
            "search_title": "Ivy Queen: Tiny Desk Concert",
            "specific_word": "Tiny Desk",
        }
    ]
    iterator.save_first_titles(
        os.path.join(current_directory, "config_fake_html.json"), expected_json
    )
    assert (
        iterator.load_channels(os.path.join(current_directory, "config_fake_html.json"))
        == expected_json
    )

    os.remove(os.path.join(current_directory, "config_fake_html.json"))
