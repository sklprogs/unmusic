#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.root.controller import ROOT

ROOT.get_root()


class Commands:
    
    def run_tracks(self):
        from tracks.controller import Tracks
        itracks = Tracks()
        for i in range(40):
            itracks.add()
        return itracks


com = Commands()


if __name__ == '__main__':
    '''
    import gui.tests
    import gui.tracks
    app = gui.tests.Test()
    track = gui.tracks.Track()
    app.set_gui(track.pnl_trk)
    app.show()
    '''
    window = com.run_tracks()
    window.show()
    ROOT.end()

