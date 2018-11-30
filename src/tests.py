#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg
import logic     as lg
import gui       as gi

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install(lg.PRODUCT,'../resources/locale')


class Commands:
    
    def __init__(self):
        pass
    

com = Commands()

if __name__ == '__main__':
    lg.objs.db().albumid = 6
    print(lg.objs._db.prev_album('razbar'))
