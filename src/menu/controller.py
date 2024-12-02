#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.root.controller import ROOT

''' If we use module-level variables instead of 'Objects', this must be done
    as soon as we can; otherwise, we can get the following error: 'QWidget:
    Must construct a QApplication before a QWidget'. This is because creating
    a class stored in a controller will also create its GUI.
'''
ROOT.get_root()

from config import CONFIG
from album_editor.controller import ALBUM_EDITOR
from . import gui


class Menu:
    
    def __init__(self):
        self.set_gui()
    
    def show_editor(self):
        ALBUM_EDITOR.reset()
        ALBUM_EDITOR.show()
    
    def quit(self):
        self.close()
    
    def set_gui(self):
        self.gui = gui.Menu()
        self.set_bindings()
    
    def set_bindings(self):
        self.gui.bind(('Ctrl+Q',), self.quit)
        self.gui.bind(('Esc',), self.gui.minimize)
        self.gui.btn_edt.set_action(self.show_editor)
        self.gui.btn_qit.set_action(self.quit)
    
    def show(self):
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.gui.close()


f = '[unmusic] unmusic.menu.controller.__main__'
if CONFIG.Success:
    MENU = Menu()
    MENU.show()
else:
    mes = _('Invalid configuration!')
    Message(f, mes, True).show_error()
ROOT.end()
