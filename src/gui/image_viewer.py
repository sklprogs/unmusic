#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class ImageViewer:
    
    def __init__(self):
        self.set_gui()
    
    def set_icon(self):
        # Does not accent None
        self.pnl_img.setWindowIcon(sh.gi.objs.get_icon())
    
    def set_title(self):
        self.pnl_img.setWindowTitle(_('Image Viewer'))
    
    def centralize(self):
        ''' Do this only after showing the widget; otherwise, it will have
            bogus dimensions of 640×480.
        '''
        self.pnl_img.move(sh.objs.get_root().primaryScreen().geometry().center() - self.pnl_img.rect().center())
    
    def set_image(self, path):
        image = PyQt6.QtGui.QPixmap(path)
        image = image.scaled(PyQt6.QtCore.QSize(1024, 768))
        self.lbl_img.widget.setPixmap(image)
        return image
    
    def set_layout(self):
        self.pnl_img = PyQt6.QtWidgets.QWidget()
        self.lay_img = PyQt6.QtWidgets.QHBoxLayout()
        self.lay_img.setContentsMargins(0, 0, 0, 0)
        self.pnl_img.setLayout(self.lay_img)
    
    def set_gui(self):
        self.set_layout()
        self.lbl_img = sh.Label()
        self.lay_img.addWidget(self.lbl_img.widget)
        self.set_icon()
        self.set_title()
    
    def show(self):
        self.pnl_img.show()
        self.centralize()
    
    def close(self):
        self.pnl_img.close()
