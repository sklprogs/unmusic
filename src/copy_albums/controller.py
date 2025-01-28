#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.graphics.root.controller import ROOT

from copy_albums.gui import CopyAlbums as guiCopyAlbums


class CopyAlbums:
    
    def __init__(self):
        self.gui = guiCopyAlbums()
        self.set_bindings()
        self.set_title()
    
    def set_title(self, title=_('Copy albums')):
        self.gui.set_title(title)
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()
    
    def set_bindings(self):
        self.gui.bind(('Esc', 'Ctrl+Q'), self.close)
        self.gui.bind(('Ctrl+Home', 'Home'), self.gui.go_start)
        self.gui.bind(('Ctrl+End', 'End'), self.gui.go_end)
        self.gui.bottom.btn_cls.set_action(self.close)


COPY_ALBUMS = CopyAlbums()
