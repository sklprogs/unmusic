#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message
from skl_shared_qt.graphics.root.controller import ROOT

''' If we use module-level variables instead of 'Objects', this must be done
    as soon as we can; otherwise, we can get the following error: 'QWidget:
    Must construct a QApplication before a QWidget'. This is because creating
    a class stored in a controller will also create its GUI.
'''
ROOT.get_root()

from config import CONFIG
from menu.controller import MENU



f = '[unmusic] unmusic.__main__'
if CONFIG.Success:
    MENU.show()
else:
    mes = _('Invalid configuration!')
    Message(f, mes, True).show_error()
ROOT.end()
