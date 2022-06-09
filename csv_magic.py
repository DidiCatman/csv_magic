import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QMainWindow, QToolBar, QFileDialog, QGridLayout, QDoubleSpinBox,
                               QWidget, QTableWidget, QTableWidgetItem, QMessageBox)

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
        self.file_name = None

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
        self.file_name = QFileDialog.getOpenFileName(self, caption='Open CSV', dir='.', filter='CSV Files (*.csv)')

        if self.file_name:
            print(self.file_name[0])
            if not self.file_name == '':
                with open(self.file_name[0]) as f:

                    lines = f.readlines()

                    if len(lines) <= 2:
                        msg_box = QMessageBox()
                        msg_box.setText('No valid csv!')
                        msg_box.exec()
                    else:
                        csv = []
                        [csv.append(line[:-1].split(';')) for line in lines]

                        self.table.setRowCount(len(csv) - 1)
                        self.table.setColumnCount(len(csv[0]))
                        self.table.setHorizontalHeaderLabels(csv[0])

                        for y, col in enumerate(csv[1:]):
                            for x, value in enumerate(col):
                                self.table.setItem(y, x, QTableWidgetItem(value))

    def save(self):
        if self.file_name:
            with open('{}_edit.csv'.format(self.file_name[0].split('.')[0]), 'w') as f:
                headers = [self.table.horizontalHeaderItem(c) for c in range(self.table.rowCount() + 1)]
                labels = [x.text() for x in headers if x is not None]
                csv = [';'.join(labels) + '\n']
                for y in range(self.table.rowCount()):
                    line = []
                    for x in range(self.table.columnCount()):
                        item = self.table.item(y, x)
                        if item is not None:
                            line.append(item.text())
                    csv.append(';'.join(line) + '\n')
                f.writelines(csv)

    def add_position(self):
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
