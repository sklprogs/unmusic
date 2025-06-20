#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QScrollArea
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtCore import Qt

from skl_shared.localize import _
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.checkbox.controller import CheckBox
from skl_shared.graphics.option_menu.controller import OptionMenu
from skl_shared.graphics.button.controller import Button
from skl_shared.graphics.entry.controller import Entry
from skl_shared.graphics.label.controller import Label


class CopyAlbums:
    
    def __init__(self):
        self.set_gui()
    
    def remove(self, cbx):
        self.center.lay_scr.removeWidget(cbx.widget)
    
    def set_info(self, text):
        self.bottom.label.set_text(text)
    
    def add_row(self, rowno, string):
        cbx = CheckBox(string)
        self.center.lay_scr.addWidget(cbx.widget, rowno, 0, 1, 1)
        return cbx
    
    def go_start(self):
        slider = self.center.scroll_area.verticalScrollBar()
        slider.setValue(slider.minimum())
    
    def go_end(self):
        slider = self.center.scroll_area.verticalScrollBar()
        slider.setValue(slider.maximum())
    
    def add_widgets(self):
        self.layout.addWidget(self.top.pane)
        self.layout.addWidget(self.center.pane)
        self.layout.addWidget(self.bottom.pane)
    
    def set_widgets(self):
        self.pane = QWidget()
        self.layout = QVBoxLayout()
        self.top = Top(self.pane)
        self.center = Center(self.pane)
        self.bottom = Bottom(self.pane)
    
    def set_layout(self):
        self.pane.setLayout(self.layout)
    
    def set_gui(self):
        self.set_widgets()
        self.add_widgets()
        self.set_layout()
        self.configure()
    
    def centralize(self):
        self.pane.move(ROOT.get_root().primaryScreen().geometry().center() - self.pane.rect().center())
    
    def configure(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.pane.setMinimumSize(620, 620)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self.pane).activated.connect(action)
    
    def set_title(self, title):
        self.pane.setWindowTitle(title)
    
    def show(self):
        self.pane.show()
        self.centralize()
    
    def close(self):
        self.pane.close()



class Top:
    
    def __init__(self, parent):
        self.parent = parent
        self.set_gui()
    
    def set_layout(self):
        self.pane = QWidget(self.parent)
        self.layout = QGridLayout()
        self.pane.setLayout(self.layout)
    
    def set_gui(self):
        self.set_layout()
        self.set_widgets()
        self.add_widgets()
        self.configure()
    
    def set_widgets(self):
        items = (_('Mobile collection'), _('Local collection'), _('External collection'))
        self.opt_src = OptionMenu(items, _('External collection'), action=None)
        self.opt_dst = OptionMenu(items, _('Mobile collection'), action=None) 
        items = (_('Any'), _('Heavy'), _('Light'))
        self.opt_gnr = OptionMenu(items, _('Heavy'), action=None)
        items = (_('Random'), _('From Start'), _('From End'))
        self.opt_ftc = OptionMenu(items, action=None)
        self.ent_lmt = Entry()
        self.lbl_src = Label(_('Source:'))
        self.lbl_trg = Label(_('Target:'))
        self.lbl_gnr = Label(_('Genres:'))
        self.lbl_ftc = Label(_('Fetch:'))
        self.lbl_lmt = Label(_('Limit:'))
    
    def add_widgets(self):
        self.layout.addWidget(self.lbl_src.widget, 0, 0, 1, 1)
        self.layout.addWidget(self.lbl_trg.widget, 0, 1, 1, 1)
        self.layout.addWidget(self.lbl_gnr.widget, 0, 2, 1, 1)
        self.layout.addWidget(self.lbl_ftc.widget, 0, 3, 1, 1)
        self.layout.addWidget(self.lbl_lmt.widget, 0, 4, 1, 1)
        self.layout.addWidget(self.opt_src.widget, 1, 0, 1, 1)
        self.layout.addWidget(self.opt_dst.widget, 1, 1, 1, 1)
        self.layout.addWidget(self.opt_gnr.widget, 1, 2, 1, 1)
        self.layout.addWidget(self.opt_ftc.widget, 1, 3, 1, 1)
        self.layout.addWidget(self.ent_lmt.widget, 1, 4, 1, 1)
    
    def configure(self):
        self.layout.setContentsMargins(10, 10, 10, 0)
        self.ent_lmt.set_max_width(30)



class Bottom:
    
    def __init__(self, parent):
        self.parent = parent
        self.set_gui()
    
    def set_layout(self):
        self.pane = QWidget(self.parent)
        self.layout = QGridLayout()
        self.pane.setLayout(self.layout)
    
    def set_gui(self):
        self.set_layout()
        self.set_widgets()
        self.add_widgets()
        self.configure()
    
    def set_widgets(self):
        self.label = Label(_('Free space has not been calculated yet.'))
        self.btn_cls = Button(text=_('Close'), hint=_('Close this window'))
        self.btn_ftc = Button(text=_('Fetch'), hint=_('Fill the list'))
        self.btn_clc = Button(text=_('Calculate'), hint=_('Calculate free and required space'))
        self.btn_nxt = Button(text=_('Copy'), hint=_('Start copying albums'))
    
    def add_widgets(self):
        self.layout.addWidget(self.label.widget, 0, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.btn_cls.widget, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.btn_ftc.widget, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.btn_clc.widget, 1, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.btn_nxt.widget, 1, 3, 1, 1, Qt.AlignmentFlag.AlignRight)
    
    def configure(self):
        self.layout.setContentsMargins(10, 0, 10, 10)
        policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_cls.widget.setSizePolicy(policy)
        self.btn_ftc.widget.setSizePolicy(policy)
        self.btn_nxt.widget.setSizePolicy(policy)



class Center:
    
    def __init__(self, parent):
        self.parent = parent
        self.set_gui()
    
    def set_layout(self):
        self.pane = QWidget(self.parent)
        self.layout = QVBoxLayout()
        self.pane.setLayout(self.layout)
    
    def set_gui(self):
        self.set_layout()
        self.set_widgets()
        self.add_widgets()
        self.configure()
    
    def configure(self):
        self.scroll_area.setWidgetResizable(True)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.lay_scr.setContentsMargins(10, 10, 10, 10)
        self.pnl_scr.setFocus()
    
    def set_widgets(self):
        self.scroll_area = QScrollArea(self.pane)
        self.pnl_scr = QWidget(self.scroll_area)
        self.lay_scr = QGridLayout(self.pnl_scr)
    
    def add_widgets(self):
        self.layout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(self.pnl_scr)
