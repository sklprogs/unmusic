#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import PyQt6
import PyQt6.QtWidgets


class App(PyQt6.QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_layout(self):
        self.parent = PyQt6.QtWidgets.QWidget()
        self.layout_ = PyQt6.QtWidgets.QGridLayout()
        #self.layout_.setContentsMargins(0, 0, 0, 0)
    
    def set_widgets(self):
        self.lbl_art = PyQt6.QtWidgets.QLabel()
        self.lbl_art.setText('Artist:')
        self.ent_art = PyQt6.QtWidgets.QLineEdit()
    
    def set_gui(self):
        self.set_layout()
        self.set_widgets()
        self.add_widgets()
        self.setCentralWidget(self.parent)
    
    def add_widgets(self):
        self.layout_.addWidget(self.lbl_art, 0, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_art, 0, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.parent.setLayout(self.layout_)


if __name__ == '__main__':
    f = '__main__'
    exe = PyQt6.QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    sys.exit(exe.exec())
