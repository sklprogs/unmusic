#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QShortcut, QKeySequence

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.root.controller import ROOT
from skl_shared_qt.graphics.icon.controller import ICON
from skl_shared_qt.graphics.button.controller import Button
from skl_shared_qt.paths import PDIR

ICON.set(PDIR.add('..', 'resources', 'unmusic.png'))


class Menu:
    
    def __init__(self, *args, **kwargs):
        self.set_gui()
    
    def minimize(self):
        self.app.showMinimized()
    
    def centralize(self):
        ''' Do this only after showing the widget; otherwise, it will have
            bogus dimensions of 640×480.
        '''
        self.app.move(ROOT.get_root().primaryScreen().geometry().center() - self.app.rect().center())
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self.window).activated.connect(action)
    
    def set_buttons(self):
        self.btn_edt = Button(_('Album Editor'))
        self.btn_prp = Button(text = _('Prepare files')
                             ,hint = _('Move sub-folders to a root folder, split large lossless files, etc.'))
        self.btn_col = Button(_('Collect tags & Obfuscate'))
        self.btn_cop = Button(_('Copy music'))
        self.btn_del = Button(_('Delete low-rated music'))
        self.btn_dup = Button(_('Delete duplicates from local collection'))
        self.btn_qit = Button(_('Quit'))
    
    def add_buttons(self):
        self.layout.addWidget(self.btn_edt.widget)
        self.layout.addWidget(self.btn_prp.widget)
        self.layout.addWidget(self.btn_col.widget)
        self.layout.addWidget(self.btn_cop.widget)
        self.layout.addWidget(self.btn_del.widget)
        self.layout.addWidget(self.btn_dup.widget)
        self.layout.addWidget(self.btn_qit.widget)
    
    def set_layout(self):
        self.app = QMainWindow()
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.window.setLayout(self.layout)
        self.app.setCentralWidget(self.window)
    
    def set_icon(self):
        # Does not accept None
        self.app.setWindowIcon(ICON.get())
    
    def set_title(self, title='unmusic'):
        self.app.setWindowTitle(title)
    
    def configure(self):
        self.btn_edt.set_default()
        self.btn_edt.change_font_size(2)
        self.btn_prp.change_font_size(2)
        self.btn_col.change_font_size(2)
        self.btn_cop.change_font_size(2)
        self.btn_del.change_font_size(2)
        self.btn_dup.change_font_size(2)
        self.btn_qit.change_font_size(2)
    
    def set_gui(self):
        self.set_layout()
        self.set_buttons()
        self.add_buttons()
        self.set_icon()
        self.set_title()
        self.configure()
    
    def show(self):
        self.app.show()
    
    def close(self):
        self.app.close()
