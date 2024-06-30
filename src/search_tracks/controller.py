#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import logic as lg
from . import gui
import tracks.controller


class Tracks(tracks.controller.Tracks):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tracks = []
        self.Active = False
        self.Success = True
        self.gui = gui.Tracks()
        self.set_bindings()
    
    def reload(self, pattern):
        self.fill(pattern)
        self.show()
    
    def _dump(self, old, new):
        f = '[unmusic] search_tracks.controller.Tracks._dump'
        if not old or not new:
            sh.com.rep_empty(f)
            return
        if len(old) != len(new):
            sub = f'{len(old)} = {len(new)}'
            mes = _('Condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f, mes).show_error()
            return
        Dump = False
        for i in range(len(old)):
            if len(old[i]) != 7 or len(new[i]) != 4:
                self.Success = False
                mes = _('Wrong input data!')
                sh.objs.get_mes(f, mes).show_error()
                # We're in loop - do not use 'return'
                continue
            old_record = [old[i][0], old[i][2], old[i][3], old[i][6]]
            new_record = [new[i][0], new[i][1], new[i][2], new[i][3]]
            if old_record != new_record:
                if not new[i][0]:
                    mes = _('A track title should be indicated.')
                    sh.objs.get_mes(f, mes).show_warning()
                    # We're in loop - do not use 'return'
                    continue
                mes = _('Edit #{}.').format(i + 1)
                #cur
                self.update_info(mes)
                lg.DB.update_track (no = i + 1
                                   ,data = new_record
                                   )
                Dump = True
        return Dump
    
    def add(self):
        # We need to override original 'add' since 'gui' is different here
        track = gui.Track()
        self.gui.add(track)
        self.tracks.append(track)
        return track
    
    def fill(self, pattern):
        f = '[unmusic] search_tracks.controller.Tracks.fill'
        if not self.Success:
            sh.com.cancel(f)
            return
        data = lg.DB.search_tracks(pattern)
        if not data:
            mes = _('No matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        for i in range(len(data)):
            record = data[i]
            track = self.add()
            if len(record) != 8:
                self.Success = False
                mes = _('Wrong input data: "{}"!').format(data)
                sh.objs.get_mes(f, mes).show_error()
                return
            track.reset()
            track.ent_alb.insert(record[0])
            track.ent_tit.insert(record[1])
            track.ent_tno.insert(record[2])
            track.ent_lyr.insert(record[3])
            track.ent_com.insert(record[4])
            track.ent_bit.insert(str(record[5] // 1000) + 'k')
            track.ent_len.insert(sh.lg.com.get_human_time(float(record[6])))
            track.opt_rtg.set(record[7])


SEARCH_TRACKS = Tracks()
