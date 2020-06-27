#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import logic as lg
import gui as gi


class Commands:
    
    def __init__(self):
        pass
        
    def show_query(self):
        lg.objs.get_db().updateDB ('begin;select ALBUM from ALBUMS \
                                    where ARTIST="%s";commit;' \
                                   % ("Jean-Sebastien Royer",)
                                  )
        print(lg.objs.db.dbc.fetchone())
    
    def show_mixed_rating(self):
        lg.objs.get_db().albumid = 7
        lg.objs.db.dbc.execute ('update TRACKS set RATING = ? \
                                  where ALBUMID = ? and NO <= ?'
                                 ,(7,lg.objs.db.albumid,5,)
                                )
        lg.objs.db.save()
        lg.objs.db.dbc.execute('select * from TRACKS')
        rows    = lg.objs.db.get_tracks()
        headers = []
        for i in range(7):
            headers.append('header' + str(i))
        sh.lg.Table (headers = headers
                    ,rows    = rows
                    ,Shorten = 1
                    ,MaxRow  = 1000
                    ,MaxRows = 35
                    ).print()
    
    def show_tracks(self):
        itracks = gi.Tracks()
        itracks.reset()
        for i in range(20):
            itracks.add()
        for i in range(len(itracks.tracks)):
            itracks.tracks[i].ent_tno.insert(i+1)
            itracks.tracks[i].ent_tit.insert(_('Track #%d') % (i + 1))
        itracks.add_after()
        itracks.show()
    
    def check_nos(self):
        f = 'tests.Commands.check_nos'
        albumid = lg.objs.get_db().get_max_id()
        if albumid:
            for i in range(albumid):
                lg.objs.db.albumid = i + 1
                print(lg.objs.db.albumid,':',lg.objs.get_db().check_nos())
        else:
            sh.com.rep_empty(f)
    

com = Commands()


if __name__ == '__main__':
    f = 'tests.__main__'
    sh.com.start()
    print(lg.objs.get_db().get_next_rated())
    lg.objs.get_db().close()
    sh.com.end()
