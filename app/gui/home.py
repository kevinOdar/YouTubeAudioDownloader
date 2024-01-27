from PyQt6 import uic
from model.channel import Channel
from gui.list import ListWindow
import requests
from PyQt6.QtWidgets import QWidget


class Home(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.home = uic.loadUi("gui/home.ui")
        self.initGUI()
        self.home.lblMessage.setText("")
        self.home.show()

    def search_youtube_channel(self):
        if len(self.home.txtChannel.text()) == 0:
            self.home.lblMessage.setText("Please, enter a channel name")
            self.home.txtChannel.setFocus()
        else:
            status_code = self.validate_youtube_channel(self.home.txtChannel.text())
            if status_code == 200:
                channel = Channel(channel_name=self.home.txtChannel.text())
                self.list = ListWindow(channel)
                self.home.hide()

            else:
                self.home.lblMessage.setText("The channel doesn't exist")

    def initGUI(self):
        self.home.btnSearch.clicked.connect(self.search_youtube_channel)

    def validate_youtube_channel(self, channel_name):
        url = f"https://www.youtube.com/c/{channel_name}"
        response = requests.get(url)
        return response.status_code
