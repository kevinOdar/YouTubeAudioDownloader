import os
import sys
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from gui.home import Home
from data.channel import Channel
import pytest
from unittest.mock import Mock


@pytest.fixture
def home_test(qtbot):
    ventana = Home()
    qtbot.addWidget(ventana)
    return ventana


@pytest.fixture
def mocker():
    return Mock()


def test_user_doesnt_enter_a_channel(home_test, qtbot):
    print("entra aca")
    QTest.mouseMove(home_test.home.btnSearch)
    QTest.mouseClick(home_test.home.btnSearch, Qt.MouseButton.LeftButton)
    assert home_test.home.lblMessage.text() == "Please, enter a channel name"


def test_user_entered_an_invalid_channel(home_test, qtbot):
    QTest.mouseMove(home_test.home.txtChannel)
    QTest.mouseClick(home_test.home.txtChannel, Qt.MouseButton.LeftButton)

    channel_name = "NonExistentChannel2"
    QTest.keyClicks(home_test.home.txtChannel, channel_name)
    assert home_test.home.txtChannel.text() == channel_name

    QTest.mouseMove(home_test.home.btnSearch)
    QTest.mouseClick(home_test.home.btnSearch, Qt.MouseButton.LeftButton)
    assert home_test.home.lblMessage.text() == "The channel doesn't exist"


def test_user_enters_valid_channel_and_shows_list_window(home_test, qtbot, mocker):
    channel_name = "NonExistentChannel"
    QTest.keyClicks(home_test.home.txtChannel, channel_name)
    assert home_test.home.txtChannel.text() == channel_name

    mocker.return_value.status_code = 200

    QTest.mouseMove(home_test.home.btnSearch)
    QTest.mouseClick(home_test.home.btnSearch, Qt.MouseButton.LeftButton)

    assert home_test.list is not None
    assert not home_test.home.isVisible()
