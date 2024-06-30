#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6
import PyQt6.QtWidgets
import PyQt6.QtGui

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import tracks.gui


class Tracks(tracks.gui.Tracks):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_title(self):
        self.pnl_trs.setWindowTitle(_('Track Search'))



class Track(tracks.gui.Track):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def dump(self):
        return (self.ent_alb.get(), self.ent_tit.get(), self.ent_lyr.get()
               ,self.ent_com.get(), int(self.opt_rtg.get())
               )
    
    def configure(self):
        self.ent_alb.disable()
        self.ent_tno.disable()
        self.ent_bit.disable()
        self.ent_len.disable()
        self.ent_tno.widget.setMinimumWidth(180)
        self.ent_tit.widget.setMinimumWidth(180)
        self.ent_lyr.widget.setMinimumWidth(180)
        self.ent_com.widget.setMinimumWidth(180)
        self.ent_bit.widget.setMinimumWidth(180)
        self.ent_len.widget.setMinimumWidth(180)
    
    def reset(self):
        self.ent_alb.clear()
        self.ent_tno.clear()
        self.ent_tit.clear()
        self.ent_lyr.clear()
        self.ent_com.clear()
        self.ent_bit.clear()
        self.ent_len.clear()
        self.opt_rtg.set(0)
    
    def set_entries(self):
        self.ent_alb = sh.Entry()
        self.ent_tno = sh.Entry()
        self.ent_tit = sh.Entry()
        self.ent_lyr = sh.Entry()
        self.ent_com = sh.Entry()
        self.ent_bit = sh.Entry()
        self.ent_len = sh.Entry()
    
    def set_labels(self):
        self.lbl_alb = sh.Label(_('Album #:'))
        self.lbl_tno = sh.Label(_('Track #:'))
        self.lbl_tit = sh.Label(_('Title:'))
        self.lbl_lyr = sh.Label(_('Lyrics:'))
        self.lbl_com = sh.Label(_('Comment:'))
        self.lbl_bit = sh.Label(_('Bitrate:'))
        self.lbl_len = sh.Label(_('Length:'))
        self.lbl_rtg = sh.Label(_('Rating:'))
    
    def add_labels(self):
        self.lay_trk.addWidget(self.lbl_alb.widget, 0, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_tno.widget, 1, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_tit.widget, 2, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_lyr.widget, 3, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_com.widget, 4, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_bit.widget, 5, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_len.widget, 6, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_rtg.widget, 7, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
    
    def add_entries(self):
        self.lay_trk.addWidget(self.ent_alb.widget, 0, 1, 1, 1)
        self.lay_trk.addWidget(self.ent_tno.widget, 1, 1, 1, 1)
        self.lay_trk.addWidget(self.ent_tit.widget, 2, 1, 1, 1)
        self.lay_trk.addWidget(self.ent_lyr.widget, 3, 1, 1, 1)
        self.lay_trk.addWidget(self.ent_com.widget, 4, 1, 1, 1)
        self.lay_trk.addWidget(self.ent_bit.widget, 5, 1, 1, 1)
        self.lay_trk.addWidget(self.ent_len.widget, 6, 1, 1, 1)
    
    def add_options(self):
        self.lay_trk.addWidget(self.opt_rtg.widget, 7, 1, 1, 1)
