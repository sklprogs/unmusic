#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import logic as lg
import gui as gi


class MediocreAlbums:
    
    def __init__(self):
        self.Success = lg.objs.get_db().Success
        self.albums = ()
        self.good_tracks = []
        self.good_artists = []
        self.report = []
        self.purge = []
    
    def set_good_tracks(self):
        f = '[unmusic] tests.MediocreAlbums.set_good_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            query = 'select ALBUMID from TRACKS where RATING > 7 \
                     order by ALBUMID'
            lg.objs.get_db().dbc.execute(query)
            result = lg.objs.db.dbc.fetchall()
            if result:
                self.good_tracks = sorted(set([item[0] for item in result]))
        except Exception as e:
            self.fail(f,e)
    
    def fail(self,func,error):
        self.Success = False
        mes = _('Operation has failed!\nDetails: {}').format(error)
        sh.objs.get_mes(func,mes).show_warning()
    
    def set_good_artists(self):
        f = '[unmusic] tests.MediocreAlbums.set_good_artists'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'select ARTIST from ALBUMS where RATING > 7'
        try:
            lg.objs.get_db().dbc.execute(query)
            result = lg.objs.db.dbc.fetchall()
            if result:
                self.good_artists = sorted(set([item[0].lower() for item in result]))
        except Exception as e:
            self.fail(f,e)
    
    def set_albums(self):
        f = '[unmusic] tests.MediocreAlbums.set_albums'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            query = 'select ALBUMID,ARTIST,YEAR,ALBUM,RATING \
                     from ALBUMS where RATING > 0 and RATING < 8 \
                     order by ALBUMID'
            lg.objs.get_db().dbc.execute(query)
            self.albums = lg.objs.db.dbc.fetchall()
        except Exception as e:
            self.fail(f,e)
    
    def set_to_purge(self):
        f = '[unmusic] tests.MediocreAlbums.set_to_purge'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.albums or not self.good_artists or not self.good_tracks:
            self.Success = False
            sh.com.rep_empty(f)
            return
        for row in self.albums:
            album_id, artist, year, album, rating = row[0], row[1], row[2], row[3], row[4]
            if album_id in self.good_tracks or artist.lower() in self.good_artists:
                continue
            sub = '{}: {} - {} - {}: {}'.format(album_id,artist,year,album,rating)
            self.report.append(sub)
            self.purge.append(album_id)
    
    def show_report(self):
        f = '[unmusic] tests.MediocreAlbums.show_report'
        if not self.Success:
            sh.com.cancel(f)
            return
        albums = sh.com.set_figure_commas(len(self.albums))
        exclude = len(self.albums) - len(self.purge)
        exclude = sh.com.set_figure_commas(exclude)
        purge = sh.com.set_figure_commas(len(self.purge))
        self.report.append('')
        sub = _('Mediocre albums in total: {}, exclude: {}, purge: {}')
        sub = sub.format(albums,exclude,purge)
        self.report.append(sub)
        ids = [str(album_id) for album_id in self.purge]
        sub = _('IDs of the albums to purge: {}').format(', '.join(ids))
        self.report.append(sub)
        sh.com.run_fast_debug(f,'\n'.join(self.report))
    
    def run(self):
        self.set_good_artists()
        self.set_good_tracks()
        self.set_albums()
        self.set_to_purge()
        self.show_report()
        lg.objs.get_db().close()



class GoodRating:
    
    def __init__(self):
        self.Success = lg.objs.get_db().Success
        self.data = ()
        self.memory = {}
    
    def fail(self,func,error):
        self.Success = False
        mes = _('Operation has failed!\nDetails: {}').format(error)
        sh.objs.get_mes(func,mes).show_warning()
    
    def fetch(self):
        f = '[unmusic] tests.GoodRating.fetch'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            query = 'select ALBUMID,ARTIST,ALBUM,RATING from ALBUMS order by ARTIST'
            lg.objs.get_db().dbc.execute(query)
            self.data = lg.objs.db.dbc.fetchall()
        except Exception as e:
            self.fail(f,e)
    
    def export(self):
        f = '[unmusic] tests.GoodRating.export'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.data:
            self.Success = False
            sh.com.rep_empty(f)
            return
        for row in self.data:
            album_id, artist, album, rating = row[0], row[1], row[2], row[3]
            if not artist in self.memory:
                self.memory[artist] = {}
                self.memory[artist]['Good'] = False
                self.memory[artist]['albums'] = {}
            self.memory[artist]['albums'][album_id] = {'album':album
                                                      ,'rating':rating
                                                      }
    
    def _is_good(self,ids):
        ratings = [ids[id_]['rating'] for id_ in ids \
                   if ids[id_]['rating'] > 0
                  ]
        if ratings and min(ratings) > 7 and len(ratings) > 1:
            return True
    
    def set_good(self):
        f = '[unmusic] tests.GoodRating.set_good'
        if not self.Success:
            sh.com.cancel(f)
            return
        for artist in self.memory:
            if self._is_good(self.memory[artist]['albums']):
                self.memory[artist]['Good'] = True
    
    def report(self):
        # Unlike BadArtistss, shows albums without ratings as well
        f = '[unmusic] tests.GoodRating.report'
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = []
        for artist in self.memory:
            if self.memory[artist]['Good']:
                sub = _('Artist: {}').format(artist)
                mes.append(sub)
                for album_id in self.memory[artist]['albums']:
                    sub = _('ID: {}, rating: {}').format(album_id,self.memory[artist]['albums'][album_id]['rating'])
                    mes.append(sub)
                mes.append('')
        sh.com.run_fast_debug(f,'\n'.join(mes))
    
    def run(self):
        self.fetch()
        self.export()
        self.set_good()
        self.report()
        lg.objs.get_db().close()



class BadArtists:
    
    def __init__(self):
        self.Success = lg.objs.get_db().Success
        self.data = ()
        self.memory = {}
    
    def fail(self,func,error):
        self.Success = False
        mes = _('Operation has failed!\nDetails: {}').format(error)
        sh.objs.get_mes(func,mes).show_warning()
    
    def fetch(self):
        f = '[unmusic] tests.BadArtists.fetch'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            query = 'select ALBUMID,ARTIST,ALBUM,RATING from ALBUMS order by ARTIST'
            lg.objs.get_db().dbc.execute(query)
            self.data = lg.objs.db.dbc.fetchall()
        except Exception as e:
            self.fail(f,e)
    
    def export(self):
        f = '[unmusic] tests.BadArtists.export'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.data:
            self.Success = False
            sh.com.rep_empty(f)
            return
        for row in self.data:
            album_id, artist, album, rating = row[0], row[1], row[2], row[3]
            if not artist in self.memory:
                self.memory[artist] = {}
                self.memory[artist]['Bad'] = False
                self.memory[artist]['albums'] = {}
            self.memory[artist]['albums'][album_id] = {'album':album
                                                      ,'rating':rating
                                                      }
    
    def _is_bad(self,ids):
        ratings = [ids[id_]['rating'] for id_ in ids \
                   if ids[id_]['rating'] > 0
                  ]
        if ratings and max(ratings) < 7 and len(ratings) > 1:
            return True
    
    def set_bad(self):
        f = '[unmusic] tests.BadArtists.set_bad'
        if not self.Success:
            sh.com.cancel(f)
            return
        for artist in self.memory:
            if self._is_bad(self.memory[artist]['albums']):
                self.memory[artist]['Bad'] = True
    
    def report(self):
        f = '[unmusic] tests.BadArtists.report'
        if not self.Success:
            sh.com.cancel(f)
            return
        ids = []
        mes = []
        for artist in self.memory:
            if self.memory[artist]['Bad']:
                sub = _('Artist: {}').format(artist)
                mes.append(sub)
                for album_id in self.memory[artist]['albums']:
                    if self.memory[artist]['albums'][album_id]['rating'] > 0:
                        sub = _('ID: {}, rating: {}').format(album_id,self.memory[artist]['albums'][album_id]['rating'])
                        mes.append(sub)
                        ids.append(album_id)
                mes.append('')
        mes.append('')
        ids = sorted(ids)
        ids = [str(item) for item in ids]
        sub = _('All IDs: {}').format(', '.join(ids))
        mes.append(sub)
        sh.com.run_fast_debug(f,'\n'.join(mes))
    
    def run(self):
        self.fetch()
        self.export()
        self.set_bad()
        self.report()
        lg.objs.get_db().close()



class AlbumRating:
    
    def __init__(self,ids):
        self.Success = lg.objs.get_db().Success
        self.ids = ids
    
    def set_no(self):
        f = '[unmusic] tests.AlbumRating.set_no'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.no < 1:
            self.Success = False
            mes = _('Wrong input data: "{}"!').format(self.no)
            sh.objs.get_mes(f,mes).show_warning()
            return
        lg.objs.get_db().albumid = self.no
    
    def get(self):
        f = '[unmusic] tests.AlbumRating.get'
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = _('Album: {}, average rating: {}')
        mes = mes.format(self.no,lg.objs.get_db().get_rating())
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def loop(self):
        for self.no in self.ids:
            self.set_no()
            self.get()
    
    def run(self):
        self.loop()
        lg.objs.get_db().close()



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
    #BadArtists().run()
    #GoodRating().run()
    MediocreAlbums().run()
    sh.com.end()
