import os
import sys
import re
import pytest

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from app.model.video import Video
import downloader

current_directory = os.path.dirname(os.path.abspath(__file__))
output_directory = os.path.join(current_directory, "../mp3_output")

expected_videos = []  # Used by the fixture


@pytest.fixture
def delete_test_files():
    yield
    for video in expected_videos:
        filename = video[0]  # First value of the tuple

        file_path = os.path.join(
            output_directory, re.sub(r'[\/:*?"<>|]', "", filename) + ".mp3"
        )
        if os.path.exists(file_path):
            os.remove(file_path)


def test_load_more_videos():
    channel_url = "https://www.youtube.com/@bossanovaguitar/videos"

    driver = downloader.set_driver(channel_url, 10)
    video_elements = downloader.load_more_videos(driver)
    assert len(video_elements) == 48  # 48 videos


# @pytest.mark.only
def test_download_audio_as_mp3(delete_test_files):
    global expected_videos  # Used by the fixture
    expected_videos = [
        (
            "04 - U2 New Years Day (Slane Castle 2001 Live) HD",
            "https://www.youtube.com/watch?v=95vkJfeJBw4",
        )
    ]

    file_path = os.path.join(output_directory, f"{expected_videos[0][0]}.mp3")
    video = Video(expected_videos[0][0], expected_videos[0][1], "")
    downloader.download_audio_as_mp3(
        # expected_videos[0][0], expected_videos[0][1], output_directory
        video,
        output_directory,
    )

    assert os.path.exists(file_path)
    assert file_path.endswith(".mp3")


# @pytest.mark.only
def test_download_videos_from_channel_all_videos(delete_test_files):
    channel_config = {
        "channel_url": "file:///"
        + os.path.join(current_directory, "fake_youtube_channel.html"),
        "search_title": "",
        "specific_word": "Tiny Desk",
    }
    global expected_videos  # Used by the fixture
    expected_videos = [
        (
            "Ivy Queen: Tiny Desk Concert",
            "https://www.youtube.com/watch?v=7EAM4pxxL4Y",
            "https://i.ytimg.com/vi/7EAM4pxxL4Y/hqdefault.jpg",
        ),
        (
            "Caroline Polachek: Tiny Desk Concert",
            "https://www.youtube.com/watch?v=JmnZHQNN5cc",
            "https://i.ytimg.com/vi/JmnZHQNN5cc/hqdefault.jpg",
        ),
        (
            "Villano Antillano: Tiny Desk Concert",
            "https://www.youtube.com/watch?v=RxhleZbLF64",
            "https://i.ytimg.com/vi/RxhleZbLF64/hqdefault.jpg",
        ),
        (
            "Alex Cuba: Tiny Desk Concert",
            "https://www.youtube.com/watch?v=A3ThZptD8WY",
            "https://i.ytimg.com/vi/A3ThZptD8WY/hqdefault.jpg",
        ),
        (
            "Chlöe: Tiny Desk Concert",
            "https://www.youtube.com/watch?v=oIeqO2tyhcY",
            "https://i.ytimg.com/vi/oIeqO2tyhcY/hqdefault.jpg",
        ),
    ]
    assert downloader.get_videos_from_channel(channel_config) == expected_videos

    downloader.download_videos_from_channel(channel_config)
    for title, _, _ in expected_videos:
        expected_file_path = os.path.join(
            output_directory, re.sub(r'[\/:*?"<>|]', "", title) + ".mp3"
        )
        assert os.path.exists(expected_file_path)


def test_only_download_one_video(delete_test_files, capsys):
    channel_config = {
        "channel_url": "file:///"
        + os.path.join(current_directory, "fake_youtube_channel.html"),
        "search_title": "Caroline Polachek: Tiny Desk Concert",
        "specific_word": "Tiny Desk",
    }
    global expected_videos  # Used by the fixture
    expected_videos = [
        (
            "Ivy Queen: Tiny Desk Concert",
            "https://www.youtube.com/watch?v=7EAM4pxxL4Y",
            "https://i.ytimg.com/vi/7EAM4pxxL4Y/hqdefault.jpg",
        ),
    ]
    assert downloader.get_videos_from_channel(channel_config) == expected_videos

    downloader.download_videos_from_channel(channel_config)
    assert os.path.exists(
        os.path.join(output_directory, "Ivy Queen Tiny Desk Concert.mp3")
    )

    with pytest.raises(
        Exception, match='"Ivy Queen: Tiny Desk Concert" was already downloaded'
    ):
        video = Video(expected_videos[0][0], expected_videos[0][1], "")
        downloader.download_audio_as_mp3(video, output_directory)

    capsys.readouterr()  # To catch the first printout "Downloaded audio..."
    downloader.download_videos_from_channel(channel_config)
    captured_already_downloaded_text = capsys.readouterr()

    assert (
        captured_already_downloaded_text.out
        == '"Ivy Queen: Tiny Desk Concert" was already downloaded\n'
    )
