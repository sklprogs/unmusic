#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import rep
from skl_shared_qt.graphics.root.controller import ROOT

from logic import DB
from copy_albums.gui import CopyAlbums as guiCopyAlbums


class CopyAlbums:
    
    def __init__(self):
        self.set_values()
        self.set_gui()
    
    def set_values(self):
        self.rowno = 0
        self.albums = []
        self.limit = 30
    
    def add_row(self, album):
        f = '[unmusic] copy_albums.controller.CopyAlbums.add_row'
        if not album:
            rep.empty(f)
            return
        self.gui.add_row(self.rowno, album)
        self.rowno += 1
    
    def set_gui(self):
        self.gui = guiCopyAlbums()
        self.set_bindings()
        self.set_title()
        self.gui.top.ent_lmt.set_text(self.limit)
    
    def set_limit(self):
        f = '[unmusic] copy_albums.controller.CopyAlbums.set_limit'
        limit = self.gui.top.ent_lmt.get()
        if not limit.isdigit():
            rep.wrong_input(f, limit)
            return
        self.limit = limit
    
    def reset(self):
        self.set_values()
        self.set_limit()
    
    def refresh(self):
        self.reset()
        self.fetch()
        self.fill()
    
    def fetch(self):
        f = '[unmusic] copy_albums.controller.CopyAlbums.fetch'
        #ALBUMID, ALBUM, ARTIST, YEAR
        data = DB.get_albums(self.limit)
        if not data:
            rep.empty(f)
            return
        for row in data:
            #info = [row[2], row[3], row[1]]
            info = [row[0], row[2], row[3], row[1]]
            info = [str(item).strip() for item in info]
            info = [item for item in info if not item in ('None', '', '0', '?')]
            info = ' - '.join(info)
            if not info:
                info = '?'
            self.albums.append(info)
        self.albums = [album for album in self.albums if album]
    
    def fill(self):
        for album in self.albums:
            self.add_row(album)
    
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
        self.gui.bottom.btn_ftc.set_action(self.refresh)


COPY_ALBUMS = CopyAlbums()
