#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import logic as lg
from . import gui


class Tracks:
    
    def __init__(self):
        self.tracks = []
        self.Active = False
        self.Success = True
        self.gui = gui.Tracks()
        self.set_bindings()
    
    def decode(self):
        f = '[unmusic] tracks.controller.Tracks.decode'
        if not self.Success:
            sh.com.cancel(f)
            return
        for track in self.tracks:
            title = track.ent_tit.get()
            title = lg.com.decode_back(title)
            track.ent_tit.clear()
            track.ent_tit.insert(title)
    
    def _dump(self, old, new):
        f = '[unmusic] tracks.controller.Tracks._dump'
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
                mes = _('Edit #{}.').format(i+1)
                self.gui.update_info(mes)
                lg.objs.get_db().update_track (no = i + 1
                                              ,data = new_record
                                              )
                Dump = True
        return Dump
    
    def dump_new(self):
        new = []
        for track in self.tracks:
            new.append(track.dump())
        return new
    
    def dump(self):
        f = '[unmusic] tracks.controller.Tracks.dump'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not lg.objs.get_db().check_nos():
            mes = _('Track numbers should be sequential!')
            sh.objs.get_mes(f, mes).show_warning()
            return
        old = lg.objs.db.get_tracks()
        new = self.dump_new()
        return self._dump(old, new)
    
    def save(self):
        ''' #NOTE: this should be done before 'albumid' is changed, otherwise,
            a wrong DB record will be overwritten!
        '''
        f = '[unmusic] tracks.controller.Tracks.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.dump():
            objs.get_editor().update_rating()
            self.gui.update_info(_('Save DB.'))
            lg.objs.get_db().save()
    
    def set_bindings(self):
        self.gui.bind(('Ctrl+Q',), self.close)
        self.gui.bind(('Esc',), self.close)
    
    def add(self):
        track = gui.Track()
        self.gui.add(track)
        self.tracks.append(track)
        return track
    
    def show(self):
        self.Active = True
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.Active = False
        self.save()
        self.gui.close()
    
    def fill_search(self, data):
        f = '[unmusic] tracks.controller.Tracks.fill_search'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not data:
            sh.com.rep_empty(f)
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
            track.ent_tno.insert(record[2])
            track.ent_tit.insert(record[1])
            track.ent_lyr.insert(record[3])
            track.ent_com.insert(record[4])
            track.ent_bit.insert(str(record[5] // 1000) + 'k')
            track.ent_len.insert(sh.lg.com.get_human_time(float(record[6])))
            track.opt_rtg.set(record[7])
    
    def reload(self):
        self.fill()
        self.show()
    
    def fill(self):
        f = '[unmusic] tracks.controller.Tracks.fill'
        if not self.Success:
            sh.com.cancel(f)
            return
        data = lg.objs.get_db().get_tracks()
        if not data:
            mes = _('No tracks are associated with this album.')
            sh.objs.get_mes(f, mes).show_info()
            return
        for i in range(len(data)):
            self.add()
            record = data[i]
            track = self.tracks[i]
            if len(record) != 7:
                self.Success = False
                mes = _('Wrong input data: "{}"!').format(data)
                sh.objs.get_mes(f, mes).show_error()
                return
            track.reset()
            track.ent_tno.insert(str(record[1]))
            track.ent_tit.insert(record[0])
            track.ent_lyr.insert(record[2])
            track.ent_com.insert(record[3])
            track.ent_bit.insert(str(record[4] // 1000) + 'k')
            track.ent_len.insert(sh.lg.com.get_human_time(float(record[5])))
            track.opt_rtg.set(record[6])


TRACKS = Tracks()
