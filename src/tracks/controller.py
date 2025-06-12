#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.logic import com

from logic import DB
from tracks.gui import Tracks as guiTracks, Track as guiTrack


class Tracks:
    
    def __init__(self):
        self.tracks = []
        self.Active = False
        self.Success = True
        self.gui = guiTracks()
        self.set_bindings()
    
    def go_start(self):
        f = '[unmusic] tracks.controller.Tracks.go_start'
        if not self.Success:
            rep.cancel(f)
            return
        self.gui.go_start()
    
    def go_end(self):
        f = '[unmusic] tracks.controller.Tracks.go_end'
        if not self.Success:
            rep.cancel(f)
            return
        self.gui.go_end()
    
    def zero_rating(self):
        f = '[unmusic] tracks.controller.Tracks.zero_rating'
        if not self.Success:
            rep.cancel(f)
            return
        for track in self.tracks:
            track.opt_rtg.set(0)
    
    def decode(self):
        f = '[unmusic] tracks.controller.Tracks.decode'
        if not self.Success:
            rep.cancel(f)
            return
        for track in self.tracks:
            title = track.ent_tit.get()
            title = com.decode_back(title)
            track.ent_tit.clear()
            track.ent_tit.insert(title)
    
    def _dump(self, old, new):
        f = '[unmusic] tracks.controller.Tracks._dump'
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
            if old_record == new_record:
                continue
            if not new[i][0]:
                mes = _('A track title should be indicated.')
                Message(f, mes, True).show_warning()
                # We're in loop - do not use 'return'
                continue
            mes = _('Edit track #{}.').format(i+1)
            self.gui.send_info(mes)
            DB.update_track(i + 1, new_record)
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
            rep.cancel(f)
            return
        if not DB.check_nos():
            mes = _('Track numbers should be sequential!')
            Message(f, mes, True).show_warning()
            return
        old = DB.get_tracks()
        new = self.dump_new()
        return self._dump(old, new)
    
    def save(self):
        ''' #NOTE: this should be done before 'albumid' is changed, otherwise,
            a wrong DB record will be overwritten!
        '''
        f = '[unmusic] tracks.controller.Tracks.save'
        if not self.Success:
            rep.cancel(f)
            return
        if self.dump():
            self.gui.send_info(_('Save DB.'))
            DB.save()
    
    def set_bindings(self):
        self.gui.bind(('Ctrl+Q', 'Esc',), self.close)
        self.gui.bind(('Ctrl+Home',), self.go_start)
        self.gui.bind(('Ctrl+End',), self.go_end)
        self.gui.bottom.btn_zer.set_action(self.zero_rating)
        self.gui.pnl_trs.sig_close.connect(self.close)
    
    def add(self):
        track = guiTrack()
        self.gui.add(track)
        self.tracks.append(track)
        return track
    
    def show(self):
        f = '[unmusic] tracks.controller.Tracks.show'
        if not self.Success:
            rep.cancel(f)
            return
        self.Active = True
        self.clear()
        self.fill()
        self.gui.show()
        self.gui.update_size()
        self.gui.centralize()
        self.go_start()
    
    def close(self):
        self.Active = False
        self.save()
        self.gui.close()
    
    def clear(self):
        for track in self.tracks:
            self.gui.remove(track)
    
    def fill(self):
        f = '[unmusic] tracks.controller.Tracks.fill'
        if not self.Success:
            rep.cancel(f)
            return
        data = DB.get_tracks()
        if not data:
            self.Success = False
            mes = _('Album {} has no tracks!').format(DB.albumid)
            Message(f, mes, True).show_warning()
            return
        self.tracks = []
        for i in range(len(data)):
            self.add()
            record = data[i]
            track = self.tracks[i]
            if len(record) != 7:
                self.Success = False
                mes = _('Wrong input data: "{}"!').format(data)
                Message(f, mes, True).show_error()
                return
            track.reset()
            track.ent_tno.insert(str(record[1]))
            track.ent_tit.insert(record[0])
            track.ent_lyr.insert(record[2])
            track.ent_com.insert(record[3])
            track.ent_bit.insert(str(record[4] // 1000) + 'k')
            track.ent_len.insert(com.get_human_time(float(record[5])))
            track.opt_rtg.set(record[6])


TRACKS = Tracks()
