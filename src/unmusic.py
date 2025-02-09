#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys

from skl_shared_qt.localize import _
from skl_shared_qt.graphics.root.controller import ROOT

''' If we use module-level variables instead of 'Objects', this must be done
    as soon as we can; otherwise, we can get the following error: 'QWidget:
    Must construct a QApplication before a QWidget'. This is because creating
    a class stored in a controller will also create its GUI.
'''
ROOT.get_root()

from skl_shared_qt.message.controller import Message


f = '[unmusic] unmusic.__main__'
mes = _('Start with arguments: {}').format(' '.join(sys.argv))
Message(f, mes).show_debug()

from config import CONFIG

if CONFIG.Success:
    if len(sys.argv) > 1 and sys.argv[1] == '--albums':
        from album_editor.controller import ALBUM_EDITOR
        ALBUM_EDITOR.reset()
        ALBUM_EDITOR.show()
    else:
        from menu.controller import MENU
        MENU.show()
else:
    mes = _('Invalid configuration!')
    Message(f, mes, True).show_error()
ROOT.end()
