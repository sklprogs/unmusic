#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import gui.albums as gi


class AlbumEditor:
    
    def __init__(self):
        self.gui = gi.AlbumEditor()
        self.set_bindings()
    
    def set_bindings(self):
        self.gui.bind(('Ctrl+Q',), self.close)
        self.gui.bind(('Esc',), self.close)
        #self.gui.bind(('Esc',), self.minimize)
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    editor = AlbumEditor()
    editor.show()
    sh.com.end()
