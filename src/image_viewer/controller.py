#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from config import CONFIG
import logic as lg
from . import gui
from .logic import IMAGE


class ImageViewer:
    
    def __init__(self):
        self.gui = gui.ImageViewer()
        self.set_bindings()
    
    def set_bindings(self):
        self.gui.bind(('Esc',), self.close)
        self.gui.lbl_img.set_action(self.close)
    
    def set_image(self):
        f = '[unmusic] image_viewer.controller.ImageViewer.set_image'
        path = IMAGE.run()
        if not path:
            sh.com.rep_empty(f)
            return
        try:
            self.image = self.gui.set_image(path)
        except Exception as e:
            ''' Do not fail 'Success' here - it can be just an incorrectly
                ripped image.
            '''
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes).show_warning()
    
    def show(self):
        self.gui.show()
    
    def close(self, event=None):
        self.gui.close()


IMAGE_VIEWER = ImageViewer()
