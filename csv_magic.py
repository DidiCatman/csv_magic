#!/usr/bin/env python3

__author__ = 'Dieter Skroblin'
__version__ = '1.0.0'
__license__ = 'GPL'

import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QMainWindow, QToolBar, QFileDialog, QGridLayout, QDoubleSpinBox,
                               QWidget, QTableWidget, QTableWidgetItem, QMessageBox)

SPINBOX_DEFAULT = 1.5
SPINBOX_SINGLE_STEP = 0.1
WIDTH = 600
HEIGHT = 600


def msg_box(string):
    m_box = QMessageBox()
    m_box.setText(string)
    m_box.exec()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # setup widgets
        win = QWidget()
        toolbar = QToolBar()
        grid = QGridLayout()
        self.table = QTableWidget()
        self.file_name = None

        self.double_spin_box_plus = QDoubleSpinBox(prefix='+ ', suffix=' mm',
                                                   value=SPINBOX_DEFAULT, singleStep=SPINBOX_SINGLE_STEP)
        self.double_spin_box_minus = QDoubleSpinBox(prefix='- ', suffix=' mm',
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
        grid.addWidget(self.double_spin_box_minus, 0, 0)
        grid.addWidget(self.double_spin_box_plus, 0, 1)
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
            print('load {}'.format(self.file_name[0]))
            if not self.file_name == '':
                with open(self.file_name[0]) as f:
                    lines = f.readlines()
                    if len(lines) <= 2:
                        msg_box('No valid csv!')
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
        if not self.file_name:
            msg_box('No csv loaded!')
        elif not self.table.selectedIndexes():
            msg_box('No selection!')
        else:
            # retrieve row and column indexes of selection
            selected_indexes = self.table.selectedIndexes()
            selected_rows = [index.row() for index in selected_indexes]
            selected_columns = [index.column() for index in selected_indexes]

            # insert new (copy) rows
            offset = 0
            new_index = []
            for row in set(selected_rows):
                current_row = row + offset
                if not self.double_spin_box_minus.value() == 0.0:
                    offset += 1
                    # insert row before
                    current_row = row + offset
                    self.table.insertRow(current_row - 1)
                    for x in range(self.table.columnCount()):
                        item = QTableWidgetItem(self.table.item(current_row, x).text())
                        self.table.setItem(current_row - 1, x, item)
                new_index.append(current_row)
                if not self.double_spin_box_plus.value() == 0.0:
                    offset += 1
                    # insert row after
                    self.table.insertRow(current_row + 1)
                    for x in range(self.table.columnCount()):
                        item = QTableWidgetItem(self.table.item(current_row, x).text())
                        self.table.setItem(current_row + 1, x, item)

            # create list with new selected row indexes
            new_selected_rows = [0] * len(selected_rows)
            for s, n in zip(set(selected_rows), new_index):
                index = [i for i, e in enumerate(selected_rows) if e == s]  # find index of set value
                for i in index:
                    new_selected_rows[i] = n  # replace with new index value

            # insert new values
            for y, x in zip(new_selected_rows, selected_columns):
                current_value = float(self.table.item(y, x).text())
                if not self.double_spin_box_minus.value() == 0.0:
                    new_value = current_value - self.double_spin_box_minus.value()
                    self.table.setItem(y - 1, x, QTableWidgetItem(str(new_value)))
                if not self.double_spin_box_plus.value() == 0.0:
                    new_value = current_value + self.double_spin_box_minus.value()
                    self.table.setItem(y + 1, x, QTableWidgetItem(str(new_value)))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
