#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import io
import re
import phrydy
import db

from config import CONFIG, PATHS

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

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
        ,'Slamming Brutal Death Metal', 'Technical Brutal Death Metal'
        ,'Technical Death Metal', 'Thrash Metal'
        )



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
        sh.objs.get_mes(f, mes, True).show_debug()
        mes = _('External collection: {}').format(self.exter)
        sh.objs.get_mes(f, mes, True).show_debug()
        mes = _('Mobile collection: {}').format(self.mobil)
        sh.objs.get_mes(f, mes, True).show_debug()
        if self.local and self.exter and self.mobil:
            return True
        else:
            self.Success = False
            mes = _('Empty output is not allowed!')
            sh.objs.get_mes(f, mes).show_warning()
    
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
                sh.objs.get_mes(f, mes).show_warning()
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
            iterable.append(self.rates[i] + [size])
        headers = ('ID','ALBUM','MIN','MAX','SIZE')
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,Transpose = True
                           ,maxrow = 70
                           ).run()
        sh.com.run_fast_debug(f, mes)
    
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
            sh.objs.get_mes(f, mes, True).show_debug()
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



class Objects:
    
    def __init__(self):
        self.default = self.db = self.image = None
        
    def get_db(self):
        f = '[unmusic] logic.Objects.get_db'
        if self.db is not None:
            return self.db
        self.db = db.DB(PATHS.get_db())
        return self.db



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
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes).show_warning()
    
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
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes).show_warning()
    
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
        sh.objs.get_mes(f, mes).show_info()
    
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
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes).show_warning()
    
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
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes).show_warning()
        return self.audio



class Walker:
    
    def __init__(self, path=''):
        if path:
            self.reset(path=path)
    
    def delete_empty(self):
        ''' Delete empty folders. Since 'sh.lg.Directory' instance is recreated
            each time, we can call this procedure at any time without the need
            to reset 'Walker'.
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
    
    def reset(self, path):
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
        if min_ <= CONFIG.new['cur_id'] <= max_:
            objs.db.albumid = CONFIG.new['cur_id']
        else:
            sub = f"{min_} <= {CONFIG.new['cur_id']} <= {max_}"
            mes = _('Condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f, mes).show_warning()
    
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
    
    def decode(self, text):
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
com.restore_id()



if __name__ == '__main__':
    f = '[unmusic] logic.__main__'
    ibad = BadMusic()
    ibad.rates = [[1]]
    ibad.get_sizes()
    objs.get_db().close()
