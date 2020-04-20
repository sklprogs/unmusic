#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared2.shared as sh
from skl_shared2.localize import _
import logic   as lg
import gui     as gi
import unmusic as ct


if __name__ == '__main__':
    f = '[unmusic] album_editor.__main__'
    sh.com.start()
    ct.objs.get_editor().reset()
    ct.objs.editor.show()
    lg.objs.get_db().save()
    lg.objs.db.close()
    mes = _('Goodbye!')
    sh.objs.get_mes(f,mes,True).show_debug()
    sh.com.end()
