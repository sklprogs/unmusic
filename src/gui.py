#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6
import PyQt6.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class AlbumEditor(PyQt6.QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def set_layout(self):
        self.parent = PyQt6.QtWidgets.QWidget()
        self.layout_ = PyQt6.QtWidgets.QGridLayout()
        #self.layout_.setContentsMargins(0, 0, 0, 0)
    
    def set_labels(self):
        self.lbl_art = PyQt6.QtWidgets.QLabel()
        self.lbl_alb = PyQt6.QtWidgets.QLabel()
        self.lbl_yer = PyQt6.QtWidgets.QLabel()
        self.lbl_cnt = PyQt6.QtWidgets.QLabel()
        self.lbl_com = PyQt6.QtWidgets.QLabel()
        self.lbl_bit = PyQt6.QtWidgets.QLabel()
        self.lbl_len = PyQt6.QtWidgets.QLabel()
    
    def set_entries(self):
        self.ent_art = PyQt6.QtWidgets.QLineEdit()
        self.ent_alb = PyQt6.QtWidgets.QLineEdit()
        self.ent_yer = PyQt6.QtWidgets.QLineEdit()
        self.ent_cnt = PyQt6.QtWidgets.QLineEdit()
        self.ent_com = PyQt6.QtWidgets.QLineEdit()
        self.ent_bit = PyQt6.QtWidgets.QLineEdit()
        self.ent_len = PyQt6.QtWidgets.QLineEdit()
    
    def set_widgets(self):
        self.set_labels()
        self.set_entries()
        self.set_text()
    
    def set_text(self):
        self.lbl_art.setText(_('Artist:'))
        self.lbl_alb.setText(_('Album:'))
        self.lbl_yer.setText(_('Year:'))
        self.lbl_cnt.setText(_('Country:'))
        self.lbl_com.setText(_('Comment:'))
        self.lbl_bit.setText(_('Average bitrate:'))
        self.lbl_len.setText(_('Total length:'))
    
    def set_gui(self):
        self.set_layout()
        self.set_widgets()
        self.add_widgets()
        self.setCentralWidget(self.parent)
    
    def add_labels(self):
        self.layout_.addWidget(self.lbl_art, 0, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_alb, 1, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_yer, 2, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_cnt, 3, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_com, 4, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_bit, 5, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_len, 6, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
    
    def add_entries(self):
        self.layout_.addWidget(self.ent_art, 0, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_alb, 1, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_yer, 2, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_cnt, 3, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_com, 4, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_bit, 5, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_len, 6, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
    
    def add_widgets(self):
        self.add_labels()
        self.add_entries()
        self.parent.setLayout(self.layout_)


if __name__ == '__main__':
    f = '__main__'
    import sys
    exe = PyQt6.QtWidgets.QApplication(sys.argv)
    app = AlbumEditor()
    app.show()
    sys.exit(exe.exec())
