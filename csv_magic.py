import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QMainWindow, QToolBar, QFileDialog, QGridLayout, QLabel, QDoubleSpinBox,
                               QWidget)

SPINBOX_DEFAULT = 1.5
WIDTH = 600
HEIGHT = 400


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        window = QWidget()
        toolbar = QToolBar()
        grid = QGridLayout()

        double_spin_box_plus = QDoubleSpinBox()
        double_spin_box_plus.setPrefix("+ ")
        double_spin_box_plus.setValue(SPINBOX_DEFAULT)
        double_spin_box_minus = QDoubleSpinBox()
        double_spin_box_minus.setPrefix("- ")
        double_spin_box_minus.setValue(SPINBOX_DEFAULT)

        load_action = QAction("Load...", self, shortcut="Ctrl+L", triggered=self.load)
        exit_action = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)

        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(load_action)
        file_menu.addAction(exit_action)

        toolbar.addAction(load_action)

        grid.addWidget(double_spin_box_minus, 0, 0)
        grid.addWidget(double_spin_box_plus, 0, 1)

        self.addToolBar(toolbar)
        window.setLayout(grid)
        self.setCentralWidget(window)
        self.setGeometry(300, 300, WIDTH, HEIGHT)
        self.setWindowTitle("CSV Magic")
        self.show()

    def load(self):
        file_name = QFileDialog.getOpenFileName(self, caption="Open CSV", dir=".", filter="CSV Files (*.csv)")

        if file_name:
            print(file_name[0])


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
