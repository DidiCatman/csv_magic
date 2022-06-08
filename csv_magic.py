# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press Strg+F8 to toggle the breakpoint.

import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle("CSV Magic")

        toolbar = QToolBar()
        self.addToolBar(toolbar)
        file_menu = self.menuBar().addMenu("&File")
        load_action = QAction("Load...", self, shortcut="Ctrl+L", triggered=self.load)
        file_menu.addAction(load_action)
        toolbar.addAction(load_action)
        exit_action = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        file_menu.addAction(exit_action)

        self.show()

    def load(self):
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
