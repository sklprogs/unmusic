#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtGui import QImage
from PyQt5.QtCore import QByteArray


class Image:
    
    def __init__(self):
        self.image = QImage()
    
    def load(self, data):
        return self.image.loadFromData(QByteArray(data))
    
    def save(self, filew):
        return self.image.save(filew, 'JPG')
