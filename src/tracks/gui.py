#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QGridLayout, QLayout, QScrollArea
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtCore import Qt, QObject, pyqtSignal

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.paths import PDIR
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.button.controller import Button
from skl_shared.graphics.label.controller import Label
from skl_shared.graphics.entry.controller import Entry
from skl_shared.graphics.option_menu.controller import OptionMenu


class Bottom:
    
    def __init__(self):
        self.set_values()
        self.set_gui()
    
    def set_values(self):
        self.icn_rld = PDIR.add('..', 'resources', 'buttons', 'reload.png')
        self.icn_zer = PDIR.add('..', 'resources', 'buttons', 'zero_rating.png')
        self.icn_dec = PDIR.add('..', 'resources', 'buttons', 'decode.png')

    def set_layout(self):
        self.pnl_btm = QWidget()
        self.lay_btm = QGridLayout(self.pnl_btm)
        self.lay_btm.setContentsMargins(10, 2, 10, 7)
        self.pnl_btm.setLayout(self.lay_btm)
    
    def set_gui(self):
        self.set_layout()
        self.set_widgets()
        self.add_widgets()
        self.configure()
    
    def configure(self):
        policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_rld.widget.setSizePolicy(policy)
        self.btn_zer.widget.setSizePolicy(policy)
        self.btn_dec.widget.setSizePolicy(policy)
    
    def set_widgets(self):
        self.btn_rld = Button(hint = _('Reload the present record')
                             ,inactive = self.icn_rld
                             ,active = self.icn_rld)
        self.btn_zer = Button(hint = _('Zero rating for all tracks')
                             ,inactive = self.icn_zer
                             ,active = self.icn_zer)
        self.btn_dec = Button(hint = _('Decode back to cp1251')
                             ,inactive = self.icn_dec
                             ,active = self.icn_dec)
        self.pnl_btm.setLayout(self.lay_btm)
    
    def add_widgets(self):
        self.lay_btm.addWidget(self.btn_rld.widget, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.lay_btm.addWidget(self.btn_zer.widget, 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.lay_btm.addWidget(self.btn_dec.widget, 0, 2, 1, 6, Qt.AlignmentFlag.AlignLeft)



class Signal(QObject):
    # Separate from Tracks; otherwise, the following error is thrown:
    # TypeError: Tracks cannot be converted to QObject
    sig_rating = pyqtSignal()
    sig_info = pyqtSignal(str)



class Top(QWidget):
    
    sig_close = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def update_size(self):
        self.resize(self.sizeHint())
        self.updateGeometry()
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)



class Tracks:
    
    def __init__(self):
        self.set_gui()
        self.signal = Signal()
    
    def update_size(self):
        self.pnl_scr.update_size()
    
    def send_rating(self):
        self.signal.sig_rating.emit()
    
    def send_info(self, mes):
        self.signal.sig_info.emit(mes)
    
    def centralize(self):
        ''' Do this only after showing the widget; otherwise, it will have
            bogus dimensions of 640×480.
        '''
        self.pnl_trs.move(ROOT.get_root().primaryScreen().geometry().center() - self.pnl_trs.rect().center())
    
    def set_title(self):
        self.pnl_trs.setWindowTitle(_('Tracks'))
    
    def go_start(self):
        slider = self.scroll_area.verticalScrollBar()
        slider.setValue(slider.minimum())
    
    def go_end(self):
        slider = self.scroll_area.verticalScrollBar()
        slider.setValue(slider.maximum())
    
    def set_scroll(self):
        self.scroll_area = QScrollArea(self.pnl_trs)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.lay_trs.addWidget(self.scroll_area)
        self.lay_trs.addWidget(self.bottom.pnl_btm)
        self.pnl_scr = Top(self.scroll_area)
        self.lay_scr = QVBoxLayout(self.pnl_scr)
        ''' Prevent tracks (QLineEdit) from gaining too much space between each
            other, e.g. when there is only one track for the whole album (#2).
        '''
        self.lay_scr.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.lay_scr.setContentsMargins(3, 0, 18, 0)
        self.scroll_area.setWidget(self.pnl_scr)
    
    def set_layout(self):
        self.pnl_trs = Top()
        self.bottom = Bottom()
        self.lay_trs = QVBoxLayout()
        self.lay_trs.setContentsMargins(0, 0, 0, 0)
        self.pnl_trs.setLayout(self.lay_trs)
    
    def set_gui(self):
        self.set_layout()
        self.set_scroll()
        self.set_title()
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self.pnl_trs).activated.connect(action)
    
    def add(self, track):
        self.lay_scr.addWidget(track.pnl_trk)
    
    def remove(self, track):
        self.lay_scr.removeWidget(track.pnl_trk)
    
    def show(self):
        self.pnl_trs.show()
    
    def close(self):
        self.pnl_trs.close()
        self.send_rating()



class Track:
    
    def __init__(self):
        self.set_gui()
    
    def dump(self):
        return (self.ent_tit.get(), self.ent_lyr.get(), self.ent_com.get()
               ,int(self.opt_rtg.get()))
    
    def configure(self):
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
        self.ent_tno.clear()
        self.ent_tit.clear()
        self.ent_lyr.clear()
        self.ent_com.clear()
        self.ent_bit.clear()
        self.ent_len.clear()
        self.opt_rtg.set(0)
    
    def set_layout(self):
        self.pnl_trk = QWidget()
        self.lay_trk = QGridLayout()
        self.pnl_trk.setLayout(self.lay_trk)
    
    def set_entries(self):
        self.ent_tno = Entry()
        self.ent_tit = Entry()
        self.ent_lyr = Entry()
        self.ent_com = Entry()
        self.ent_bit = Entry()
        self.ent_len = Entry()
    
    def set_labels(self):
        self.lbl_tno = Label(_('Track #:'))
        self.lbl_tit = Label(_('Title:'))
        self.lbl_lyr = Label(_('Lyrics:'))
        self.lbl_com = Label(_('Comment:'))
        self.lbl_bit = Label(_('Bitrate:'))
        self.lbl_len = Label(_('Length:'))
        self.lbl_rtg = Label(_('Rating:'))
    
    def set_options(self):
        self.opt_rtg = OptionMenu((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    
    def add_labels(self):
        self.lay_trk.addWidget(self.lbl_tno.widget, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_tit.widget, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_lyr.widget, 2, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_com.widget, 3, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_bit.widget, 4, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_len.widget, 5, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.lay_trk.addWidget(self.lbl_rtg.widget, 6, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
    
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
        self.configure()
