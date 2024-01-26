from gui.home import Home
from PyQt6.QtWidgets import QApplication


class App:
    def __init__(self) -> None:
        self.app = QApplication([])
        self.home = Home()

        self.app.exec()


app = App()
