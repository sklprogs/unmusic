#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
import logic      as lg
import gui        as gi
import unmusic    as ct

import gettext
import skl_shared.gettext_windows
skl_shared.gettext_windows.setup_env()
gettext.install('unmusic','../resources/locale')


if __name__ == '__main__':
    f = '[unmusic] album_editor.__main__'
    sh.com.start()
    ct.objs.editor().reset()
    ct.objs._editor.show()
    lg.objs.db().save()
    lg.objs._db.close()
    mes = _('Goodbye!')
    sh.objs.mes(f,mes,True).debug()
    sh.com.end()
