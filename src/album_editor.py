#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared     as sh
import sharedGUI  as sg
import logic      as lg
import gui        as gi
import controller as ct

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('unmusic','../resources/locale')


if __name__ == '__main__':
    f = 'unmusic.album_editor.__main__'
    sg.objs.start()
    ct.objs.editor().reset()
    ct.objs._editor.show()
    lg.objs.db().save()
    lg.objs._db.close()
    sh.log.append (f,_('DEBUG')
                  ,_('Goodbye!')
                  )
    sg.objs.end()
