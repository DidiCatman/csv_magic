import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QMainWindow, QToolBar, QFileDialog, QGridLayout, QDoubleSpinBox,
                               QWidget, QTableWidget, QTableWidgetItem)

SPINBOX_DEFAULT = 1.5
SPINBOX_SINGLE_STEP = 0.1
WIDTH = 600
HEIGHT = 400


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # setup widgets
        win = QWidget()
        toolbar = QToolBar()
        grid = QGridLayout()
        self.table = QTableWidget()

        double_spin_box_plus = QDoubleSpinBox(prefix='+ ', suffix=' mm',
                                              value=SPINBOX_DEFAULT, singleStep=SPINBOX_SINGLE_STEP)
        double_spin_box_minus = QDoubleSpinBox(prefix='- ', suffix=' mm',
                                               value=SPINBOX_DEFAULT, singleStep=SPINBOX_SINGLE_STEP)

        # setup actions
        load_action = QAction('Load...', self, shortcut='Ctrl+L', triggered=self.load)
        add_pos_action = QAction('Add Positions', self, shortcut='Ctrl+A', triggered=self.add_position)
        save_action = QAction('Save', self, shortcut='Ctrl+S', triggered=self.save)
        exit_action = QAction('Exit', self, shortcut='Ctrl+Q', triggered=self.close)

        # setup file menu
        file_menu = self.menuBar().addMenu('&File')
        file_menu.addAction(load_action)
        file_menu.addAction(add_pos_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        # setup toolbar
        toolbar.addAction(load_action)
        toolbar.addAction(add_pos_action)
        toolbar.addAction(save_action)

        # create grid layout
        grid.addWidget(double_spin_box_minus, 0, 0)
        grid.addWidget(double_spin_box_plus, 0, 1)
        grid.addWidget(self.table, 1, 0, 1, 2)  # row, column, height, width
        win.setLayout(grid)

        # general setup
        self.setCentralWidget(win)
        self.addToolBar(toolbar)
        self.setGeometry(300, 300, WIDTH, HEIGHT)
        self.setWindowTitle('CSV Magic')
        self.show()

    def load(self):
        file_name = QFileDialog.getOpenFileName(self, caption='Open CSV', dir='.', filter='CSV Files (*.csv)')

        if file_name:
            print(file_name[0])
            with open(file_name[0]) as f:

                csv = []
                [csv.append(line[:-1].split(';')) for line in f.readlines()]

                self.table.setRowCount(len(csv) - 1)
                self.table.setColumnCount(len(csv[0]))
                self.table.setHorizontalHeaderLabels(csv[0])

                for i, col in enumerate(csv[1:]):
                    for n, value in enumerate(col):
                        self.table.setItem(i, n, QTableWidgetItem(value))


    def save(self):
        pass

    def add_position(self):
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
