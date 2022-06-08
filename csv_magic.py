# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press Strg+F8 to toggle the breakpoint.

from PySide6.QtWidgets import QApplication, QMainWindow
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle("Window Title")
        self.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
