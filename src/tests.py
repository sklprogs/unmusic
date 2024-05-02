#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Commands:
    
    def run_tracks(self):
        import gui.tracks as gi


if __name__ == '__main__':
    sh.com.start()
    import gui.tests
    import gui.tracks
    app = gui.tests.Test()
    track = gui.tracks.Track()
    app.set_gui(track.pnl_trk)
    app.show()
    sh.com.end()

