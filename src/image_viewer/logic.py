#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import logic as lg


class Image:
    
    def __init__(self):
        self.dir = sh.Home('unmusic').add_share(_('Images'))
        self.Success = sh.Path(self.dir).create()
        self.path = ''
    
    def get(self):
        f = '[unmusic] image_viewer.logic.Image.get'
        if not self.Success:
            sh.com.cancel(f)
            return self.path
        path = self.get_cover()
        if path and os.path.exists(path):
            self.path = path
        else:
            self.path = sh.objs.get_pdir().add('..', 'resources', 'cd.png')
        return self.path
    
    def get_cover(self):
        f = '[unmusic] image_viewer.logic.Image.get_cover'
        if not self.Success:
            sh.com.cancel(f)
            return
        name = str(lg.DB.albumid) + '.jpg'
        return os.path.join(self.dir, name)
    
    def run(self):
        return self.get()


IMAGE = Image()
