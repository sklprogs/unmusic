#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import phrydy

import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('shared','./shared/resources/locale')


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
                title = re.sub('^\d+[\.]{0,1}[\s]{0,1}','',title)
            if title:
                return title
            else:
                return '?'
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
                    self._title = self.extract_title()
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



if __name__ == '__main__':
    sg.objs.start()
    Track('/tmp/test.mp3').summary()
    sg.objs.end()
