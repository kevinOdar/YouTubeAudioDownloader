import iterator


original_channels = iterator.load_channels("config.json")
channels = iterator.download_videos_from_each_channel(original_channels)
iterator.save_first_titles("config.json", channels)
