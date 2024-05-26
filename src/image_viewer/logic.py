#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from config import PATHS
import logic as lg


class Image:
    
    def __init__(self):
        self.dir = PATHS.get_images()
        self.Success = sh.Path(self.dir).create()
        self.path = ''
    
    def get(self):
        f = '[unmusic] image_viewer.logic.Image.get'
        if not self.Success:
            sh.com.cancel(f)
            return self.path
        path = PATHS.get_cover(str(lg.DB.albumid))
        if path and os.path.exists(path):
            self.path = path
        else:
            self.path = sh.objs.get_pdir().add('..', 'resources', 'cd.png')
        return self.path
    
    def run(self):
        return self.get()


IMAGE = Image()
