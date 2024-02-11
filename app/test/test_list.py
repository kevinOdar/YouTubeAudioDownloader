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


def test_list_elements_appear(list_test, qtbot):
    assert list_test.list.spinner_label.isVisible()
    assert list_test.list.btnDownloadAll.isVisible()
    assert list_test.list.lblSelectedPath.isVisible()
    assert list_test.list.btnBack.isVisible()
    assert list_test.list.tableWidget.isVisible()


def test_list_shows_elements(list_test, qtbot):
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
    qtbot.wait(10000)  # download time

    mp3_file_path = os.path.join(temporal_test_folder, "◄Slark 25mmrsec► │VOL.1│.mp3")
    assert os.path.exists(mp3_file_path)
    assert (
        list_test.list.lblMessage.text()
    ), '"◄Slark 25mmrsec► │VOL.1│" downloaded successfully'


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
    qtbot.wait(10000)  # download time

    list_test.set_download_path(temporal_test_folder)
    button_first_video = list_test.list.tableWidget.cellWidget(0, 2).findChild(
        QPushButton
    )

    qtbot.mouseClick(button_first_video, Qt.MouseButton.LeftButton)

    assert os.path.exists(mp3_file_path)
    assert (
        list_test.list.lblMessage.text()
    ), '"◄Slark 25mmrsec► │VOL.1│" was already downloaded'


# @pytest.mark.only
def test_filter_and_download(list_test, qtbot, temporal_test_folder):
    # Wait until the table is visible and populated
    qtbot.waitUntil(
        lambda: list_test.list.tableWidget.isVisible()
        and list_test.list.tableWidget.rowCount() > 0,
        timeout=60000,
    )

    list_test.set_download_path(temporal_test_folder)

    qtbot.keyClicks(list_test.list.txtFilter, "pudge")

    qtbot.waitUntil(
        lambda: list_test.list.tableWidget.rowCount() == 2,
        timeout=5000,
    )

    qtbot.mouseClick(list_test.list.btnDownloadAll, Qt.MouseButton.LeftButton)

    mp3_file_path1 = os.path.join(temporal_test_folder, "◄Pudge 25mmrsec► │VOL.1│.mp3")
    mp3_file_path2 = os.path.join(temporal_test_folder, "◄Pudge 25mmrsec► │VOL.2│.mp3")
    assert os.path.exists(mp3_file_path1)
    assert os.path.exists(mp3_file_path2)
    assert (
        list_test.list.lblMessage.text()
    ), '"◄Pudge 25mmr/sec► │VOL.1│" downloaded successfully'
