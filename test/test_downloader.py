import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

import downloader

def test_load_more_videos():
    channel_url = "https://www.youtube.com/@bossanovaguitar/videos"

    driver = downloader.set_driver(channel_url, 10)
    video_elements = downloader.load_more_videos(driver)
    assert len(video_elements) == 209  # 48 videos

def test_download_audio_as_mp3():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_directory = os.path.join(current_directory, "test/mp3_output")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    video_url = "https://www.youtube.com/watch?v=95vkJfeJBw4"

    downloader.download_audio_as_mp3(video_url, output_directory)

    title = "04 - U2 New Years Day (Slane Castle 2001 Live) HD"

    mp3_filename = os.path.join(output_directory, f"{title}.mp3")
    assert os.path.exists(mp3_filename)
    assert mp3_filename.endswith(".mp3")

    if os.path.exists(mp3_filename):
        os.remove(mp3_filename)

def test_download_videos_from_channel_all_videos():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_directory = os.path.join(current_directory, "../mp3_output")
    channel_config = {
        "channel_url": "file:///E:/Desktop/Kevin/Projects/obtener-audio-youtube/test/fake_youtube_channel.html",
        "search_title": "",
        "specific_word": "Tiny Desk",
    }
    expected_videos = [
        ("Ivy Queen: Tiny Desk Concert", "https://www.youtube.com/watch?v=7EAM4pxxL4Y"),
        (
            "Caroline Polachek: Tiny Desk Concert",
            "https://www.youtube.com/watch?v=JmnZHQNN5cc",
        ),
        (
            "Villano Antillano: Tiny Desk Concert",
            "https://www.youtube.com/watch?v=RxhleZbLF64",
        ),
        ("Alex Cuba: Tiny Desk Concert", "https://www.youtube.com/watch?v=A3ThZptD8WY"),
        ("Chlöe: Tiny Desk Concert", "https://www.youtube.com/watch?v=oIeqO2tyhcY"),
    ]
    assert downloader.download_videos_from_channel(channel_config) == expected_videos
    os.remove(os.path.join(output_directory, "Chlöe Tiny Desk Concert.mp3"))
    os.remove(os.path.join(output_directory, "Alex Cuba Tiny Desk Concert.mp3"))
    os.remove(os.path.join(output_directory, "Caroline Polachek Tiny Desk Concert.mp3"))
    os.remove(os.path.join(output_directory, "Ivy Queen Tiny Desk Concert.mp3"))
    os.remove(os.path.join(output_directory, "Villano Antillano Tiny Desk Concert.mp3"))

def test_download_videos_from_channel_one_video(capsys):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_directory = os.path.join(current_directory, "../mp3_output")
    channel_config = {
        "channel_url": "file:///E:/Desktop/Kevin/Projects/obtener-audio-youtube/test/fake_youtube_channel.html",
        "search_title": "Caroline Polachek: Tiny Desk Concert",
        "specific_word": "Tiny Desk",
    }
    expected_videos = [
        ("Ivy Queen: Tiny Desk Concert", "https://www.youtube.com/watch?v=7EAM4pxxL4Y"),
    ]
    assert downloader.download_videos_from_channel(channel_config) == expected_videos
    captured_downloaded_text = capsys.readouterr()
    downloader.download_videos_from_channel(channel_config)
    captured_already_downloaded_text = capsys.readouterr()
    assert captured_already_downloaded_text.out == "Ivy Queen: Tiny Desk Concert was already downloaded\n"
    os.remove(os.path.join(output_directory, "Ivy Queen Tiny Desk Concert.mp3"))