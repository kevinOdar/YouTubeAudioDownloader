import os
from PyQt6 import uic, QtNetwork
from PyQt6.QtWidgets import (
    QLabel,
    QApplication,
    QPushButton,
    QVBoxLayout,
    QStyle,
    QWidget,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QUrl, Qt
from data.channel import ChannelData
from model.channel import Channel

channelData = ChannelData()


class ImageWidget(QLabel):
    def __init__(self, imageUrl):
        super(ImageWidget, self).__init__()
        self.network_manager = QtNetwork.QNetworkAccessManager(self)
        self.image_url = imageUrl
        self.request_image()

    def request_image(self):
        request = QtNetwork.QNetworkRequest(QUrl(self.image_url))
        self.network_manager.finished.connect(self.handle_image_response)
        self.network_manager.get(request)

    def handle_image_response(self, reply):
        if reply.error() == QtNetwork.QNetworkReply.NetworkError.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.setPixmap(pixmap)
            self.setScaledContents(True)
        else:
            print(f"Error loading image: {reply.errorString()}")


class DownloadButton(QPushButton):
    def __init__(self, row, title, url, list):
        super(DownloadButton, self).__init__("Download")
        self.row = row
        self.col = 2
        self.title = title
        self.url = url
        self.list = list
        self.setFixedSize(100, 50)
        self.clicked.connect(self.download_audio)

    def download_audio(self):
        if not self.list.download_path:  # Show an alert if download_path is empty
            self.list.handle_download_error(
                "Please select a download folder before downloading."
            )
        else:
            channelData.videos_to_download = [(self.title, self.url, None)]
            channelData.download_videos(self.list.download_path, self.list.show_message)


class ListWindow:
    def __init__(self, channel: Channel) -> None:
        self.list = uic.loadUi("gui/list.ui")

        self.list.lblMessage.setText("")

        self.list.btnBack.setIcon(
            QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)
        )
        self.list.btnBack.setToolTip("Return")
        self.list.btnBack.clicked.connect(self.back_home)

        self.download_path = ""
        self.list.btnSelectPath.setToolTip("Select Download Folder")
        self.list.btnSelectPath.clicked.connect(self.select_download_path)
        self.list.btnSelectPath.setIcon(
            QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        )

        self.list.show()
        self.list.tableWidget.setColumnWidth(0, 298)
        self.list.tableWidget.setColumnWidth(1, 330)  # 355 without vertical bar
        self.list.tableWidget.setColumnWidth(2, 120)

        try:
            availableVideos = channelData.get_videos(channel)

            self.list.btnDownloadAll.clicked.connect(
                lambda: self.download_all(availableVideos)
            )

            self.list.tableWidget.setRowCount(len(availableVideos))
            for i, (title, url, thumbnail_url) in enumerate(availableVideos):
                self.list.tableWidget.setRowHeight(i, 200)  # 166 original on youtube

                # First column
                image = ImageWidget(thumbnail_url)
                self.list.tableWidget.setCellWidget(i, 0, image)

                # Second column
                text_label = QLabel(title)
                text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                text_label.setWordWrap(True)
                self.list.tableWidget.setCellWidget(i, 1, text_label)

                # Third column
                download_button = DownloadButton(i, title, url, self)
                container_widget = QWidget()
                container_layout = QVBoxLayout(container_widget)
                container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                container_layout.addWidget(download_button)
                self.list.tableWidget.setCellWidget(i, 2, container_widget)

        except Exception as e:
            print(e)

    def download_all(self, availableVideos):
        if not self.download_path:
            self.handle_download_error(
                "Please select a download folder before downloading."
            )
        else:
            channelData.videos_to_download = availableVideos
            channelData.download_videos(self.download_path, self.show_message)

    def back_home(self):
        from gui.home import Home

        self.home = Home()
        self.list.hide()

    def select_download_path(self):
        selected_path = QFileDialog.getExistingDirectory(
            self.list, "Select Download Folder", self.download_path
        )
        if selected_path:  # Only if the user update the downlaods path
            self.download_path = selected_path
            self.list.lblSelectedPath.setText("../" + os.path.basename(selected_path))

    def handle_download_error(self, error_message):
        QMessageBox.critical(
            self.list,
            "Error",
            error_message,
            QMessageBox.StandardButton.Ok,
        )

    def show_message(self, message):
        self.list.lblMessage.setText(message)
