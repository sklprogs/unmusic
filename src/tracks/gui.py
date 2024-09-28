#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6
import PyQt6.QtWidgets
import PyQt6.QtGui

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


sh.gi.ICON = sh.objs.get_pdir().add('..', 'resources', 'unmusic.png')


class Bottom:
    
    def __init__(self):
        self.set_values()
        self.set_gui()
    
    def set_values(self):
        self.icn_rld = sh.objs.get_pdir().add ('..', 'resources', 'buttons'
                                              ,'reload.png'
                                              )
        self.icn_zer = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'zero_rating.png'
                                        )
        self.icn_dec = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'decode.png'
                                        )
        self.icn_sav = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'save.png'
                                        )

    def set_layout(self):
        self.pnl_btm = PyQt6.QtWidgets.QWidget()
        self.lay_btm = PyQt6.QtWidgets.QGridLayout(self.pnl_btm)
        self.lay_btm.setContentsMargins(0, 0, 0, 0)
        self.pnl_btm.setLayout(self.lay_btm)
    
    def set_gui(self):
        self.set_layout()
        self.set_widgets()
        self.add_widgets()
        self.configure()
    
    def configure(self):
        policy = PyQt6.QtWidgets.QSizePolicy (PyQt6.QtWidgets.QSizePolicy.Policy.Fixed
                                             ,PyQt6.QtWidgets.QSizePolicy.Policy.Fixed
                                             )
        self.btn_rld.widget.setSizePolicy(policy)
        self.btn_zer.widget.setSizePolicy(policy)
        self.btn_dec.widget.setSizePolicy(policy)
        self.btn_sav.widget.setSizePolicy(policy)
    
    def set_widgets(self):
        self.btn_rld = sh.Button (hint = _('Reload the present record')
                                 ,inactive = self.icn_rld
                                 ,active = self.icn_rld
                                 )
        self.btn_zer = sh.Button (hint = _('Zero rating for all tracks')
                                 ,inactive = self.icn_zer
                                 ,active = self.icn_zer
                                 )
        self.btn_dec = sh.Button (hint = _('Decode back to cp1251')
                                 ,inactive = self.icn_dec
                                 ,active = self.icn_dec
                                 )
        self.btn_sav = sh.Button (hint = _('Save changes')
                                 ,inactive = self.icn_sav
                                 ,active = self.icn_sav
                                 )
        self.pnl_btm.setLayout(self.lay_btm)
    
    def add_widgets(self):
        self.lay_btm.addWidget(self.btn_rld.widget, 0, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.lay_btm.addWidget(self.btn_zer.widget, 0, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.lay_btm.addWidget(self.btn_dec.widget, 0, 2, 1, 6, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.lay_btm.addWidget(self.btn_sav.widget, 0, 7, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignRight)



class Signal(PyQt6.QtCore.QObject):
    # Separate from Tracks; otherwise, the following error is thrown:
    # TypeError: Tracks cannot be converted to PyQt6.QtCore.QObject
    sig_rating = PyQt6.QtCore.pyqtSignal()
    sig_info = PyQt6.QtCore.pyqtSignal(str)



class Top(PyQt6.QtWidgets.QWidget):
    
    sig_close = PyQt6.QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)



class Tracks:
    
    def __init__(self):
        self.set_gui()
        self.signal = Signal()
    
    def send_rating(self):
        self.signal.sig_rating.emit()
    
    def send_info(self, mes):
        self.signal.sig_info.emit(mes)
    
    def centralize(self):
        ''' Do this only after showing the widget; otherwise, it will have
            bogus dimensions of 640×480.
        '''
        self.pnl_trs.move(sh.objs.get_root().primaryScreen().geometry().center() - self.pnl_trs.rect().center())
    
    def set_icon(self):
        # Does not accept None
        self.pnl_trs.setWindowIcon(sh.gi.objs.get_icon())
    
    def set_title(self):
        self.pnl_trs.setWindowTitle(_('Tracks'))
    
    def go_start(self):
        slider = self.scroll_area.verticalScrollBar()
        slider.setValue(slider.minimum())
    
    def go_end(self):
        slider = self.scroll_area.verticalScrollBar()
        slider.setValue(slider.maximum())
    
    def set_scroll(self):
        self.scroll_area = PyQt6.QtWidgets.QScrollArea(self.pnl_trs)
        self.scroll_area.setWidgetResizable(True)
        self.lay_trs.addWidget(self.scroll_area)
        self.lay_trs.addWidget(self.bottom.pnl_btm)
        self.pnl_scr = PyQt6.QtWidgets.QWidget(self.scroll_area)
        self.lay_scr = PyQt6.QtWidgets.QVBoxLayout(self.pnl_scr)
        self.scroll_area.setWidget(self.pnl_scr)
    
    def set_layout(self):
        self.pnl_trs = Top()
        self.bottom = Bottom()
        self.lay_trs = PyQt6.QtWidgets.QVBoxLayout()
        self.pnl_trs.setLayout(self.lay_trs)
    
    def set_gui(self):
        self.set_layout()
        self.set_scroll()
        self.set_icon()
        self.set_title()
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self.pnl_trs).activated.connect(action)
    
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
               ,int(self.opt_rtg.get())
               )
    
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
        self.configure()
