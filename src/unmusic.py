#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared_qt.shared as sh
from skl_shared_qt.localize import _

''' If we use module-level variables instead of 'Objects', this must be done
    as soon as we can; otherwise, we can get the following error: 'QWidget:
    Must construct a QApplication before a QWidget'. This is because creating
    a class stored in a controller will also create its GUI.
'''
sh.com.start()

from config import CONFIG
from menu.controller import MENU



f = '[unmusic] unmusic.__main__'
if CONFIG.Success:
    MENU.show()
else:
    mes = _('Invalid configuration!')
    #FIX: quit app normally after common dialog
    #sh.objs.get_mes(f, mes).show_error()
    idebug = sh.Debug(f, mes)
    idebug.show()
sh.com.end()
