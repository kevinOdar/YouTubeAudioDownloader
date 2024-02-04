import os
import shutil
import sys
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QPushButton

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from gui.home import Home
import pytest
from unittest.mock import Mock


@pytest.fixture
def temporal_test_folder():
    test_directory = os.path.dirname(__file__)
    temp_folder = os.path.join(test_directory, "test_folder")
    os.makedirs(temp_folder)
    yield temp_folder
    shutil.rmtree(temp_folder)


@pytest.fixture
def list_test(qtbot):
    home_window = Home()
    qtbot.addWidget(home_window)
    channel_name = "NonExistentChannel"
    QTest.keyClicks(home_window.home.txtChannel, channel_name)

    QTest.mouseMove(home_window.home.btnSearch)
    QTest.mouseClick(home_window.home.btnSearch, Qt.MouseButton.LeftButton)
    return home_window.list


# @pytest.fixture
# def mocker():
#     return Mock()


def test_list_elements_appear(list_test, qtbot):
    assert list_test.list.spinner_label.isVisible()
    assert list_test.list.btnDownloadAll.isVisible()
    assert list_test.list.lblSelectedPath.isVisible()
    assert list_test.list.btnBack.isVisible()
    assert list_test.list.tableWidget.isVisible()


def test_elements_appear(list_test, qtbot):
    qtbot.waitUntil(
        lambda: list_test.list.tableWidget.isVisible()
        and list_test.list.tableWidget.rowCount() > 0,
        timeout=50000,
    )

    assert list_test.list.tableWidget.rowCount(), 7  # 7 videos

    button_first_video = list_test.list.tableWidget.cellWidget(0, 2).findChild(
        QPushButton
    )
    button_latest_video = list_test.list.tableWidget.cellWidget(6, 2).findChild(
        QPushButton
    )

    assert isinstance(button_first_video, QPushButton)
    assert isinstance(button_latest_video, QPushButton)
    assert button_first_video.text(), "Download"
    assert button_latest_video.text(), "Download"


@pytest.mark.only
def test_download_one_element(list_test, qtbot, temporal_test_folder):

    qtbot.waitUntil(
        lambda: list_test.list.tableWidget.isVisible()
        and list_test.list.tableWidget.rowCount() > 0,
        timeout=60000,
    )

    # qtbot.mouseClick(list_test.list.btnSelectPath, Qt.MouseButton.LeftButton)

    list_test.set_download_path(temporal_test_folder)
    button_first_video = list_test.list.tableWidget.cellWidget(0, 2).findChild(
        QPushButton
    )

    qtbot.mouseClick(button_first_video, Qt.MouseButton.LeftButton)

    mp3_file_path = os.path.join(temporal_test_folder, "◄Slark 25mmrsec► │VOL.1│.mp3")
    assert os.path.exists(mp3_file_path)
    assert (
        list_test.list.lblMessage.text()
    ), '"◄Slark 25mmrsec► │VOL.1│" was successfully downloaded'


@pytest.mark.only
def test_shows_message_already_downloaded(list_test, qtbot, temporal_test_folder):

    qtbot.waitUntil(
        lambda: list_test.list.tableWidget.isVisible()
        and list_test.list.tableWidget.rowCount() > 0,
        timeout=60000,
    )

    # qtbot.mouseClick(list_test.list.btnSelectPath, Qt.MouseButton.LeftButton)

    list_test.set_download_path(temporal_test_folder)
    button_first_video = list_test.list.tableWidget.cellWidget(0, 2).findChild(
        QPushButton
    )

    qtbot.mouseClick(button_first_video, Qt.MouseButton.LeftButton)

    mp3_file_path = os.path.join(temporal_test_folder, "◄Slark 25mmrsec► │VOL.1│.mp3")
    qtbot.wait(10000)

    list_test.set_download_path(temporal_test_folder)
    button_first_video = list_test.list.tableWidget.cellWidget(0, 2).findChild(
        QPushButton
    )

    qtbot.mouseClick(button_first_video, Qt.MouseButton.LeftButton)

    assert os.path.exists(mp3_file_path)
    assert (
        list_test.list.lblMessage.text()
    ), '"◄Slark 25mmrsec► │VOL.1│" was already downloaded'
