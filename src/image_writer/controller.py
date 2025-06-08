#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from image_writer.gui import Image as guiImage


class Image:
    
    def __init__(self):
        self.Success = True
        self.gui = guiImage()
    
    def load(self, data):
        f = '[unmusic] image_writer.controller.Image.load'
        if not self.Success:
            rep.cancel(f)
            return
        if not data:
            self.Success = False
            rep.empty(f)
            return
        try:
            self.Success = self.gui.load(data)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
    
    def save(self, filew):
        f = '[unmusic] image_writer.controller.Image.save'
        if not self.Success:
            rep.cancel(f)
            return
        if not filew:
            self.Success = False
            rep.empty(f)
            return
        mes = _('Export image as {}').format(filew)
        Message(f, mes).show_info()
        try:
            self.Success = self.gui.save(filew)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
