#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtGui import QShortcut, QKeySequence, QPixmap
from PyQt6.QtCore import QSize

from skl_shared.localize import _
from skl_shared.message.controller import rep
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.label.controller import Label


class ImageViewer:
    
    def __init__(self):
        self.set_gui()
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self.pnl_img).activated.connect(action)
    
    def set_title(self):
        self.pnl_img.setWindowTitle(_('Image Viewer'))
    
    def centralize(self):
        ''' Do this only after showing the widget; otherwise, it will have
            bogus dimensions of 640×480.
        '''
        self.pnl_img.move(ROOT.get_root().primaryScreen().geometry().center() - self.pnl_img.rect().center())
    
    def set_image(self, path):
        image = QPixmap(path)
        image = image.scaled(QSize(1024, 768))
        self.lbl_img.widget.setPixmap(image)
        return image
    
    def set_layout(self):
        self.pnl_img = QWidget()
        self.lay_img = QHBoxLayout()
        self.lay_img.setContentsMargins(0, 0, 0, 0)
        self.pnl_img.setLayout(self.lay_img)
    
    def set_gui(self):
        self.set_layout()
        self.lbl_img = Label()
        self.lay_img.addWidget(self.lbl_img.widget)
        self.set_title()
    
    def show(self):
        self.pnl_img.show()
        self.centralize()
    
    def close(self):
        self.pnl_img.close()
