#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared_qt.shared as sh
from skl_shared_qt.localize import _

import logic as lg
import unmusic as ct


if __name__ == '__main__':
    f = '[unmusic] album_editor.__main__'
    sh.com.start()
    ct.objs.get_editor().reset()
    ct.objs.editor.show()
    lg.objs.get_db().save()
    lg.com.save_config()
    lg.objs.db.close()
    mes = _('Goodbye!')
    sh.objs.get_mes(f, mes, True).show_debug()
    sh.com.end()
