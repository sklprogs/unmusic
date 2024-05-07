#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6
import PyQt6.QtWidgets
import PyQt6.QtGui

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Test(PyQt6.QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def set_layout(self, widget):
        self.pnl_tst = PyQt6.QtWidgets.QWidget()
        self.lay_tst = PyQt6.QtWidgets.QVBoxLayout()
        self.lay_tst.addWidget(widget)
        self.pnl_tst.setLayout(self.lay_tst)
    
    def set_gui(self, widget):
        self.set_layout(widget)
        self.setCentralWidget(self.pnl_tst)
