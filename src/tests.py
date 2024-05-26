#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import unmusic as un


class Commands:
    
    def run_tracks(self):
        itracks = un.Tracks()
        for i in range(40):
            itracks.add()
        return itracks


com = Commands()


if __name__ == '__main__':
    sh.com.start()
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
    sh.com.end()

