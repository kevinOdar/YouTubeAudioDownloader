from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pytube import YouTube
import time
import re
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

# Output directory for MP3 files
output_directory = os.path.join(current_directory, "mp3_output")

# Function to download audio from a YouTube video as MP3
def download_audio_as_mp3(video_url, output_path, quality="128kbps"):
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
        if audio_stream:
            title = re.sub(r'[\/:*?"<>|]', '', yt.title)  # Remove invalid characters
            mp4_filename = os.path.join(output_path, f"{title}.mp4")
            mp3_filename = os.path.join(output_path, f"{title}.mp3")

            audio_stream.download(output_path=output_path, filename=title + ".mp4")

            if os.path.exists(mp4_filename) and mp4_filename.endswith(".mp4"):
                os.rename(mp4_filename, mp3_filename)
                print(f"Downloaded audio: {title}")
            else:
                print(f"Error downloading audio from {video_url}: MP4 file not found or has incorrect extension")
        else:
            print(f"Error downloading audio from {video_url}: No MP4 audio stream found")
    except Exception as e:
        print(f"Error downloading audio from {video_url}: {str(e)}")

# Function to load more videos
def load_more_videos(driver):
    continuation_elements = driver.find_elements(By.TAG_NAME, "ytd-continuation-item-renderer")
    if len(continuation_elements) > 0:
        actions = ActionChains(driver)
        actions.move_to_element(continuation_elements[0]).perform()
        time.sleep(3)  # Wait for new videos to load

def download_videos_from_channel(channel_config):
    # Selenium and Chrome Driver Configuration
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-logging")  # Disable browser logging
    options.add_argument("--log-level=3")  # Set the log level to SEVERE
    chrome_service = webdriver.chrome.service.Service(os.path.join(current_directory, "chromedriver.exe"))
    driver = webdriver.Chrome(service=chrome_service, options=options)

    # Variables from the config file
    channel_url = channel_config["channel_url"]
    search_title = channel_config["search_title"]
    specific_word = channel_config["specific_word"]

    # Open the channel page
    driver.get(channel_url)

    # Wait for elements to load
    driver.implicitly_wait(10)

    # Set to store displayed video links
    shown_video_links = set()
    video_found = False
    new_videos = []

    while True:
        load_more_videos(driver)

        video_elements = driver.find_elements(By.CLASS_NAME, "yt-simple-endpoint")
        new_videos_len = 0  # To control that there are no videos anymore

        for element in video_elements:
            href = element.get_attribute("href")
            title = element.get_attribute("title")
            if href and title and "/watch?v=" in href and href not in shown_video_links:
                new_videos_len = new_videos_len + 1  # It will be 0 if there are no videos
                if search_title and search_title in title: #search_title is not null ==> to make search_title optional
                    video_found = True
                    break  # Exit the loop if the desired video is found
                elif specific_word in title:
                    new_videos.append((title, href))
                shown_video_links.add(href)
        if video_found:
            break  # No need to continue loading if the video is found
        if new_videos_len == 0 :
            break  # No need to continue loading if there are no videos anymore 
           
    # Download audio from videos that meet the condition
    for title, href in new_videos:
        #print("Title:", title)
        video_url = href
        file_title = re.sub(r'[\/:*?"<>|]', '', title)  # Remove invalid characters
        if os.path.exists(os.path.join(output_directory, f"{file_title}.mp3")):
            print(f"{title} was already downloaded")
        else :
            try:
                download_audio_as_mp3(video_url, output_directory)  # Download audio as MP3
            except Exception as e:
                print(f"Error downloading audio from {video_url}: {str(e)} (Continuing)")
            print("-" * 50)

    # Close the browser
    driver.quit()

    return new_videos