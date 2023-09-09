from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
import json
from downloader import download_videos_from_channel

current_directory = os.path.dirname(os.path.abspath(__file__))

# Load channel configurations from a JSON file
config_path = os.path.join(current_directory, "config.json")
with open(config_path, "r", encoding="utf-8") as config_file:
    channels = json.load(config_file)

# Process each channel in the list
for channel in channels:
    download_videos_from_channel(channel)