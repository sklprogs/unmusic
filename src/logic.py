#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re
import phrydy
import sqlite3

import shared    as sh
import sharedGUI as sg

PRODUCT = 'unmusic'
VERSION = '1.0'

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install(PRODUCT,'../resources/locale')



class Directory:
    
    def __init__(self,path,rating=0):
        if path:
            self.reset (path   = path
                       ,rating = rating
                       )
    
    def reset(self,path,rating=0):
        self.values()
        self._path   = path
        self.idir    = sh.Directory(self._path)
        self.Success = self.idir.Success
        self._rating = rating
        
    def get_rating(self):
        f = 'logic.Directory.get_rating'
        if self.Success:
            match = re.search(r'\(rating (\d+)\)',self._path)
            if match:
                try:
                    rating = match.group(1)
                    if rating.isdigit():
                        self._rating = int(rating)
                except IndexError:
                    pass
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.get_rating()
        self.create_list()
        self.tracks()
        self.save_meta()
    
    def _add_album_meta(self):
        f = 'logic.Directory._add_album_meta'
        data = self._tracks[0].album_meta()
        ''' If a track could not be processed, empty tags will be
            returned, which, when written to DB, can cause confusion.
            Here we check that the track was processed successfully.
        '''
        if self._tracks[0].audio and data:
            objs._db.add_album ([data[0],data[1],data[2],data[3],'',''
                                ,data[4]
                                ]
                               )
        else:
            sh.com.empty(f)
    
    def _add_tracks_meta(self,albumid):
        f = 'logic.Directory._add_tracks_meta'
        for track in self._tracks:
            data = track.track_meta()
            ''' If a track could not be processed, empty tags will be
                returned, which, when written to DB, can cause
                confusion. Here we check that the track was processed
                successfully.
            '''
            if track.audio and data:
                if not objs._db.has_track (albumid = albumid
                                          ,no      = data[1]
                                          ,bitrate = data[4]
                                          ):
                    self._new += 1
                    objs._db.add_track ([albumid,data[0],data[1],data[2]
                                        ,'',data[3],data[4],data[5]
                                        ,self._rating
                                        ]
                                       )
            else:
                sh.com.empty(f)
    
    def save_meta(self):
        f = 'logic.Directory.save_meta'
        if self.Success:
            if self._tracks:
                # Albums of the same bitrate will share the same ID
                albumid = objs.db().has_album (artist = self._tracks[0]._artist
                                              ,year   = self._tracks[0]._year
                                              ,album  = self._tracks[0]._album
                                              )
                if albumid:
                    sh.log.append (f,_('INFO')
                                  ,_('Album %s is already in DB!') \
                                  % str(albumid)
                                  )
                else:
                    self._add_album_meta()
                    albumid = objs._db.max_id()
                if albumid:
                    self._add_tracks_meta(albumid)
                    if self._new:
                        sh.log.append (f,_('INFO')
                                      ,_('Album %d: %d new tracks.') \
                                      % (albumid,self._new)
                                      )
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def values(self):
        # Derived from 'phrydy.mediafile.TYPES'
        self._supported   = ['.mp3','.aac','.alac','.ogg','.opus'
                            ,'.flac','.ape','.wv','.mpc','.asf','.aiff'
                            ,'.dsf'
                            ]
        self.Success = True
        self._path   = ''
        self._rating = 0
        self._new    = 0
        self._files  = []
        self._audio  = []
        self._tracks = []
    
    def create_list(self):
        f = 'logic.Directory.create_list'
        if self.Success:
            if not self._files:
                self._files = self.idir.files()
                for file in self._files:
                    if sh.Path(file).extension().lower() \
                    in self._supported:
                        self._audio.append(file)
            return self._files
        else:
            sh.com.cancel(f)
    
    def tracks(self):
        f = 'logic.Directory.tracks'
        if self.Success:
            if not self._tracks:
                if self._audio:
                    for file in self._audio:
                        self._tracks.append(Track(file))
                else:
                    sh.log.append (f,_('INFO')
                                  ,_('Nothing to do!')
                                  )
            return self._tracks
        else:
            sh.com.cancel(f)



class DefaultConfig:
    
    def __init__(self):
        self.values()
        self.ihome   = sh.Home(app_name=PRODUCT)
        self.Success = self.ihome.create_conf()
    
    def run(self):
        self.db()
    
    def values(self):
        self._fdb = ''
    
    def db(self):
        f = 'logic.DefaultConfig.db'
        if self.Success:
            self._fdb = self.ihome.add_config(PRODUCT+'.db')
            if self._fdb:
                if os.path.exists(self._fdb):
                    self.Success = sh.File(file=self._fdb).Success
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)



class Objects:
    
    def __init__(self):
        self._default = self._db = None
        
    def db(self):
        f = 'logic.Objects.db'
        if not self._db:
            path = self.default()._fdb
            if self._default.Success:
                self._db = DB(path=path)
            else:
                sh.log.append (f,_('WARNING')
                              ,_('Wrong input data!')
                              )
                self._db = DB()
        return self._db
    
    def default(self):
        if not self._default:
            self._default = DefaultConfig()
            self._default.run()
        return self._default



class DB:
    
    def __init__(self,path):
        self.Success = True
        self._path   = path
        self.connect()
        self.create_albums()
        self.create_tracks()
    
    def get_album(self,albumid):
        f = 'logic.DB.get_album'
        if self.Success:
            try:
                self.dbc.execute ('select ALBUM,ARTIST,YEAR,GENRE\
                                         ,COUNTRY,COMMENT from ALBUMS \
                                   where  ALBUMID = ?',(albumid,)
                                 )
                return self.dbc.fetchone()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def max_id(self):
        f = 'logic.DB.max_id'
        if self.Success:
            try:
                ''' 'self.dbc.lastrowid' returns 'None' if an album is
                    already in DB.
                '''
                self.dbc.execute ('select ALBUMID from ALBUMS \
                                   order by ALBUMID desc'
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def has_track(self,albumid,no,bitrate):
        ''' Since tags may be missing, we use a track number to identify
            a track. Different bitrates refer to different tracks.
        '''
        f = 'logic.DB.has_track'
        if self.Success:
            try:
                self.dbc.execute ('select TITLE from TRACKS \
                                   where ALBUMID = ? and NO = ? \
                                   and BITRATE = ?'
                                  ,(albumid,no,bitrate,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def has_album(self,artist,year,album):
        f = 'logic.DB.has_album'
        if self.Success:
            try:
                self.dbc.execute ('select ALBUMID from ALBUMS \
                                   where  ARTIST = ? and YEAR = ? \
                                   and    ALBUM = ?'
                                   ,(artist,year,album,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def print (self,Selected=False,Shorten=False
              ,MaxRow=20,MaxRows=20,table='TRACKS'
              ):
        f = 'logic.DB.print'
        if self.Success:
            ''' 'self.dbc.description' is 'None' without performing 
                'select' first
             '''
            if not Selected:
                self.dbc.execute('select * from %s' % table)
            headers = [cn[0] for cn in self.dbc.description]
            rows    = self.dbc.fetchall()
            sh.Table (headers = headers
                     ,rows    = rows
                     ,Shorten = Shorten
                     ,MaxRow  = MaxRow
                     ,MaxRows = MaxRows
                     ).print()
        else:
            sh.com.cancel(f)
    
    def add_track(self,data):
        f = 'logic.DB.add_track'
        if self.Success:
            if data:
                try:
                    self.dbc.execute ('insert into TRACKS values \
                                       (?,?,?,?,?,?,?,?,?)',data
                                     )
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def add_album(self,data):
        f = 'logic.DB.add_album'
        if self.Success:
            if data:
                try:
                    self.dbc.execute ('insert into ALBUMS values \
                                       (NULL,?,?,?,?,?,?,?)',data
                                     )
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def create_tracks(self):
        f = 'logic.DB.create_tracks'
        if self.Success:
            try:
                # 9 columns by now
                self.dbc.execute (
                    'create table if not exists TRACKS (\
                     ALBUMID   integer \
                    ,TITLE     text    \
                    ,NO        integer \
                    ,LYRICS    text    \
                    ,COMMENT   text    \
                    ,SEARCH    text    \
                    ,BITRATE   integer \
                    ,LENGTH    integer \
                    ,RATING    integer \
                                                       )'
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_albums(self):
        f = 'logic.DB.create_albums'
        if self.Success:
            try:
                # 8 columns by now
                self.dbc.execute (
                    'create table if not exists ALBUMS (\
                     ALBUMID   integer primary key autoincrement \
                    ,ALBUM     text    \
                    ,ARTIST    text    \
                    ,YEAR      integer \
                    ,GENRE     text    \
                    ,COUNTRY   text    \
                    ,COMMENT   text    \
                    ,SEARCH    text    \
                                                       )'
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def save(self):
        f = 'logic.DB.save'
        if self.Success:
            sh.log.append (f,_('INFO')
                          ,_('Save "%s"') % self._path
                          )
            try:
                self.db.commit()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def fail(self,func,error):
        self.Success = False
        sh.objs.mes (func
                    ,_('WARNING')
                    ,_('Database "%s" has failed!\n\nDetails: %s') \
                    % (self._path,str(error))
                    )
    
    def close(self):
        f = 'logic.DB.close'
        if self.Success:
            try:
                self.dbc.close()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def connect(self):
        f = 'logic.DB.connect'
        if self.Success:
            try:
                self.db  = sqlite3.connect(self._path)
                self.dbc = self.db.cursor()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)



class Track:
    
    def __init__(self,file):
        self.values()
        self.file    = file
        self.Success = sh.File(self.file).Success
        self.load()
        self.info()
    
    def track_meta(self):
        f = 'logic.Track.track_meta'
        if self.Success:
            search = [self._title,self._lyrics]
            search = ' '.join(search)
            search = sh.Text(search).delete_duplicate_spaces()
            search = search.strip().lower()
            return (self._title,self._no,self._lyrics,search
                   ,self._bitrate,self._length
                   )
        else:
            sh.com.cancel(f)
    
    def album_meta(self):
        f = 'logic.Track.album_meta'
        if self.Success:
            search = [self._album,self._artist,str(self._year)
                     ,self._genre
                     ]
            search = ' '.join(search)
            search = sh.Text(search).delete_duplicate_spaces()
            search = search.strip().lower()
            return (self._album,self._artist,self._year,self._genre
                   ,search
                   )
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success  = True
        self.audio    = None
        self._artist  = ''
        self._album   = ''
        self._title   = ''
        self._lyrics  = ''
        self._genre   = ''
        self._year    = 0
        self._bitrate = 0
        self._length  = 0
        self._no      = 1
    
    def summary(self):
        f = 'logic.Track.summary'
        if self.Success:
            mes =  _('Artist:')  + ' %s\n' % self._artist
            mes += _('Album:')   + ' %s\n' % self._album
            mes += _('Genre:')   + ' %s\n' % self._genre
            mes += _('Year:')    + ' %d\n' % self._year
            mes += _('Track #:') + ' %d\n' % self._no
            mes += _('Title:')   + ' %s\n' % self._title
            mes += _('Lyrics:')  + ' %s\n' % self._lyrics
            if self._length:
                minutes = self._length // 60
                seconds = self._length - minutes * 60
            else:
                minutes = seconds = 0
            mes += _('Length:') + ' %d ' % minutes + _('min') + ' %d ' \
                   % seconds + _('sec') + '\n'
            sh.objs.mes (f,_('INFO')
                        ,mes
                        )
        else:
            sh.com.cancel(f)
    
    def extract_title(self):
        f = 'logic.Track.extract_title'
        if self.Success:
            title = sh.Path(self.file).filename()
            if title:
                result = re.sub('^\d+[\.]{0,1}[\s]{0,1}','',title)
                if result:
                    return result
                else:
                    # If a title is just a digit + an extension.
                    return title
        else:
            sh.com.cancel(f)
    
    def info(self):
        f = 'logic.Track.info'
        if self.Success:
            if self.audio:
                try:
                    artist = [self.audio.artist,self.audio.albumartist
                             ,self.audio.composer
                             ]
                    artist = [item for item in artist if item]
                    if artist:
                        self._artist = artist[0]
                    ''' Prevents from type mismatch (e.g., 'phrydy'
                        returns 'None' in case a year is not set).
                        If an input value is empty then we do not
                        overwrite a default value which should be of
                        a correct type. This does not work as
                        a separate procedure.
                    '''
                    if self.audio.album:
                        self._album = self.audio.album
                    else:
                        dirname = sh.Path(self.file).dirname()
                        dirname = sh.Path(dirname).basename()
                        self._album = '[[' + dirname + ']]'
                    if self.audio.genre:
                        self._genre = self.audio.genre
                    if self.audio.year:
                        self._year = self.audio.year
                    if self.audio.title:
                        self._title = self.audio.title
                    else:
                        extracted = self.extract_title()
                        if extracted:
                            self._title = extracted
                    if self.audio.bitrate:
                        self._bitrate = self.audio.bitrate
                    if self.audio.length:
                        self._length = self.audio.length
                    if str(self.audio.track).isdigit():
                        self._no = self.audio.track
                    if self.audio.lyrics:
                        self._lyrics = self.audio.lyrics
                except Exception as e:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Third party module has failed!\n\nDetails: %s')\
                                % str(e)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = 'logic.Track.load'
        if self.Success:
            if not self.audio:
                try:
                    self.audio = phrydy.MediaFile(self.file)
                except Exception as e:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Third party module has failed!\n\nDetails: %s')\
                                % str(e)
                                )
            return self.audio
        else:
            sh.com.cancel(f)



class Walker:
    
    def __init__(self,path=''):
        if path:
            self.reset(path=path)
    
    def reset(self,path):
        self.values()
        self._path   = path
        self.idir    = sh.Directory(self._path)
        self.Success = self.idir.Success
    
    def _embedded(self,folder):
        return [item for item in self._dirs \
                if folder in item and folder != item
               ]
    
    def dirs(self):
        f = 'logic.Walker.dirs'
        if self.Success:
            if not self._dirs:
                for dirpath, dirnames, filenames \
                in os.walk(self.idir.dir):
                    if not dirpath in self._dirs:
                        self._dirs.append(dirpath)
                self._dirs = [folder for folder in self._dirs \
                              if not self._embedded(folder)
                             ]
            return self._dirs
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success = True
        self._path   = ''
        self._dirs   = []



objs = Objects()
objs.default()



if __name__ == '__main__':
    sg.objs.start()
    f = 'logic.__main__'
    dirs = Walker('/tmp/meta').dirs()
    if dirs:
        timer = sh.Timer(f)
        timer.start()
        for folder in dirs:
            Directory(path=folder).run()
        timer.end()
        objs.db().save()
        print('Max ID:',objs.db().max_id())
        objs.db().print (table   = 'ALBUMS'
                        ,Shorten = True
                        ,MaxRow  = 40
                        ,MaxRows = 200
                        )
        objs._db.print (table   = 'TRACKS'
                       ,Shorten = True
                       ,MaxRow  = 40
                       ,MaxRows = 200
                       )
    else:
        sh.com.empty(f)
    sg.objs.end()
