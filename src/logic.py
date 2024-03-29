#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import io
import re
import phrydy
import db

from skl_shared.localize import _
import skl_shared.shared as sh
import skl_shared.image.controller as im

VERSION = '1.1'
# Derived from 'phrydy.mediafile.TYPES'
TYPES = ['.mp3', '.aac', '.alac', '.ogg', '.opus', '.flac', '.ape', '.wv'
        ,'.mpc', '.asf', '.aiff', '.dsf'
        ]
#NOTE: Do not localize (being stored in DB)
GENRES = ('?', 'Alternative Rock', 'Ambient', 'Black Metal', 'Blues'
         ,'Brutal Death Metal', 'Chanson', 'Classical', 'Death Metal'
         ,'Death Metal/Grindcore', 'Death/Black Metal'
         ,'Death/Thrash Metal', 'Deathcore', 'Electronic', 'Ethnic', 'Game'
         ,'Goregrind', 'Grindcore', 'Heavy Metal', 'Industrial Metal'
         ,'Melodic Death Metal', 'Metal', 'Pop', 'Power Metal', 'Rap'
         ,'Relaxation', 'Rock', 'Soundtrack', 'Technical Brutal Death Metal'
         ,'Technical Death Metal', 'Thrash Metal', 'Vocal'
         )
''' Can have genres not comprised by GENRES (since GENRES is used to fill GUI
    and has a limit).
'''
LIGHT = ('Alternative Rock', 'Ambient', 'Blues', 'Chanson', 'Classical'
        ,'Electronic', 'Ethnic', 'Game', 'Pop', 'Rap', 'Relaxation', 'Rock'
        ,'Soundtrack', 'Vocal', 'Folk'
        )
HEAVY = ('Black Metal', 'Brutal Death Metal', 'Death Metal'
        ,'Death Metal/Grindcore', 'Death/Black Metal', 'Death/Thrash Metal'
        ,'Deathcore', 'Goregrind', 'Grindcore', 'Heavy Metal'
        ,'Industrial Metal', 'Melodic Death Metal', 'Metal', 'Power Metal'
        ,'Technical Brutal Death Metal', 'Technical Death Metal'
        ,'Thrash Metal'
        )


class Collection:
    
    def __init__(self):
        self.set_paths()
    
    def set_paths(self):
        self.local = objs.get_default().ihome.add_share(_('local collection'))
        self.external = objs.default.ihome.add_share(_('external collection'))
        self.mobile = objs.default.ihome.add_share(_('mobile collection'))
    
    def get_local_album(self, albumid=None):
        if albumid is None:
            return os.path.join(self.local, str(objs.get_db().albumid))
        else:
            return os.path.join(self.local, str(albumid))
    
    def get_ext_album(self, albumid=None):
        if albumid is None:
            return os.path.join(self.external, str(objs.get_db().albumid))
        else:
            return os.path.join(self.external, str(albumid))
    
    def get_mob_album(self, albumid=None):
        if albumid is None:
            return os.path.join(self.mobile, str(objs.get_db().albumid))
        else:
            return os.path.join(self.mobile, str(albumid))
    
    def has_any_album(self, albumid=None):
        return self.has_local_album(albumid) or self.has_ext_album(albumid) \
                                             or self.has_mob_album(albumid)
    
    def has_local_album(self, albumid=None):
        return os.path.exists(self.get_local_album(albumid))
    
    def has_ext_album(self, albumid=None):
        return os.path.exists(self.get_ext_album(albumid))
    
    def has_mob_album(self, albumid=None):
        return os.path.exists(self.get_mob_album(albumid))



class Image:
    
    def __init__(self):
        self.dir = sh.Home('unmusic').add_share(_('Images'))
        self.Success = sh.Path(self.dir).create()
        self.path = ''
    
    def get(self):
        f = '[unmusic] logic.Image.get'
        if not self.Success:
            sh.com.cancel(f)
            return self.path
        path = self.get_cover()
        if path and os.path.exists(path):
            self.path = path
        else:
            self.path = sh.objs.get_pdir().add('..','resources','cd.png')
        return self.path
    
    def get_cover(self):
        f = '[unmusic] logic.Image.get_cover'
        if not self.Success:
            sh.com.cancel(f)
            return
        name = str(objs.get_db().albumid) + '.jpg'
        return os.path.join(self.dir,name)
    
    def run(self):
        return self.get()



class ExportKeys:
    
    def run(self):
        sh.lg.globs['int']['curid'] = objs.get_db().albumid



class CreateConfig(sh.CreateConfig):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fill_int(self):
        section = _('Integers')
        self.add_section(section)
        section_abbr = self.sections[-1].abbr
        
        key = 'curid'
        comment = _('[Autosave] Album ID to load at startup')
        self.add_key(section, section_abbr, key, comment)



class DefaultKeys(sh.DefaultKeys):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load()
    
    def load(self):
        self._load_int()
    
    def _load_int(self):
        sh.lg.globs['int'].update({'curid':1})



class BadMusic:
    
    def __init__(self):
        self.set_values()
        self.Success = objs.get_db().Success
    
    def set_values(self):
        self.Success = True
        self.rates = []
        self.sizes = []
        self.dellst = []
        self.local = ''
        self.exter = ''
        self.mobil = ''
        
    def get_all_carriers(self):
        f = '[unmusic] logic.BadMusic.get_all_carriers'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.local = objs.get_default().ihome.add_share(_('local collection'))
        self.exter = objs.default.ihome.add_share(_('external collection'))
        self.mobil = objs.default.ihome.add_share(_('mobile collection'))
        mes = _('Local collection: {}').format(self.local)
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = _('External collection: {}').format(self.exter)
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = _('Mobile collection: {}').format(self.mobil)
        sh.objs.get_mes(f,mes,True).show_debug()
        if self.local and self.exter and self.mobil:
            return True
        else:
            self.Success = False
            mes = _('Empty output is not allowed!')
            sh.objs.get_mes(f,mes).show_warning()
    
    def get_affected_carriers(self):
        f = '[unmusic] logic.BadMusic.get_affected_carriers'
        self.get_all_carriers()
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.dellst:
            sh.com.rep_empty(f)
            return
        affected = []
        for item in self.dellst:
            if self.local in item:
                affected.append(_('local collection'))
                break
        for item in self.dellst:
            if self.exter in item:
                affected.append(_('external collection'))
                break
        for item in self.dellst:
            if self.mobil in item:
                affected.append(_('mobile collection'))
                break
        return affected
    
    def delete(self):
        f = '[unmusic] logic.BadMusic.delete'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.dellst:
            sh.com.rep_empty(f)
            return
        for album in self.dellst:
            if not sh.Directory(album).delete():
                mes = _('Operation has been canceled.')
                sh.objs.get_mes(f,mes).show_warning()
                break
    
    def report(self):
        f = '[unmusic] logic.BadMusic.report'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.rates or not self.sizes:
            sh.com.rep_empty(f)
            return
        iterable = []
        for i in range(len(self.rates)):
            if self.sizes[i]:
                size = sh.com.get_human_size (bsize = self.sizes[i]
                                             ,LargeOnly = True
                                             )
            else:
                size = _('N/A')
            iterable.append(self.rates[i]+[size])
        headers = ('ID','ALBUM','MIN','MAX','SIZE')
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,Transpose = True
                           ,maxrow = 70
                           ).run()
        sh.com.run_fast_debug(f,mes)
    
    def get_sizes(self):
        f = '[unmusic] logic.BadMusic.get_sizes'
        self.get_all_carriers()
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.rates:
            sh.com.rep_empty(f)
            return
        for item in self.rates:
            albumid = str(item[0])
            path1 = os.path.join(self.local,albumid)
            path2 = os.path.join(self.exter,albumid)
            path3 = os.path.join(self.mobil,albumid)
            if os.path.exists(path1):
                size1 = sh.Directory(path1).get_size()
                self.dellst.append(path1)
            else:
                size1 = 0
            if os.path.exists(path2):
                size2 = sh.Directory(path2).get_size()
                self.dellst.append(path2)
            else:
                size2 = 0
            if os.path.exists(path3):
                size3 = sh.Directory(path3).get_size()
                self.dellst.append(path3)
            else:
                size3 = 0
            size = size1 + size2 + size3
            self.sizes.append(size)
        return self.sizes
    
    def get_rates(self, limit=0, max_rate=4):
        f = '[unmusic] logic.BadMusic.get_rates'
        if not self.Success:
            sh.com.cancel(f)
            return
        # ALBUMID (0), ALBUM (1), ARTIST (2), YEAR (3)
        albums = objs.get_db().get_albums(limit)
        if not albums:
            sh.com.cancel(f)
            return
        old = objs.db.albumid
        for album in albums:
            objs.db.albumid = album[0]
            mes = _('Process album ID: {}')
            mes = mes.format(objs.db.albumid)
            sh.objs.get_mes(f,mes,True).show_debug()
            rates = objs.db.get_rates()
            if not rates:
                sh.com.rep_empty(f)
                continue
            if min(rates) > 0 and max(rates) <= max_rate:
                album_title = [str(album[2]), str(album[3]), str(album[1])]
                album_title = ' - '.join(album_title)
                item = [album[0], album_title, min(rates), max(rates)]
                self.rates.append(item)
        objs.db.albumid = old
        return self.rates



class Play:
    
    def __init__(self):
        self.set_values()
        self.Success = objs.get_db().Success
    
    def call_player(self):
        f = '[unmusic] logic.Play.call_player'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.get_playlist():
            sh.com.rep_empty(f)
            return
        sh.lg.Launch(self.playlist).launch_default()
    
    def set_values(self):
        self.Success = True
        self.album = ''
        self.playlist = ''
        self.audio = []
        self.nos = []
        self.titles = []
        self.len_ = []
    
    def get_album(self):
        f = '[unmusic] logic.Play.get_album'
        if not self.Success:
            sh.com.cancel(f)
            return self.album
        if not self.album:
            local_album = objs.get_default().ihome.add_share (_('local collection')
                                                             ,str(objs.get_db().albumid)
                                                             )
            exter_album = objs.default.ihome.add_share (_('external collection')
                                                       ,str(objs.db.albumid)
                                                       )
            local_exists = os.path.exists(local_album)
            exter_exists = os.path.exists(exter_album)
            if local_exists:
                self.album = local_album
            elif exter_exists:
                self.album = exter_album
        return self.album
    
    def get_audio(self):
        f = '[unmusic] logic.Play.get_audio'
        if not self.Success:
            sh.com.cancel(f)
            return self.audio
        if not self.audio:
            idir = Directory(self.get_album())
            idir.create_list()
            self.Success = idir.Success
            if idir.audio:
                self.audio = idir.audio
        return self.audio
    
    def get_available(self):
        f = '[unmusic] logic.Play.get_available'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.get_audio()
        if not (self.audio and self.nos and self.titles and self.len_):
            self.Success = False
            sh.com.rep_empty(f)
            return
        result = []
        errors = []
        for no in self.nos:
            try:
                result.append(self.audio[no])
            except IndexError:
                errors.append(no)
        ''' This may happen when some tracks have been deleted from
            a collection after filling DB or when there is a mismatch of
            ALBUMID stored in DB and the folder named after ALBUMID in the
            collection. In any case, this should not normally happen.
        '''
        if errors:
            for no in errors:
                try:
                    del self.titles[no]
                    del self.nos[no]
                    del self.len_[no]
                except IndexError:
                    pass
            errors = [str(error) for error in errors]
            mes = _('Tracks {} have not been found in "{}"!')
            mes = mes.format(errors,self.get_album())
            sh.objs.get_mes(f,mes).show_warning()
        if len(self.nos) == len(self.titles) == len(self.len_):
            pass
        else:
            self.Success = False
            sub = '{} = {} = {}'.format (len(self.nos)
                                        ,len(self.titles)
                                        ,len(self.len_)
                                        )
            mes = _('Condition "{}" is not observed!')
            mes = mes.format(sub)
            sh.objs.get_mes(f,mes).show_error()
        return result
    
    def get_playlist(self):
        f = '[unmusic] logic.Play.get_playlist'
        if self.Success:
            if not self.playlist:
                self.playlist = _('playlist') + '.m3u8'
                self.playlist = objs.get_default().ihome.add_share(self.playlist)
        else:
            sh.com.cancel(f)
        return self.playlist
    
    def gen_list(self):
        f = '[unmusic] logic.Play.gen_list'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.nos:
            sh.com.rep_empty(f)
            return
        self.out = io.StringIO()
        result = objs.get_db().get_album()
        ''' Adding #EXTINF will allow to use tags in those players that support
            it (e.g., clementine, deadbeef). This entry should have the
            following format: '#EXTINF:191,Artist Name - Track Title' (multiple
            hyphens may not be supported).
        '''
        if result:
            ''' The hyphen here is actually useless, but
                'deadbeef' will not separate an album and
                a title correctly otherwise.
            '''
            header = result[1] + ': ' + result[0] + ' - '
        else:
            header = ''
        files = self.get_available()
        if files and self.nos:
            self.out.write('#EXTM3U\n')
            for i in range(len(files)):
                self.out.write('#EXTINF:')
                self.out.write(str(int(self.len_[i])))
                self.out.write(',')
                self.out.write(header)
                self.out.write(str(self.nos[i]+1))
                self.out.write('. ')
                ''' Replacing a hyphen will allow 'deadbeef'
                    to correctly distinguish between an album
                    and a title.
                '''
                self.out.write(self.titles[i].replace(' - ',': ').replace(' ~ ',': '))
                self.out.write('\n')
                self.out.write(files[i])
                self.out.write('\n')
        else:
            sh.com.rep_empty(f)
        text = self.out.getvalue()
        self.out.close()
        if not text:
            sh.com.rep_empty(f)
            return
        sh.lg.WriteTextFile (file = self.get_playlist()
                            ,Rewrite = True
                            ).write(text)
    
    def play_all_tracks(self):
        f = '[unmusic] logic.Play.play_all_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        tracks = objs.get_db().get_tracks()
        if not tracks:
            sh.com.rep_empty(f)
            return
        self.titles = [track[0] for track in tracks]
        self.len_ = [track[5] for track in tracks]
        # '-1' since count starts with 1 in DB and we need 0
        self.nos = [track[1] - 1 for track in tracks]
        self.gen_list()
        self.call_player()
    
    def play_good_tracks(self, rating=8):
        f = '[unmusic] logic.Play.play_good_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        tracks = objs.get_db().get_good_tracks(rating)
        if not tracks:
            sh.com.rep_empty(f)
            return
        self.titles = [track[0] for track in tracks]
        self.len_ = [track[5] for track in tracks]
        # '-1' since count starts with 1 in DB and we need 0
        self.nos = [track[1] - 1 for track in tracks]
        self.gen_list()
        self.call_player()



class AlbumEditor:
    
    def __init__(self):
        self.Success = True
    
    def _get_album(self, albumid):
        local_album = objs.get_default().ihome.add_share (_('local collection')
                                                         ,str(albumid)
                                                         )
        exter_album = objs.default.ihome.add_share (_('external collection')
                                                   ,str(albumid)
                                                   )
        local_exists = os.path.exists(local_album)
        exter_exists = os.path.exists(exter_album)
        if local_exists:
            return local_album
        elif exter_exists:
            return exter_album
    
    def _has_any_album(self, albumids):
        for albumid in albumids:
            if objs.get_collection().has_any_album(albumid):
                return albumid
    
    def set_prev_unrated(self):
        f = '[unmusic] logic.AlbumEditor.set_prev_unrated'
        if not self.Success:
            sh.com.cancel(f)
            return
        albumids = objs.get_db().get_prev_unrated(objs.db.albumid)
        self._set_unrated(albumids)
    
    def set_next_unrated(self):
        f = '[unmusic] logic.AlbumEditor.set_next_unrated'
        if not self.Success:
            sh.com.cancel(f)
            return
        albumids = objs.get_db().get_next_unrated(objs.db.albumid)
        self._set_unrated(albumids)
    
    def _set_unrated(self, albumids):
        f = '[unmusic] logic.AlbumEditor._set_unrated'
        if not albumids:
            mes = _('No more matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        albumid = self._has_any_album(albumids)
        if albumid is None:
            mes = _('No more matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        objs.db.albumid = albumid
        self.check_no()
    
    def set_prev_rated(self, rating=0):
        # This code is orphaned, but may be useful in the future
        f = '[unmusic] logic.AlbumEditor.set_prev_rated'
        if not self.Success:
            sh.com.cancel(f)
            return
        albumid = objs.get_db().get_prev_rated(rating, objs.db.albumid)
        if not albumid:
            mes = _('No more matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        objs.db.albumid = albumid
        self.check_no()
    
    def set_next_rated(self, rating=0):
        # This code is orphaned, but may be useful in the future
        f = '[unmusic] logic.AlbumEditor.set_next_rated'
        if not self.Success:
            sh.com.cancel(f)
            return
        albumid = objs.get_db().get_next_rated(rating, objs.db.albumid)
        if not albumid:
            mes = _('No more matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        objs.db.albumid = albumid
        self.check_no()
    
    def get_mean_bitrate(self):
        f = '[unmusic] logic.AlbumEditor.get_mean_bitrate'
        if not self.Success:
            sh.com.cancel(f)
            return
        mean = objs.get_db().get_bitrate()
        if not mean:
            sh.com.rep_empty(f)
            return
        mean = [rating for rating in mean if rating]
        if not mean:
            return 0
        # Return 'int' since we don't need 'float' here
        return sum(mean) // len(mean)
    
    def get_mean_rating(self):
        f = '[unmusic] logic.AlbumEditor.get_mean_rating'
        if not self.Success:
            sh.com.cancel(f)
            return 0.0
        mean = objs.get_db().get_rates()
        if not mean:
            sh.com.rep_empty(f)
            return 0.0
        ''' We should not count tracks with an undefined (0) rating, otherwise,
            if there is a mix of tracks with zero and non-zero rating,
            an overall rating will be lower than a mean rating of the non-zero
            rating tracks.
        '''
        if not mean or 0 in mean:
            return 0.0
        ''' This intentionally returns float even if all elements are equal.
            It's better to show at least 2 digits after the dot since, for
            example, an album with 30 tracks, where 29 of them have the rating
            of 8 and 1 - of 9, will have the mean rating of ~8.03.
        '''
        return round(sum(mean) / len(mean), 2)
    
    def check_no(self):
        f = '[unmusic] logic.AlbumEditor.check_no'
        if self.Success:
            objs.get_db().albumid = sh.lg.Input(f, objs.get_db().albumid).get_integer()
        else:
            sh.com.cancel(f)
        return objs.get_db().albumid
    
    def get_min(self):
        f = '[unmusic] logic.AlbumEditor.get_min'
        if not self.Success:
            sh.com.cancel(f)
            return 0
        return sh.lg.Input(f,objs.get_db().get_min_id()).get_integer()
    
    def get_max(self):
        f = '[unmusic] logic.AlbumEditor.get_max'
        if not self.Success:
            sh.com.cancel(f)
            return 0
        _max = objs.get_db().get_max_id()
        if not isinstance(_max, int):
            mes = _('The database is empty. You need to fill it first.')
            sh.objs.get_mes(f,mes).show_warning()
            return 0
        return _max
    
    def inc(self):
        f = '[unmusic] logic.AlbumEditor.inc'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.check_no() == self.get_max():
            objs.get_db().albumid = self.get_min()
        else:
            objs.get_db().albumid = objs.get_db().get_next_id()
            self.check_no()
    
    def dec(self):
        f = '[unmusic] logic.AlbumEditor.dec'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.check_no() == self.get_min():
            objs.get_db().albumid = self.get_max()
        else:
            objs.get_db().albumid = objs.get_db().get_prev_id()
            self.check_no()

    def _compare_albums(self, old, new):
        # Quotes in the text will fail the query, so we screen them
        new[0] = str(new[0]).replace('"', '""')
        new[1] = str(new[1]).replace('"', '""')
        new[3] = str(new[3]).replace('"', '""')
        new[4] = str(new[4]).replace('"', '""')
        new[5] = str(new[5]).replace('"', '""')
        search = [new[0], new[1], str(new[2]), new[3], new[4], new[5]]
        search = ' '.join(search)
        search = sh.lg.Text(search).delete_duplicate_spaces()
        search = search.strip().lower()
        
        add = []
        for i in range(len(new)):
            if old[i] != new[i]:
                if i == 0:
                    base = 'ALBUM="%s"'
                elif i == 1:
                    base = 'ARTIST="%s"'
                elif i == 2:
                    base = 'YEAR="%d"'
                elif i == 3:
                    base = 'GENRE="%s"'
                elif i == 4:
                    base = 'COUNTRY="%s"'
                elif i == 5:
                    base = 'COMMENT="%s"'
                elif i == 6:
                    base = 'RATING="%f"'
                add.append(base % new[i])
        if add:
            add.append('SEARCH="%s"' % search)
            add = 'begin;update ALBUMS set ' + ','.join(add)
            add += ' where ALBUMID=%d;commit;' % objs.get_db().albumid
            return add



class Directory:
    
    def __init__(self, path):
        self.set_values()
        if path:
            self.reset(path)
    
    def _set_no(self, i, max_len):
        no = str(i + 1)
        while len(no) < max_len:
            no = '0' + no
        return no
    
    def save_image(self):
        f = '[unmusic] logic.Directory.save_image'
        if not self.Success or not objs.get_image().Success:
            sh.com.cancel(f)
            return
        # Non-emptiness of 'self.tracks' was already checked in 'self.run'
        if not self.tracks[0].image:
            sh.com.rep_lazy(f)
            return
        name = str(objs.get_db().albumid) + '.jpg'
        path = os.path.join(objs.image.dir, name)
        mes = _('Save "{}"').format(path)
        sh.objs.get_mes(f,mes,True).show_info()
        if not sh.com.rewrite(path):
            mes = _('Operation has been canceled by the user.')
            sh.objs.get_mes(f,mes,True).show_info()
            return
        iimage = im.Image()
        iimage.bytes_ = self.tracks[0].image
        iimage.get_loader()
        iimage.convert2rgb()
        iimage.save(path, 'JPEG')
        return iimage.Success
    
    def move_tracks(self):
        f = '[unmusic] logic.Directory.move_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        success = []
        ''' The current algorithm of tracks renumbering guarantees that
            the file list (*unless changed*) will have a consecutive numbering
            of tracks.
        '''
        max_len = len(self.audio)
        max_len = len(str(max_len))
        for i in range(len(self.audio)):
            file = self.audio[i]
            no = self._set_no(i, max_len)
            basename = no + sh.lg.Path(file).get_ext().lower()
            dest = os.path.join(self.target, basename)
            success.append(sh.lg.File(file=file, dest=dest).move())
        self.Success = not (False in success or None in success)
    
    def purge(self):
        f = '[unmusic] logic.Directory.purge'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.tracks:
            sh.com.rep_empty(f)
            return
        mes = _('Purge tracks')
        sh.objs.get_mes(f, mes, True).show_info()
        for track in self.tracks:
            track.purge()
            track.save()
            if not track.Success:
                self.Success = False
                return
    
    def create_target(self):
        f = '[unmusic] logic.Directory.create_target'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not objs.get_db().albumid:
            self.Success = False
            sh.com.rep_empty(f)
            return
        self.target = objs.get_default().ihome.add_share (_('processed')
                                                         ,str(objs.db.albumid)
                                                         )
        self.Success = sh.lg.Path(self.target).create()
    
    def reset(self, path):
        self.set_values()
        self.path = path
        self.idir = sh.lg.Directory(self.path)
        self.Success = self.idir.Success
        
    def get_rating(self):
        f = '[unmusic] logic.Directory.get_rating'
        if not self.Success:
            sh.com.cancel(f)
            return
        match = re.search(r'\(rating (\d+)\)', self.path)
        if match:
            try:
                rating = match.group(1)
                if rating.isdigit():
                    self.rating = int(rating)
            except IndexError:
                pass
    
    def run(self):
        self.get_rating()
        self.create_list()
        self.get_tracks()
        if self.tracks:
            self.renumber_tracks()
            self.save_meta()
            ''' The following actions should be carried out
                only if we want to obfuscate tracks.
            '''
            self.create_target()
            self.purge()
            self.move_tracks()
            self.save_image()
        return self.Success
    
    def add_album_meta(self):
        f = '[unmusic] logic.Directory.add_album_meta'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.tracks:
            sh.com.rep_empty(f)
            return
        ''' If a track could not be processed, empty tags will be returned,
            which, when written to DB, can cause confusion. Here we check that
            the track was processed successfully.
        '''
        if not self.tracks[0].audio:
            sh.com.rep_empty(f)
            return
        album = self.tracks[0].album
        artist = self.tracks[0].artist
        year = self.tracks[0].year
        genre = self.tracks[0].genre
        album = com.sanitize(album)
        album = com.delete_album_trash(album)
        artist = com.sanitize(artist)
        if str(year).isdigit():
            year = int(year)
        else:
            # Prevent from storing an incorrect value
            year = 0
        genre = com.sanitize(genre)
        
        search = [album,artist,str(year),genre]
        search = ' '.join(search)
        search = search.lower()
        
        objs.get_db().add_album([album, artist, year, genre, '', '', search, 0])
    
    def _add_tracks_meta(self, albumid):
        f = '[unmusic] logic.Directory._add_tracks_meta'
        for track in self.tracks:
            data = track.get_track_meta()
            ''' If a track could not be processed, empty tags will be returned,
                which, when written to DB, can cause confusion. Here we check
                that the track was processed successfully.
            '''
            if not track.audio or not data:
                sh.com.rep_empty(f)
                return
            objs.get_db().albumid = albumid
            objs.db.add_track ([albumid, data[0], data[1], data[2], '', data[3]
                               ,data[4], data[5], self.rating
                               ]
                              )
    
    def save_meta(self):
        f = '[unmusic] logic.Directory.save_meta'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.tracks:
            sh.com.rep_empty(f)
            return
        ''' It seems better to create new ALBUMID without checking if it
            already exists. Reasons:
            1) CD1, CD2, etc. may share same tags.
            2) Albums of different bitrate may share same tags, however, they
               are actually different albums.
            3) Since extracting metadata and obfucating are united by default,
               the program may try to overwrite already existing files in case
               there is an ALBUMID conflict (which does not and should not fail
               'Success').
            4) If tags have been edited after extraction, there is no easy way
               to establish if DB already has a corresponding ALBUMID.
        '''
        self.add_album_meta()
        albumid = objs.db.get_max_id()
        if not albumid:
            sh.com.rep_empty(f)
            return
        self._add_tracks_meta(albumid)
        mes = _('Album {}: {} tracks.')
        mes = mes.format(albumid, len(self.tracks))
        sh.objs.get_mes(f,mes,True).show_info()
    
    def set_values(self):
        self.Success = True
        self.idir = None
        self.path = ''
        self.target = ''
        self.rating = 0
        self.files = []
        self.audio = []
        self.tracks = []
    
    def create_list(self):
        f = '[unmusic] logic.Directory.create_list'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.files:
            return self.files
        if not self.idir:
            sh.com.rep_empty(f)
            return self.files
        self.files = self.idir.get_files()
        for file in self.files:
            if sh.lg.Path(file).get_ext().lower() in TYPES:
                self.audio.append(file)
        return self.files
    
    def renumber_tracks(self):
        ''' We use track NO field instead of an autoincrement, so we must keep
            these fields unique within the same album.
        '''
        f = '[unmusic] logic.Directory.renumber_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        nos = [i + 1 for i in range(len(self.tracks))]
        count = 0
        for i in range(len(self.tracks)):
            if self.tracks[i].no != nos[i]:
                count += 1
                self.tracks[i].no = nos[i]
        if count:
            mes = _('{}/{} tracks have been renumbered.')
            mes = mes.format(count, len(self.tracks))
            sh.objs.get_mes(f,mes,True).show_warning()
    
    def get_tracks(self):
        f = '[unmusic] logic.Directory.get_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.tracks:
            return self.tracks
        if not self.audio:
            mes = _('Folder "{}" has no audio files.').format(self.path)
            sh.objs.get_mes(f, mes, True).show_info()
            return self.tracks
        for file in self.audio:
            self.tracks.append(Track(file=file))
        return self.tracks



class DefaultConfig:
    
    def __init__(self):
        self.set_values()
        self.ihome = sh.lg.Home(app_name='unmusic')
        self.Success = self.ihome.create_conf()
    
    def get_config(self):
        f = '[unmusic] logic.DefaultConfig.get_config'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.fconf:
            self.fconf = self.ihome.add_config('unmusic.cfg')
        return self.fconf
    
    def run(self):
        self.get_db()
    
    def set_values(self):
        self.fdb = ''
        self.fconf = ''
    
    def get_db(self):
        f = '[unmusic] logic.DefaultConfig.get_db'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.fdb = self.ihome.add_config('unmusic.db')
        if not self.fdb:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if os.path.exists(self.fdb):
            self.Success = sh.lg.File(file=self.fdb).Success



class Objects:
    
    def __init__(self):
        self.default = self.db = self.config = self.image = self.collection \
                     = None
        
    def get_collection(self):
        if not self.collection:
            self.collection = Collection()
        return self.collection
    
    def get_image(self):
        if self.image is None:
            self.image = Image()
        return self.image
    
    def get_config(self):
        if self.config is None:
            self.config = sh.Config(objs.get_default().get_config())
            self.config.run()
        return self.config
    
    def get_db(self):
        f = '[unmusic] logic.Objects.get_db'
        if self.db is not None:
            return self.db
        path = self.get_default().fdb
        if not self.default.Success:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes, True).show_warning()
            self.db = db.DB()
            return self.db
        self.db = db.DB(path)
        return self.db
    
    def get_default(self):
        if self.default is None:
            self.default = DefaultConfig()
            self.default.run()
        return self.default



class Track:
    
    def __init__(self, file):
        self.set_values()
        self.file = file
        self.Success = sh.lg.File(self.file).Success
        self.load()
        self.set_info()
        self.decode()
        self.delete_unsupported()
    
    def delete_unsupported(self):
        f = '[unmusic] logic.Track.delete_unsupported'
        if not self.Success:
            sh.com.cancel(f)
            return
        # Other fields should be processed before writing to DB
        self.title = sh.lg.Text(self.title).delete_unsupported()
        self.lyrics = sh.lg.Text(self.lyrics).delete_unsupported()
    
    def purge(self):
        f = '[unmusic] logic.Track.purge'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.audio:
            sh.com.rep_empty(f)
            return
        try:
            self.audio.delete()
            self.audio.images = {}
        except Exception as e:
            self.Success = False
            mes = _('Third-party module has failed!\n\nDetails: {}')
            mes = mes.format(e)
            sh.objs.get_mes(f,mes).show_warning()
    
    def save(self):
        ''' This is only needed if the file was changed by means of 'phrydy',
            see, for example, 'self.purge'.
        '''
        f = '[unmusic] logic.Track.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.audio:
            sh.com.rep_empty(f)
            return
        try:
            self.audio.save()
        except Exception as e:
            self.Success = False
            mes = _('Third-party module has failed!\n\nDetails: {}')
            mes = mes.format(e)
            sh.objs.get_mes(f,mes).show_warning()
    
    def decode(self):
        # Fix Cyrillic tags
        f = '[unmusic] logic.Track.decode'
        if not self.Success:
            sh.com.cancel(f)
            return
        # Other fields should be decoded before writing to DB
        self.title = com.decode(self.title)
        self.lyrics = com.decode(self.lyrics)
    
    def get_track_meta(self):
        f = '[unmusic] logic.Track.get_track_meta'
        if not self.Success:
            sh.com.cancel(f)
            return
        search = [self.title,self.lyrics]
        search = ' '.join(search)
        search = sh.lg.Text(search).delete_duplicate_spaces()
        search = search.strip().lower()
        return (self.title, self.no, self.lyrics, search, self.bitrate
               ,self.length
               )
    
    def set_values(self):
        self.Success = True
        self.audio = None
        self.image = None
        self.artist = ''
        self.album = ''
        self.title = ''
        self.lyrics = ''
        self.genre = ''
        self.year = 0
        self.bitrate = 0
        self.length = 0
        self.no = 1
    
    def show_summary(self):
        f = '[unmusic] logic.Track.show_summary'
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = _('Artist: {}').format(self.artist)
        mes += '\n'
        mes += _('Album: {}').format(self.album)
        mes += '\n'
        mes += _('Genre: {}').format(self.genre)
        mes += '\n'
        mes += _('Year: {}').format(self.year)
        mes += '\n'
        mes += _('Track #: {}').format(self.no)
        mes += '\n'
        mes += _('Title: {}').format(self.title)
        mes += '\n'
        mes += _('Lyrics: {}').format(self.lyrics)
        if self.length:
            minutes = self.length // 60
            seconds = self.length - minutes * 60
        else:
            minutes = seconds = 0
        mes += _('Length: {} {} {} {}').format (minutes, _('min'), seconds
                                               ,_('sec')
                                               )
        mes +=  '\n'
        sh.objs.get_mes(f,mes).show_info()
    
    def extract_title(self):
        f = '[unmusic] logic.Track.extract_title'
        if not self.Success:
            sh.com.cancel(f)
            return
        title = sh.lg.Path(self.file).get_filename()
        if not title:
            return
        result = re.sub('^\d+[\.]{0,1}[\s]{0,1}','',title)
        if not result:
            # If a title is just a digit + an extension.
            return title
        return result
    
    def _set_info(self):
        f = '[unmusic] logic.Track._set_info'
        artist = [self.audio.artist, self.audio.albumartist
                 ,self.audio.composer
                 ]
        artist = [item for item in artist if item]
        if artist:
            self.artist = artist[0]
        ''' - Prevents from type mismatch (e.g., 'phrydy' returns 'None'
              in case a year is not set).
            - If an input value is empty then we do not overwrite a default
              value which should be of a correct type. This does not work
              as a separate procedure.
        '''
        if self.audio.album:
            self.album = str(self.audio.album)
        else:
            dirname = sh.lg.Path(self.file).get_dirname()
            dirname = sh.lg.Path(dirname).get_basename()
            self.album = '[[' + dirname + ']]'
        if self.audio.genre:
            self.genre = str(self.audio.genre)
        if self.audio.year:
            self.year = sh.lg.Input (title = f
                                    ,value = self.audio.year
                                    ).get_integer()
        if self.audio.title:
            self.title = str(self.audio.title)
        else:
            extracted = self.extract_title()
            if extracted:
                self.title = extracted
        if self.audio.bitrate:
            self.bitrate = self.audio.bitrate
        if self.audio.length:
            self.length = self.audio.length
        if str(self.audio.track).isdigit():
            self.no = self.audio.track
        if self.audio.lyrics:
            self.lyrics = str(self.audio.lyrics)
        if self.audio.images:
            self.image = self.audio.images[0].data
    
    def set_info(self):
        f = '[unmusic] logic.Track.set_info'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.audio:
            sh.com.rep_empty(f)
            return
        try:
            self._set_info()
        except Exception as e:
            mes = _('Third-party module has failed!\n\nDetails: {}')
            mes = mes.format(e)
            sh.objs.get_mes(f,mes).show_warning()
    
    def load(self):
        f = '[unmusic] logic.Track.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.audio:
            return self.audio
        try:
            self.audio = phrydy.MediaFile(self.file)
        except Exception as e:
            mes = _('Third-party module has failed!\n\nDetails: {}')
            mes = mes.format(e)
            sh.objs.get_mes(f,mes).show_warning()
        return self.audio



class Walker:
    
    def __init__(self,path=''):
        if path:
            self.reset(path=path)
    
    def delete_empty(self):
        ''' Delete empty folders. Since 'sh.lg.Directory' instance is
            recreated each time, we can call this procedure at any time
            without the need to reset 'Walker'.
        '''
        f = '[unmusic] logic.Walker.delete_empty'
        self.get_dirs()
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.dirs:
            sh.com.rep_empty(f)
            return
        for folder in self.dirs:
            sh.lg.Directory(folder).delete_empty()
    
    def reset(self,path):
        self.set_values()
        self.path = path
        self.idir = sh.lg.Directory(self.path)
        self.Success = self.idir.Success
    
    def get_dirs(self):
        f = '[unmusic] logic.Walker.get_dirs'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.dirs:
            return self.dirs
        for dirpath, dirnames, filenames in os.walk(self.idir.dir):
            if not dirpath in self.dirs:
                self.dirs.append(dirpath)
        return self.dirs
    
    def set_values(self):
        self.Success = True
        self.path = ''
        self.dirs = []



class Commands:
    
    def __init__(self):
        pass
    
    def save_config(self):
        ExportKeys().run()
        CreateConfig(objs.get_default().get_config()).run()
    
    def restore_id(self):
        f = '[unmusic] logic.Commands.restore_id'
        min_ = objs.get_db().get_min_id()
        max_ = objs.db.get_max_id()
        if not min_ or not max_:
            sh.com.rep_empty(f)
            return
        if min_ <= sh.lg.globs['int']['curid'] <= max_:
            objs.db.albumid = sh.lg.globs['int']['curid']
        else:
            sub = f"{min_} <= {sh.lg.globs['int']['curid']} <= {max_}"
            mes = _('Condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_warning()
    
    def sanitize(self, field):
        field = sh.lg.Text(field).delete_unsupported()
        field = sh.lg.Text(field).delete_duplicate_spaces()
        field = field.strip()
        field = self.decode(field)
        if not field:
            field = '?'
        return field
    
    def delete_album_trash(self, album):
        album = album.replace(' (@FLAC)', '').replace(' (@VBR)', '')
        album = album.replace(' (@vbr)', '').replace(', @FLAC', '')
        album = album.replace(',@FLAC', '').replace(', @VBR', '')
        album = album.replace(',@VBR', '').replace(', @vbr', '')
        album = album.replace(',@vbr', '')
        album = re.sub(' \(@\d+\)', '', album)
        album = re.sub(',[\s]{0,1}@\d+\)', '', album)
        return album
    
    def decode(self,text):
        try:
            byted = bytes(text, 'iso-8859-1')
            return byted.decode('cp1251')
        except:
            return text
    
    def decode_back(self, text):
        try:
            byted = bytes(text, 'cp1251')
            return byted.decode('utf-8')
        except:
            return text



objs = Objects()
com = Commands()
DefaultKeys()
objs.get_default()
objs.get_config()
com.restore_id()



if __name__ == '__main__':
    f = '[unmusic] logic.__main__'
    ibad = BadMusic()
    ibad.rates = [[1]]
    ibad.get_sizes()
    objs.get_db().close()
