from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
import json
from downloader import download_videos_from_channel

current_directory = os.path.dirname(os.path.abspath(__file__))

# Output directory for MP3 files
output_directory = os.path.join(current_directory, "mp3_output")

# Check if the output folder exists and create it if not
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Load channel configurations from a JSON file
config_path = os.path.join(current_directory, "config.json")
with open(config_path, "r", encoding="utf-8") as config_file:
    channels = json.load(config_file)

# Process each channel in the list
for channel in channels:
    results = download_videos_from_channel(channel)
    first_result = None
    
    if results:
        # Save the first downloaded title in the JSON file
        channel["search_title"] = results[0][0]

# Save the first downloaded title in the JSON file
with open("config.json", "w") as json_file:
    json.dump(channels, json_file, indent=4)
