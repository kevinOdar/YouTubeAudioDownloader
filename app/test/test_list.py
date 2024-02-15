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


@pytest.fixture
def temporary_test_folder():
    test_directory = os.path.dirname(__file__)
    temp_folder = os.path.join(test_directory, "test_folder")
    os.makedirs(temp_folder)
    yield temp_folder
    shutil.rmtree(temp_folder)


@pytest.fixture
def list_window_fixture(qtbot):
    home_window = Home()
    qtbot.addWidget(home_window)
    channel_name = "NonExistentChannel"
    QTest.keyClicks(home_window.home.txtChannel, channel_name)

    QTest.mouseMove(home_window.home.btnSearch)
    QTest.mouseClick(home_window.home.btnSearch, Qt.MouseButton.LeftButton)
    return home_window.list


def test_list_elements_appear(list_window_fixture, qtbot):
    list_widget = list_window_fixture.list_widget
    assert list_widget.spinner_label.isVisible()
    assert list_widget.btnDownloadAll.isVisible()
    assert not list_widget.btnDownloadAll.isEnabled()
    assert list_widget.txtFilter.isVisible()
    assert not list_widget.txtFilter.isEnabled()
    assert list_widget.lblSelectedPath.isVisible()
    assert list_widget.btnBack.isVisible()
    assert list_widget.tableWidget.isVisible()


def test_list_shows_elements(list_window_fixture, qtbot):
    list_widget = list_window_fixture.list_widget
    qtbot.waitUntil(
        lambda: list_widget.tableWidget.isVisible()
        and list_widget.tableWidget.rowCount() > 0,
        timeout=50000,
    )

    assert list_widget.tableWidget.rowCount() == 7  # 7 videos

    button_first_video = list_widget.tableWidget.cellWidget(0, 2).findChild(QPushButton)
    button_latest_video = list_widget.tableWidget.cellWidget(6, 2).findChild(
        QPushButton
    )

    assert isinstance(button_first_video, QPushButton)
    assert isinstance(button_latest_video, QPushButton)
    assert button_first_video.text() == "Download"
    assert button_latest_video.text() == "Download"


def test_download_one_element(list_window_fixture, qtbot, temporary_test_folder):

    list_widget = list_window_fixture.list_widget
    qtbot.waitUntil(
        lambda: list_widget.tableWidget.isVisible()
        and list_widget.tableWidget.rowCount() > 0,
        timeout=60000,
    )

    list_window_fixture.set_download_path(temporary_test_folder)
    button_first_video = list_widget.tableWidget.cellWidget(0, 2).findChild(QPushButton)

    qtbot.mouseClick(button_first_video, Qt.MouseButton.LeftButton)
    qtbot.wait(10000)  # download time

    mp3_file_path = os.path.join(temporary_test_folder, "◄Slark 25mmrsec► │VOL.1│.mp3")
    assert os.path.exists(mp3_file_path)

    assert (
        list_widget.lblMessage.text()
    ) == '"◄Slark 25mmr/sec► │VOL.1│" downloaded successfully'


@pytest.mark.only
def test_shows_message_already_downloaded(
    list_window_fixture, qtbot, temporary_test_folder
):

    list_widget = list_window_fixture.list_widget
    qtbot.waitUntil(
        lambda: list_widget.tableWidget.isVisible()
        and list_widget.tableWidget.rowCount() > 0,
        timeout=60000,
    )

    list_window_fixture.set_download_path(temporary_test_folder)
    button_first_video = list_widget.tableWidget.cellWidget(0, 2).findChild(QPushButton)

    qtbot.mouseClick(button_first_video, Qt.MouseButton.LeftButton)

    mp3_file_path = os.path.join(temporary_test_folder, "◄Slark 25mmrsec► │VOL.1│.mp3")
    qtbot.wait(10000)  # download time

    qtbot.mouseClick(button_first_video, Qt.MouseButton.LeftButton)

    qtbot.wait(5000)

    assert os.path.exists(mp3_file_path)
    assert (
        list_widget.lblMessage.text()
    ) == '"◄Slark 25mmr/sec► │VOL.1│" was already downloaded'


def test_filter_and_download(list_window_fixture, qtbot, temporary_test_folder):
    list_widget = list_window_fixture.list_widget
    qtbot.waitUntil(
        lambda: list_widget.tableWidget.isVisible()
        and list_widget.tableWidget.rowCount() > 0,
        timeout=60000,
    )

    list_window_fixture.set_download_path(temporary_test_folder)

    qtbot.keyClicks(list_widget.txtFilter, "pudge")

    qtbot.waitUntil(
        lambda: list_widget.tableWidget.rowCount() == 2,
        timeout=5000,
    )

    qtbot.mouseClick(list_widget.btnDownloadAll, Qt.MouseButton.LeftButton)
    qtbot.wait(15000)  # download time
    mp3_file_path1 = os.path.join(temporary_test_folder, "◄Pudge 25mmrsec► │VOL.1│.mp3")
    mp3_file_path2 = os.path.join(temporary_test_folder, "◄Pudge 25mmrsec► │VOL.2│.mp3")
    assert os.path.exists(mp3_file_path1)
    assert os.path.exists(mp3_file_path2)
    assert (
        list_widget.lblMessage.text()
    ) == '"◄Pudge 25mmr/sec► │VOL.1│" downloaded successfully'


def test_download_button_is_blocked_until_download_finishes(
    list_window_fixture, qtbot, temporary_test_folder
):
    list_widget = list_window_fixture.list_widget
    qtbot.waitUntil(
        lambda: list_widget.tableWidget.isVisible()
        and list_widget.tableWidget.rowCount() > 0,
        timeout=60000,
    )

    list_window_fixture.set_download_path(temporary_test_folder)
    button_third_video = list_widget.tableWidget.cellWidget(2, 2).findChild(QPushButton)

    qtbot.mouseClick(button_third_video, Qt.MouseButton.LeftButton)

    assert not button_third_video.isEnabled()
    qtbot.wait(10000)  # download time
    assert button_third_video.isEnabled()
