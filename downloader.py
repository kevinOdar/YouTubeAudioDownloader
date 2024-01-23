from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pytube import YouTube
import time
import re
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

output_directory = os.path.join(current_directory, "mp3_output")


def download_audio_as_mp3(title, video_url, output_path):
    file_title = re.sub(r'[\/:*?"<>|]', "", title)  # Remove invalid characters
    if os.path.exists(os.path.join(output_directory, f"{file_title}.mp3")):
        raise Exception(f"{title} was already downloaded")
    else:
        try:
            yt = YouTube(video_url)
            audio_stream = yt.streams.filter(
                only_audio=True, file_extension="mp4"
            ).first()
            if audio_stream:
                mp4_filename = os.path.join(output_path, f"{file_title}.mp4")
                mp3_filename = os.path.join(output_path, f"{file_title}.mp3")

                audio_stream.download(
                    output_path=output_path, filename=file_title + ".mp4"
                )

                if os.path.exists(mp4_filename) and mp4_filename.endswith(".mp4"):
                    os.rename(mp4_filename, mp3_filename)
                    print(f"Downloaded audio: {file_title}")
                else:
                    raise FileNotFoundError(
                        f"Error downloading audio from {video_url}: MP4 file not found or has incorrect extension"
                    )
            else:
                raise ValueError(
                    f"Error downloading audio from {video_url}: No MP4 audio stream found"
                )
        except Exception as e:
            raise Exception(f"Error downloading audio from {video_url}: {str(e)}")


def set_driver(channel_url, wait):
    # Selenium and Chrome Driver Configuration
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-logging")  # Disable browser logging
    options.add_argument("--log-level=3")  # Set the log level to SEVERE
    chrome_service = webdriver.chrome.service.Service(
        os.path.join(current_directory, "chromedriver.exe")
    )
    driver = webdriver.Chrome(service=chrome_service, options=options)

    driver.get(channel_url)  # Open the channel page

    driver.implicitly_wait(wait)  # Wait for elements to load
    return driver


def load_more_videos(driver):
    continuation_elements = driver.find_elements(
        By.TAG_NAME, "ytd-continuation-item-renderer"
    )
    if len(continuation_elements) > 0:
        actions = ActionChains(driver)
        actions.move_to_element(continuation_elements[0]).perform()
        time.sleep(3)  # Wait for new videos to load
    return driver.find_elements(
        By.CSS_SELECTOR,
        ".yt-simple-endpoint.focus-on-expand.style-scope.ytd-rich-grid-media",
    )


def get_videos_from_channel(channel_config):
    channel_url = channel_config["channel_url"]
    search_title = channel_config["search_title"]
    specific_word = channel_config["specific_word"]

    driver = set_driver(channel_url, 10)

    shown_video_links = set()  # Set to store displayed video links
    video_found = False
    new_videos = []

    while True:
        video_elements = load_more_videos(driver)
        new_videos_len = 0  # To control that there are no videos anymore
        for element in video_elements:
            href = element.get_attribute("href")
            title = element.get_attribute("title")
            if href and title and "/watch?v=" in href and href not in shown_video_links:
                new_videos_len = (
                    new_videos_len + 1
                )  # It will be 0 if there are no new videos
                if (
                    search_title and search_title in title
                ):  # search_title is not null ==> to make search_title optional
                    video_found = True
                    break  # Exit the loop if the desired video is found
                elif specific_word in title:
                    new_videos.append(
                        (
                            title,
                            href,
                            "https://i.ytimg.com/vi/" + href[-11:] + "/hqdefault.jpg",
                        )
                    )
                shown_video_links.add(href)
        if video_found:
            break  # No need to continue loading if the video is found
        if new_videos_len == 0:
            break  # No need to continue loading if there are no videos anymore
    driver.quit()  # Close the browser
    return new_videos


def download_videos_from_channel(channel_config):
    new_videos = get_videos_from_channel(channel_config)

    for title, video_url, _ in new_videos:
        try:
            download_audio_as_mp3(title, video_url, output_directory)
        except Exception as e:
            print(str(e))

    return new_videos
