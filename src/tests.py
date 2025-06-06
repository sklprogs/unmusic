#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.root.controller import ROOT

ROOT.get_root()

from config import PATHS
from db import DB


class Commands:
    
    def run_tracks(self):
        from tracks.controller import Tracks
        itracks = Tracks()
        for i in range(40):
            itracks.add()
        return itracks
    
    def get_many_bad_albums(self):
        f = '[unmusic] tests.Commands.get_many_bad_albums'
        idb = TestDB(PATHS.get_db())
        Message(f, idb.get_many_bad_albums()).show_debug()
        idb.close()
        



class TestDB(DB):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.albumid = 10806
    
    def get_many_bad_albums(self, rating=5, limit=5):
        f = '[unmusic] tests.TestDB.get_many_bad_albums'
        if not self.Success:
            rep.cancel(f)
            return
        query = 'select distinct ALBUMID from TRACKS where RATING > 0 and RATING < ? order by ALBUMID desc'
        # limit=0 provides an empty output
        if limit:
            query += ' limit ?'
        try:
            if limit:
                self.dbc.execute(query, (rating, limit,))
            else:
                self.dbc.execute(query, (rating,))
            result = self.dbc.fetchall()
            if result:
                return [item[0] for item in result]
        except Exception as e:
            self.fail(f, e)


com = Commands()


if __name__ == '__main__':
    f = '[unmusic] tests.__main__'
    '''
    import gui.tests
    import gui.tracks
    app = gui.tests.Test()
    track = gui.tracks.Track()
    app.set_gui(track.pnl_trk)
    app.show()
    '''
    #window = com.run_tracks()
    #window.show()
    com.get_many_bad_albums()
    mes = _('Goodbye!')
    Message(f, mes).show_debug()
    ROOT.end()

