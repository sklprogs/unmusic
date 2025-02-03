#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import rep
from skl_shared_qt.logic import com
from skl_shared_qt.paths import Directory, Path

from config import PATHS
from logic import DB
from copy_albums.gui import CopyAlbums as guiCopyAlbums


ALBUMS = {}


class CopyAlbums:
    
    def __init__(self):
        self.set_values()
        self.set_gui()
    
    def set_values(self):
        self.cbx = []
        self.rowno = 0
        self.limit = 30
    
    def go_start(self):
        self.gui.go_start()
    
    def go_end(self):
        self.gui.go_end()
    
    def clear(self):
        for cbx in self.cbx:
            self.gui.remove(cbx)
        self.cbx = []
    
    def set_info(self, text):
        self.gui.set_info(text)
    
    def add_row(self, text):
        f = '[unmusic] copy_albums.controller.CopyAlbums.add_row'
        if not text:
            rep.empty(f)
            return
        self.cbx.append(self.gui.add_row(self.rowno, text))
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
        self.reset_last_fetch()
    
    def refresh(self):
        self.clear()
        self.reset()
        self.fetch()
        self.fill()
        self.go_start()
    
    def _is_title_taken(self, title):
        return str(self._get_id(title)).isdigit()
    
    def reset_last_fetch(self):
        for id_ in ALBUMS:
            ALBUMS[id_]['LastFetch'] = False
    
    def fetch(self):
        f = '[unmusic] copy_albums.controller.CopyAlbums.fetch'
        data = DB.get_albums(self.limit)
        if not data:
            rep.empty(f)
            return
        for row in data:
            id_, album, artist, year = row[0], row[1], row[2], row[3]
            if id_ in ALBUMS:
                ALBUMS[id_]['LastFetch'] = True
                continue
            info = [id_, artist, year, album]
            info = [str(item).strip() for item in info]
            info = [item for item in info if not item in ('None', '', '0', '?')]
            info = ' - '.join(info)
            if not info:
                info = '?'
            if self._is_title_taken(info):
                info += '_'
            ALBUMS[id_] = {'title': info, 'size': 0, 'Selected': False, 'LastFetch': True}
    
    def fill(self):
        for id_ in ALBUMS:
            if ALBUMS[id_]['LastFetch']:
                self.add_row(ALBUMS[id_]['title'])
    
    def set_title(self, title=_('Copy albums')):
        self.gui.set_title(title)
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()
    
    def get_source_id(self, id_):
        source = self.gui.top.opt_src.get()
        source = source.lower()
        if source == _('local collection'):
            return PATHS.get_local_album(id_)
        elif source == _('external collection'):
            return PATHS.get_external_album(id_)
        elif source == _('mobile collection'):
            return PATHS.get_mobile_album(id_)
    
    def get_target(self):
        target = self.gui.top.opt_dst.get()
        target = target.lower()
        if target == _('local collection'):
            return PATHS.get_local_collection()
        elif target == _('external collection'):
            return PATHS.get_external_collection()
        elif target == _('mobile collection'):
            return PATHS.get_mobile_collection()
    
    def get_free_space(self):
        f = '[unmusic] copy_albums.controller.CopyAlbums.get_free_space'
        target = self.get_target()
        if not target:
            rep.empty(f)
            return 0
        return Path(target).get_free_space()
    
    def set_size(self, id_):
        f = '[unmusic] copy_albums.controller.CopyAlbums.set_size'
        if ALBUMS[id_]['size']:
            return
        source = self.get_source_id(id_)
        if not source:
            rep.empty(f)
            return
        ALBUMS[id_]['size'] = Directory(source).get_size()
    
    def calculate(self):
        self.set_selection()
        count = 0
        total = 0
        for id_ in ALBUMS:
            if not ALBUMS[id_]['Selected'] or not ALBUMS[id_]['LastFetch']:
                continue
            count += 1
            self.set_size(id_)
            total += ALBUMS[id_]['size']
        free = self.get_free_space()
        totalh = com.get_human_size(total, True)
        freeh = com.get_human_size(free, True)
        mes = _('Albums: {}. Total size: {}. Free space: {} ({}).')
        if free > total:
            cond = _('sufficient')
        else:
            cond = _('NOT sufficient')
        mes = mes.format(count, totalh, freeh, cond)
        self.set_info(mes)
    
    def _get_id(self, title):
        for id_ in ALBUMS:
            if ALBUMS[id_]['title'] == title:
                return id_
    
    def set_selection(self):
        f = '[unmusic] copy_albums.controller.CopyAlbums.set_selection'
        for cbx in self.cbx:
            id_ = self._get_id(cbx.text)
            ALBUMS[id_]['Selected'] = cbx.get()
    
    def set_bindings(self):
        self.gui.bind(('Esc', 'Ctrl+Q'), self.close)
        self.gui.bind(('Ctrl+Home', 'Home'), self.go_start)
        self.gui.bind(('Ctrl+End', 'End'), self.go_end)
        self.gui.bottom.btn_cls.set_action(self.close)
        self.gui.bottom.btn_ftc.set_action(self.refresh)
        self.gui.bottom.btn_clc.set_action(self.calculate)


COPY_ALBUMS = CopyAlbums()
