from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
import json
from pytube import YouTube
import time
import re

current_directory = os.path.dirname(os.path.abspath(__file__))

# Load variables from the configuration file
config_path = os.path.join(current_directory, "config.json")
with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

# Selenium Configuration
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode, without a window
chrome_service = webdriver.chrome.service.Service(os.path.join(current_directory, "chromedriver.exe"))

# Chrome Driver Configuration
driver = webdriver.Chrome(service=chrome_service, options=options)

# YouTube Channel URL
channel_url = "https://www.youtube.com/c/nprmusic/videos"

# Title to search for
search_title = config["search_title"]

# Specific word to search for
specific_word = config["specific_word"]

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

# Open the channel page
driver.get(channel_url)

# Wait for elements to load
driver.implicitly_wait(10)

# Function to scroll to the end of the page
def scroll_to_end(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Function to load more videos
def load_more_videos(driver):
    continuation_elements = driver.find_elements(By.TAG_NAME, "ytd-continuation-item-renderer")
    if len(continuation_elements) > 0:
        actions = ActionChains(driver)
        actions.move_to_element(continuation_elements[0]).perform()
        time.sleep(3)  # Wait for new videos to load

# Set to store displayed video links
shown_video_links = set()
video_found = False

while True:
    load_more_videos(driver)

    video_elements = driver.find_elements(By.CLASS_NAME, "yt-simple-endpoint")

    new_videos = []

    for element in video_elements:
        href = element.get_attribute("href")
        title = element.get_attribute("title")
        if href and title and "/watch?v=" in href and href not in shown_video_links:
            if search_title in title:
                video_found = True
                break  # Exit the loop if the desired video is found
            elif specific_word in title:
                new_videos.append((title, href))
            shown_video_links.add(href)

    if video_found:
        break  # No need to continue loading if the video is found

# Download audio from videos that meet the condition
for title, href in new_videos:
    print("Title:", title)
    print("Link:", href)
    video_url = href
    try:
        download_audio_as_mp3(video_url, current_directory)  # Download audio as MP3
    except Exception as e:
        print(f"Error downloading audio from {video_url}: {str(e)} (Continuing)")
    print("-" * 50)

# Close the browser
driver.quit()
