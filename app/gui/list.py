import os
from PyQt6 import uic
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
from PyQt6.QtGui import QImage, QPixmap, QMovie, QImageReader
from PyQt6.QtCore import Qt, QUrl, QThread, pyqtSignal, QTimer
from data.channel import ChannelData
from model.channel import Channel
from model.video import Video
from typing import List
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import requests

# Constants
THUMBNAIL_COLUMN_WIDTH = 298
TITLE_COLUMN_WIDTH = 330  # 355 without vertical bar
BUTTON_COLUMN_WIDTH = 120
SPINNER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "resources/Spinner.gif"
)

# Instance of ChannelData
channel_data = ChannelData()


class ImageDownloader(QThread):
    image_loaded = pyqtSignal(QPixmap)

    def __init__(self, imageUrl):
        super().__init__()
        self.imageUrl = imageUrl

    def run(self):
        try:
            response = requests.get(self.imageUrl)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            image_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.image_loaded.emit(pixmap)
        except requests.RequestException as e:
            print(f"Error loading image: {e}")


class ImageWidget(QLabel):
    """Widget to display images downloaded from a URL."""

    def __init__(self, imageUrl):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_url = imageUrl
        self.image_downloader = ImageDownloader(imageUrl)
        self.image_downloader.image_loaded.connect(self.on_image_loaded)
        self.image_downloader.start()

    def on_image_loaded(self, pixmap):
        self.setPixmap(pixmap)
        self.setScaledContents(True)


class VideoDownloaderThread(QThread):
    video_downloaded = pyqtSignal()

    def __init__(self, videos: List[Video], download_path, callback):
        super().__init__()
        self.videos = videos
        self.download_path = download_path
        self.callback = callback

    def run(self):
        try:
            channel_data.videos_to_download = self.videos
            channel_data.download_videos(self.download_path, self.callback)
            self.video_downloaded.emit()
        except Exception as e:
            print(e)


class DownloadButton(QPushButton):
    def __init__(self, row, video: Video, list_widget):
        super(DownloadButton, self).__init__("Download")
        self.row = row
        self.col = 2
        self.video = video
        self.list_widget = list_widget
        self.setFixedSize(100, 50)

        # Spinner
        self.spinner_movie = QMovie(SPINNER_PATH)
        self.spinner_label = QLabel()
        self.spinner_label.setMovie(self.spinner_movie)
        self.spinner_label.setStyleSheet("margin-left: 7px;")

        self.clicked.connect(self.download_audio)

    def download_audio(self):
        if not self.list_widget.download_path:
            self.list_widget.handle_download_error(
                "Please select a download folder before downloading."
            )
        else:
            self.enable_column(False)
            self.hide()
            self.list_widget.list_widget.tableWidget.cellWidget(
                self.row, self.col
            ).layout().addWidget(self.spinner_label)
            self.spinner_movie.start()

            # Thread for downloading
            self.thread = VideoDownloaderThread(
                [self.video],
                self.list_widget.download_path,
                self.list_widget.show_message,
            )
            self.thread.video_downloaded.connect(self.enable_column)
            self.thread.finished.connect(self.hide_spinner)
            self.thread.start()

    def enable_column(self, enable=True):
        for row in range(self.list_widget.list_widget.tableWidget.rowCount()):
            widget = self.list_widget.list_widget.tableWidget.cellWidget(row, 2)
            if isinstance(widget, QWidget):
                widget.setEnabled(enable)

    def hide_spinner(self):
        self.spinner_movie.stop()
        self.spinner_label.hide()
        self.show()


class VideoLoaderThread(QThread):
    video_loaded = pyqtSignal(list)

    def __init__(self, channel: Channel):
        super().__init__()
        self.channel = channel
        self.availableVideos = []

    def run(self):
        try:
            self.availableVideos = channel_data.get_videos2(self.channel)
            self.video_loaded.emit(self.availableVideos)
        except Exception as e:
            print(e)


class ListWindow:
    def __init__(self, channel: Channel) -> None:
        # self.reset_instance()
        self.list_widget = uic.loadUi("gui/list.ui")
        self.channel = channel

        # Video loading thread
        self.video_loader_thread = VideoLoaderThread(channel)
        self.video_loader_thread.video_loaded.connect(self.handle_video_loading)
        self.video_loader_thread.start()

        # Message Label
        self.list_widget.lblMessage.setText("")

        # Back Button
        self.list_widget.btnBack.setIcon(
            QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)
        )
        self.list_widget.btnBack.setToolTip("Return")
        self.list_widget.btnBack.clicked.connect(self.back_home)

        # Load More Videos Button
        self.list_widget.btnLoadMore.hide()

        # Path selection
        self.download_path = ""
        self.list_widget.btnSelectPath.setToolTip("Select Download Folder")
        self.list_widget.btnSelectPath.clicked.connect(self.select_download_path)
        self.list_widget.btnSelectPath.setIcon(
            QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        )

        # Spinner
        spinner_movie = QMovie(SPINNER_PATH)
        self.list_widget.spinner_label.setMovie(spinner_movie)
        spinner_movie.start()
        layout = QVBoxLayout(self.list_widget)
        layout.addWidget(self.list_widget.spinner_label)

        # Layout - Columns
        self.list_widget.tableWidget.setColumnWidth(0, THUMBNAIL_COLUMN_WIDTH)
        self.list_widget.tableWidget.setColumnWidth(1, TITLE_COLUMN_WIDTH)
        self.list_widget.tableWidget.setColumnWidth(2, BUTTON_COLUMN_WIDTH)

        self.list_widget.show()  # Show the main window before starting the video loading thread

        # Filtering
        self.list_widget.txtFilter.textChanged.connect(self.update_filter_text)
        self.filtered_videos = self.video_loader_thread.availableVideos

        # Download All
        self.list_widget.btnDownloadAll.setEnabled(False)
        self.list_widget.btnDownloadAll.clicked.connect(self.download_all)

    # def reset_instance(self):
    #     #self.list_widget = None
    #     #self.channel = None
    #     self.video_loader_thread = None
    #     self.filtered_videos = []
    #     self.download_path = ""

    def handle_video_loading(self, availableVideos: List[Video]):
        self.list_widget.txtFilter.setEnabled(True)
        self.list_widget.btnDownloadAll.setEnabled(True)
        self.list_widget.spinner_label.hide()
        self.list_widget.btnLoadMore.hide()

        self.fill_table(availableVideos)

        if channel_data.check_if_for_more_videos():
            # self.list_widget.btnLoadMore.setEnabled(True)
            self.list_widget.btnLoadMore.show()
            self.list_widget.btnLoadMore.clicked.connect(
                lambda: self.next_videos(availableVideos)
            )

            # self.video_loader_thread = VideoLoaderThread(self.channel)
            # self.video_loader_thread.video_loaded.connect(self.handle_video_loading)
            # self.video_loader_thread.start()
            # for element in videos:
            #     print(element.title)

    def fill_table(self, availableVideos: List[Video]):
        try:
            self.list_widget.tableWidget.setRowCount(len(availableVideos))
            for i, (title, url, thumbnail_url) in enumerate(availableVideos):
                self.list_widget.tableWidget.setRowHeight(
                    i, 200
                )  # 166 original on youtube
                # First column
                image = ImageWidget(thumbnail_url)
                self.list_widget.tableWidget.setCellWidget(i, 0, image)

                # Second column
                text_label = QLabel(title)
                text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                text_label.setWordWrap(True)
                self.list_widget.tableWidget.setCellWidget(i, 1, text_label)

                # Third column
                download_button = DownloadButton(i, Video(title, url, ""), self)
                container_widget = QWidget()
                container_layout = QVBoxLayout(container_widget)
                container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                container_layout.addWidget(download_button)
                self.list_widget.tableWidget.setCellWidget(i, 2, container_widget)

        except Exception as e:
            print(e)
        finally:
            QApplication.processEvents()  # Force the application to process any pending events

    def update_filter_text(self):
        self.filtered_videos = list(
            filter(
                lambda video: self.list_widget.txtFilter.text().lower()
                in video.title.lower(),
                self.video_loader_thread.availableVideos,
            )
        )
        self.fill_table(self.filtered_videos)

    def next_videos(self, availableVideos: List[Video]):
        next_videos = channel_data.get_videos2(self.channel)
        self.video_loader_thread.availableVideos += next_videos
        self.handle_video_loading(availableVideos + next_videos)

    def download_all(self):
        if not self.download_path:
            self.handle_download_error(
                "Please select a download folder before downloading."
            )
        else:
            self.download_next(0)

    def download_next(self, row):
        if row < self.list_widget.tableWidget.rowCount():
            download_button = self.list_widget.tableWidget.cellWidget(row, 2).findChild(
                QPushButton
            )
            if download_button.isEnabled():
                download_button.click()
                QTimer.singleShot(1000, lambda: self.download_next(row + 1))
            else:
                QTimer.singleShot(500, lambda: self.download_next(row))
        else:
            self.show_message("All downloads completed!")

    def handle_download_completed(self):
        self.list_widget.spinner_label.hide()
        self.list_widget.tableWidget.setEnabled(True)

    def back_home(self):
        from gui.home import Home

        self.home = Home()
        # self.video_loader_thread.quit()  # Finalizar el hilo de carga de vídeos
        # self.video_loader_thread.wait()  # Esperar a que el hilo termine
        # self.reset_instance()

        self.list_widget.close()
        self.list_widget.deleteLater()

    def select_download_path(self):
        selected_path = QFileDialog.getExistingDirectory(
            self.list_widget, "Select Download Folder", self.download_path
        )
        if selected_path:  # Only if the user updates the downloads path
            self.download_path = selected_path
            self.list_widget.lblSelectedPath.setText(
                "../" + os.path.basename(selected_path)
            )

    def handle_download_error(self, error_message: str):
        QMessageBox.critical(
            self.list_widget,
            "Error",
            error_message,
            QMessageBox.StandardButton.Ok,
        )

    def show_message(self, message: str):
        self.list_widget.lblMessage.setText(message)

    def set_download_path(self, path: str):  # Testing purpose
        self.download_path = path
