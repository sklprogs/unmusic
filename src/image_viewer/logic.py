#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

from skl_shared.localize import _
from skl_shared.message.controller import rep
from skl_shared.paths import PDIR, Path

from config import PATHS
from logic import DB


class Image:
    
    def __init__(self):
        self.dir = PATHS.get_images()
        self.Success = Path(self.dir).create()
        self.path = ''
    
    def get(self):
        f = '[unmusic] image_viewer.logic.Image.get'
        if not self.Success:
            rep.cancel(f)
            return self.path
        path = PATHS.get_cover(str(DB.albumid))
        if path and os.path.exists(path):
            self.path = path
        else:
            self.path = PDIR.add('..', 'resources', 'cd.png')
        return self.path
    
    def run(self):
        return self.get()


IMAGE = Image()
