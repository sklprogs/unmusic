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
        
    def query(self):
        lg.objs.db().updateDB ('begin;select ALBUM from ALBUMS \
                                where ARTIST="%s";commit;' \
                               % ("Jean-Sebastien Royer",)
                              )
        print(lg.objs._db.dbc.fetchone())
    
    def mixed_rating(self):
        lg.objs.db().albumid = 7
        lg.objs._db.dbc.execute ('update TRACKS set RATING = ? \
                                  where ALBUMID = ? and NO <= ?'
                                 ,(7,lg.objs._db.albumid,5,)
                                )
        lg.objs._db.save()
        lg.objs._db.dbc.execute('select * from TRACKS')
        rows    = lg.objs._db.tracks()
        headers = []
        for i in range(7):
            headers.append('header' + str(i))
        sh.Table (headers = headers
                 ,rows    = rows
                 ,Shorten = 1
                 ,MaxRow  = 1000
                 ,MaxRows = 35
                 ).print()
    
    def tracks(self):
        itracks = gi.Tracks()
        itracks.reset()
        for i in range(20):
            itracks.add()
        for i in range(len(itracks._tracks)):
            itracks._tracks[i].ent_tno.insert(i+1)
            itracks._tracks[i].ent_tit.insert(_('Track #%d') % (i + 1))
        itracks.after_add()
        itracks.show()
    
    def check_nos(self):
        f = 'tests.Commands.check_nos'
        albumid = lg.objs.db().max_id()
        if albumid:
            for i in range(albumid):
                lg.objs._db.albumid = i + 1
                print(lg.objs._db.albumid,':',lg.objs.db().check_nos())
        else:
            sh.com.empty(f)
    

com = Commands()


if __name__ == '__main__':
    f = 'tests.__main__'
    sg.objs.start()
    lg.objs.db().albumid = 7
    data = lg.objs._db.get_album()
    if data:
        if data[6]:
            ipic = sg.Image()
            ipic._bytes = data[6]
            ipic.loader()
            ipic.thumbnail(200,300)
            top = sg.objs.new_top()
            lbl = sg.Label (parent = top
                           ,Close  = False
                           ,image  = ipic.image()
                           )
            top.show()
        else:
            sh.com.empty(f)
    else:
        sh.com.empty(f)
    lg.objs._db.close()
    sg.objs.end()
