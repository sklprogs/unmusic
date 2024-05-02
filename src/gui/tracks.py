#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6
import PyQt6.QtWidgets
import PyQt6.QtGui

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Track:
    
    def __init__(self):
        self.set_gui()
    
    def set_layout(self):
        self.pnl_trk = PyQt6.QtWidgets.QWidget()
        self.lay_trk = PyQt6.QtWidgets.QGridLayout()
        self.pnl_trk.setLayout(self.lay_trk)
    
    def set_entries(self):
        self.ent_tno = sh.Entry()
        self.ent_tit = sh.Entry()
        self.ent_lyr = sh.Entry()
        self.ent_com = sh.Entry()
        self.ent_bit = sh.Entry()
        self.ent_len = sh.Entry()
    
    def set_labels(self):
        self.lbl_tno = sh.Label(_('Track #:'))
        self.lbl_tit = sh.Label(_('Title:'))
        self.lbl_lyr = sh.Label(_('Lyrics:'))
        self.lbl_com = sh.Label(_('Comment:'))
        self.lbl_bit = sh.Label(_('Bitrate:'))
        self.lbl_len = sh.Label(_('Length:'))
        self.lbl_rtg = sh.Label(_('Rating:'))
    
    def set_options(self):
        self.opt_rtg = sh.OptionMenu((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    
    def add_labels(self):
        self.lay_trk.addWidget(self.lbl_tno.widget, 0, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_tit.widget, 1, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_lyr.widget, 2, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_com.widget, 3, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_bit.widget, 4, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_len.widget, 5, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_rtg.widget, 6, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
    
    def add_entries(self):
        self.lay_trk.addWidget(self.ent_tno.widget, 0, 1, 1, 1)
        self.lay_trk.addWidget(self.ent_tit.widget, 1, 1, 1, 1)
        self.lay_trk.addWidget(self.ent_lyr.widget, 2, 1, 1, 1)
        self.lay_trk.addWidget(self.ent_com.widget, 3, 1, 1, 1)
        self.lay_trk.addWidget(self.ent_bit.widget, 4, 1, 1, 1)
        self.lay_trk.addWidget(self.ent_len.widget, 5, 1, 1, 1)
    
    def add_options(self):
        self.lay_trk.addWidget(self.opt_rtg.widget, 6, 1, 1, 1)
    
    def set_widgets(self):
        self.set_labels()
        self.set_entries()
        self.set_options()
    
    def add_widgets(self):
        self.add_labels()
        self.add_entries()
        self.add_options()
    
    def set_gui(self):
        self.set_layout()
        self.set_widgets()
        self.add_widgets()
