#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep

from skl_shared_qt.logic import com
from logic import DB
from search_tracks.gui import Tracks as guiTracks, Track as guiTrack
import tracks.controller


class Tracks(tracks.controller.Tracks):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tracks = []
        self.Active = False
        self.Success = True
        self.gui = guiTracks()
        self.set_bindings()
    
    def reload(self, pattern):
        self.fill(pattern)
        self.show()
    
    def _dump(self, old, new):
        f = '[unmusic] search_tracks.controller.Tracks._dump'
        if not old or not new:
            rep.empty(f)
            return
        if len(old) != len(new):
            sub = f'{len(old)} = {len(new)}'
            mes = _('Condition "{}" is not observed!').format(sub)
            Message(f, mes, True).show_error()
            return
        Dump = False
        for i in range(len(old)):
            if len(old[i]) != 7 or len(new[i]) != 4:
                self.Success = False
                mes = _('Wrong input data!')
                Message(f, mes, True).show_error()
                # We're in loop - do not use 'return'
                continue
            old_record = [old[i][0], old[i][2], old[i][3], old[i][6]]
            new_record = [new[i][0], new[i][1], new[i][2], new[i][3]]
            if old_record != new_record:
                if not new[i][0]:
                    mes = _('A track title should be indicated.')
                    Message(f, mes, True).show_warning()
                    # We're in loop - do not use 'return'
                    continue
                mes = _('Edit #{}.').format(i + 1)
                #cur
                self.update_info(mes)
                DB.update_track(no = i + 1
                               ,data = new_record)
                Dump = True
        return Dump
    
    def add(self):
        # We need to override original 'add' since 'gui' is different here
        track = guiTrack()
        self.gui.add(track)
        self.tracks.append(track)
        return track
    
    def fill(self, pattern):
        f = '[unmusic] search_tracks.controller.Tracks.fill'
        if not self.Success:
            rep.cancel(f)
            return
        data = DB.search_tracks(pattern)
        if not data:
            mes = _('No matches!')
            Message(f, mes, True).show_info()
            return
        self.clear()
        for i in range(len(data)):
            record = data[i]
            track = self.add()
            if len(record) != 8:
                self.Success = False
                mes = _('Wrong input data: "{}"!').format(data)
                Message(f, mes, True).show_error()
                return
            track.reset()
            track.ent_alb.insert(record[0])
            track.ent_tit.insert(record[1])
            track.ent_tno.insert(record[2])
            track.ent_lyr.insert(record[3])
            track.ent_com.insert(record[4])
            track.ent_bit.insert(str(record[5] // 1000) + 'k')
            track.ent_len.insert(com.get_human_time(float(record[6])))
            track.opt_rtg.set(record[7])
    
    def show(self):
        f = '[unmusic] search_tracks.controller.Tracks.show'
        if not self.Success:
            rep.cancel(f)
            return
        self.Active = True
        self.gui.show()
        self.gui.update_size()
        self.gui.centralize()
        self.go_start()
    
    def save(self):
        ''' #NOTE: this should be done before 'albumid' is changed, otherwise,
            a wrong DB record will be overwritten!
        '''
        f = '[unmusic] search_tracks.controller.Tracks.save'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Not implemented yet!')
        Message(f, mes).show_info()
    
    def close(self):
        self.Active = False
        self.save()
        self.gui.close()


SEARCH_TRACKS = Tracks()
