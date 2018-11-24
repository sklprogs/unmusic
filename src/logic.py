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
        self._path = path
        self.connect()
        self.create_albums()
        self.create_tracks()
    
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
                     ALBUMID   integer autoinc \
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
    
    def values(self):
        self.Success  = True
        self.audio    = None
        self._artist  = ''
        self._year    = 0
        self._album   = ''
        self._title   = ''
        self._lyrics  = ''
        self._bitrate = 0
        self._length  = 0
        self._no      = 0
    
    def summary(self):
        f = 'logic.Track.summary'
        if self.Success:
            mes =  _('Artist') + ': %s\n' % self._artist
            mes += _('Album') + ': %s\n' % self._album
            mes += _('Year') + ': %d\n' % self._year
            mes += _('Track #') + ': %d\n' % self._no
            mes += _('Title') + ': %s\n' % self._title
            if self._length:
                minutes = self._length // 60
                seconds = self._length - minutes * 60
            else:
                minutes = seconds = 0
            mes += _('Length') + ': %d ' % minutes + _('min') + ' %d ' \
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
                return re.sub('^\d+[\.]{0,1}[\s]{0,1}','',title)
        else:
            sh.com.cancel(f)
    
    def info(self):
        f = 'logic.Track.info'
        if self.Success:
            try:
                artist = [self.audio.artist,self.audio.albumartist
                         ,self.audio.composer
                         ]
                artist = [item for item in artist if item]
                if artist:
                    self._artist = artist[0]
                ''' Prevents from type mismatch (e.g., 'phrydy' returns
                    'None' in case a year is not set). If an input value
                    is empty then we do not overwrite a default value
                    which should be of a correct type. This does not
                    work as a separate procedure.
                '''
                if self.audio.album:
                    self._album = self.audio.album
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
            except Exception as e:
                sh.objs.mes (f,_('WARNING')
                            ,_('Third party module has failed!\n\nDetails: %s')\
                            % str(e)
                            )
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



objs = Objects()



if __name__ == '__main__':
    sg.objs.start()
    objs.default()
    objs.db()
    sg.objs.end()
