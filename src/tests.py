#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import logic as lg
import gui as gi


class Album:
    
    def __init__(self):
        self.id = 0
        self.tracks = []
        self.Camel = False



class CamelCase:
    
    def __init__(self):
        self.Success = True
        self.albums = []
    
    def debug(self):
        f = '[unmusic] tests.CamelCase.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        ids = []
        camels = []
        tracks = []
        for album in self.albums:
            for track in album.tracks:
                ids.append(album.id)
                camels.append(album.Camel)
                tracks.append(track)
        headers = (_('ALBUM ID'),_('MIXED CASE'),_('TRACK'))
        iterable = [ids,camels,tracks]
        mes = sh.FastTable (headers = headers
                           ,iterable = iterable
                           ,maxrow = 100
                           ,maxrows = 1000
                           ).run()
        sh.com.run_fast_debug(f,mes)
    
    def _get_tracks(self):
        query = 'select ALBUMID,TITLE from TRACKS order by ALBUMID'
        try:
            lg.objs.get_db().dbc.execute(query)
            return lg.objs.db.dbc.fetchall()
        except Exception as e:
            self.Success = False
            mes = _('Operation has failed!\nDetails: {}').format(e)
            sh.objs.get_mes(f,mes).show_warning()
    
    def set_albums(self):
        f = '[unmusic] tests.CamelCase.set_albums'
        if not self.Success:
            sh.com.cancel(f)
            return
        result = self._get_tracks()
        if not result:
            self.Success = False
            sh.com.rep_empty(f)
            return
        old_id = 0
        tracks = []
        album = Album()
        for row in result:
            id_, track = row[0], row[1]
            if id_ == old_id:
                album.tracks.append(track)
            else:
                if album.id > 0:
                    self.albums.append(album)
                album = Album()
                old_id = album.id = id_
                album.tracks.append(track)
        self.albums.append(album)
    
    def _is_word_camel(self,word):
        ''' - There can be false-positive results if each track has
              a translation (e.g., looks like "a title in a foreign
              language (a translated title)"). Moreover, '_' or '-' are
              not considered as punctuation. To be on a safe side, we
              remove all non-alphabetic symbols here - this actually
              should not be slower than adding extra punctuation and
              then removing it together with digits.
            - NOTE: Do this when processing words, not tracks, since
              spaces will be deleted otherwise!
        '''
        word = [char for char in word if char.isalpha()]
        word = ''.join(word)
        if word == word.upper():
            return
        ''' The word may be shortened by the first symbol only here
            since we are sure now that only letters have left.
        '''
        for char in word[1:]:
            # This already checks if a letter is provided
            if char.isupper():
                return True
    
    def _is_track_camel(self,track):
        track = track.replace('_',' ')
        track = track.replace('-',' ')
        for word in track.split(' '):
            if self._is_word_camel(word):
                return True
    
    def _is_album_camel(self,tracks):
        for track in tracks:
            if not self._is_track_camel(track):
                return
        return True
    
    def set_camel(self):
        f = '[unmusic] tests.CamelCase.set_camel'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.albums:
            self.Success = False
            sh.com.rep_empty(f)
            return
        for album in self.albums:
            album.Camel = self._is_album_camel(album.tracks)
    
    def report(self):
        f = '[unmusic] tests.CamelCase.report'
        if not self.Success:
            sh.com.cancel(f)
            return
        ids = [str(album.id) for album in self.albums if album.Camel]
        if not ids:
            sh.com.rep_lazy(f)
            return
        mes = []
        sub = _('Tracks of the following albums are of a mixed case:')
        mes.append(sub)
        mes.append('')
        mes.append(', '.join(ids))
        sh.com.run_fast_debug(f,'\n'.join(mes))
    
    def run(self):
        self.set_albums()
        self.set_camel()
        lg.objs.get_db().close()
        #self.debug()
        self.report()



class Commands:
    
    def __init__(self):
        pass
    
    def show_query(self):
        f = '[unmusic] tests.Commands.show_query'
        query = 'begin;select ALBUM from ALBUMS where ARTIST="{}" \
                ;commit;'.format('Jean-Sebastien Royer')
        lg.objs.get_db().updateDB(query)
        result = lg.objs.db.dbc.fetchone()
        if result:
            mes = result[0]
        else:
            mes = _('Not found!')
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def show_mixed_rating(self):
        lg.objs.get_db().albumid = 7
        query = 'update TRACKS set RATING = ? where ALBUMID = ? \
                 and NO <= ?'
        lg.objs.db.dbc.execute(query,(7,lg.objs.db.albumid,5,))
        lg.objs.db.save()
        lg.objs.db.dbc.execute('select * from TRACKS')
        rows = lg.objs.db.get_tracks()
        headers = []
        for i in range(7):
            headers.append('header' + str(i))
        sh.lg.Table (headers = headers
                    ,rows = rows
                    ,Shorten = 1
                    ,MaxRow = 1000
                    ,MaxRows = 35
                    ).print()
    
    def show_tracks(self):
        itracks = gi.objs.get_tracks()
        itracks.reset()
        for i in range(20):
            itracks.add()
        for i in range(len(itracks.tracks)):
            itracks.tracks[i].ent_tno.insert(i+1)
            itracks.tracks[i].ent_tit.insert(_('Track #{}').format(i+1))
        itracks.adjust_by_content()
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
    #lg.objs.get_db().close()
    CamelCase().run()
    sh.com.end()
