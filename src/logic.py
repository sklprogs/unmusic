#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import io
import re
import phrydy
import sqlite3

import shared    as sh
import sharedGUI as sg

PRODUCT = 'unmusic'
VERSION = '1.0'
# Derived from 'phrydy.mediafile.TYPES'
TYPES   = ['.mp3','.aac','.alac','.ogg','.opus','.flac','.ape','.wv'
          ,'.mpc','.asf','.aiff','.dsf'
          ]

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install(PRODUCT,'../resources/locale')



class Play:
    
    def __init__(self,External=False):
        self.values()
        self.Success  = objs.db().Success
        self.External = External
    
    def call_player(self):
        f = 'logic.Play.call_player'
        if self.Success:
            if self.playlist():
                sh.Launch(self._playlist).default()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success   = True
        self.External  = False
        self._collec   = ''
        self._album    = ''
        self._playlist = ''
        self._audio    = []
        self._nos      = []
        self._titles   = []
        self._len      = []
    
    def album(self):
        f = 'logic.Play.album'
        if self.Success:
            if not self._album:
                self._album = os.path.join (self.collection()
                                           ,str(objs.db().albumid)
                                           )
        else:
            sh.com.cancel(f)
        return self._album
    
    def collection(self):
        f = 'logic.Play.collection'
        if self.Success:
            if not self._collec:
                if self.External:
                    self._collec = sh.Home(app_name=PRODUCT).add_share(_('external collection'))
                else:
                    self._collec = sh.Home(app_name=PRODUCT).add_share(_('local collection'))
        else:
            sh.com.cancel(f)
        return self._collec
    
    def audio(self):
        f = 'logic.Play.audio'
        if self.Success:
            if not self._audio:
                idir = Directory(self.album())
                idir.create_list()
                self.Success = idir.Success
                if idir._audio:
                    self._audio = idir._audio
        else:
            sh.com.cancel(f)
        return self._audio
    
    def available(self):
        f = 'logic.Play.available'
        if self.Success:
            self.audio()
            if self._audio and self._nos:
                result = []
                errors = []
                for no in self._nos:
                    try:
                        result.append(self._audio[no])
                    except IndexError:
                        errors.append(no)
                if errors:
                    for no in errors:
                        del self._tracks[no]
                        del self._nos[no]
                        del self._len[no]
                    errors = [str(error) for error in errors]
                    sh.objs.mes (f,_('WARNING')
                                ,_('Tracks %s have not been found in "%s"!')\
                                % (', '.join(errors),self.album())
                                )
                return result
            else:
                sh.com.empty(f)
            if len(self._nos) == len(self._tracks) == len(self._len):
                pass
            else:
                self.Success= False
                sh.objs.mes (f,_('ERROR')
                            ,_('Condition "%s" is not observed!') \
                            % '%d == %d == %d' % (self._nos,self._tracks
                                                 ,self._len
                                                 )
                            )
        else:
            sh.com.cancel(f)
    
    def playlist(self):
        f = 'logic.Play.playlist'
        if self.Success:
            if not self._playlist:
                self._playlist = _('playlist') + '.m3u8'
                self._playlist = sh.Home(app_name=PRODUCT).add_share(self._playlist)
        else:
            sh.com.cancel(f)
        return self._playlist
    
    def gen_list(self):
        f = 'logic.Play.gen_list'
        if self.Success:
            if self._nos:
                self.out = io.StringIO()
                result   = objs.db().get_album()
                ''' Adding #EXTINF will allow to use tags in those
                    players that support it (e.g., clementine). This
                    entry should have the following format:
                    #EXTINF:191,Artist Name - Track Title
                    (multiple hyphens are not allowed).
                '''
                if result:
                    header = result[1] + ' (' + result[0] + ') - '
                else:
                    header = ''
                files    = self.available()
                if files and self._nos:
                    self.out.write('#EXTM3U\n')
                    for i in range(len(files)):
                        self.out.write('#EXTINF:')
                        self.out.write(str(int(self._len[i])))
                        self.out.write(',')
                        self.out.write(header)
                        self.out.write(self._titles[i])
                        self.out.write('\n')
                        self.out.write(files[i])
                        self.out.write('\n')
                else:
                    sh.com.empty(f)
                text = self.out.getvalue()
                self.out.close()
                if text:
                    sh.WriteTextFile (file       = self.playlist()
                                     ,AskRewrite = False
                                     ).write(text)
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def all_tracks(self):
        f = 'logic.Play.all_tracks'
        if self.Success:
            tracks = objs.db().tracks()
            if tracks:
                self._titles = [track[0] for track in tracks]
                self._len    = [track[5] for track in tracks]
                # '-1' since count starts with 1 in DB and we need 0
                self._nos = [track[1] - 1 for track in tracks]
                self.gen_list()
                self.call_player()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def best_tracks(self):
        f = 'logic.Play.best_tracks'
        if self.Success:
            tracks = objs.db().best_tracks()
            if tracks:
                if len(tracks[0]) == 4:
                    # '-1' since count starts with 1 in DB and we need 0
                    self._nos = [item[1] - 1 for item in tracks \
                                 if item[0] == tracks[0][0]
                                ]
                    self._titles = [item[2] for item in tracks \
                                    if item[0] == tracks[0][0]
                                   ]
                    self._len = [item[3] for item in tracks \
                                 if item[0] == tracks[0][0]
                                ]
                    self.gen_list()
                    self.call_player()
                else:
                    sh.objs.mes (f,_('ERROR')
                                ,_('Wrong input data!')
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)



class AlbumEditor:
    
    def __init__(self):
        self.Success = True
    
    def mean_bitrate(self):
        f = 'logic.AlbumEditor.mean_bitrate'
        if self.Success:
            mean = objs.db().get_bitrate()
            if mean:
                mean = [rating for rating in mean if rating]
                if mean:
                    # Return 'int' since we don't need 'float' here
                    return sum(mean) // len(mean)
                else:
                    return 0
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def mean_rating(self):
        f = 'logic.AlbumEditor.mean_rating'
        if self.Success:
            mean = objs.db().get_rating()
            if mean:
                ''' We should not count tracks with an undefined (0)
                    rating, otherwise, if there is a mix of tracks with
                    zero and non-zero rating, an overall rating will be
                    lower than a mean rating of the non-zero rating
                    tracks.
                '''
                mean = [rating for rating in mean if rating]
                if mean:
                    ''' This (intentionally) returns float even if all
                        elements are equal.
                    '''
                    return sum(mean) / len(mean)
                else:
                    return 0.0
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def get_no(self):
        f = 'logic.AlbumEditor.get_no'
        if self.Success:
            objs.db().albumid = sh.Input (title = f
                                         ,value = objs.db().albumid
                                         ).integer()
        else:
            sh.com.cancel(f)
        return objs.db().albumid
    
    def get_min(self):
        f = 'logic.AlbumEditor.get_min'
        if self.Success:
            return sh.Input (title = f
                            ,value = objs.db().min_id()
                            ).integer()
        else:
            sh.com.cancel(f)
            return 0
    
    def get_max(self):
        f = 'logic.AlbumEditor.get_max'
        if self.Success:
            _max = objs.db().max_id()
            if isinstance(_max,int):
                return _max
            else:
                sh.objs.mes (f,_('WARNING')
                            ,_('The database is empty. You need to fill it first.')
                            )
                return 0
        else:
            sh.com.cancel(f)
            return 0
    
    def inc(self):
        f = 'logic.AlbumEditor.inc'
        if self.Success:
            if self.get_no() == self.get_max():
                objs.db().albumid = self.get_min()
            else:
                objs.db().albumid = objs.db().next_id()
                self.get_no()
        else:
            sh.com.cancel(f)
    
    def dec(self):
        f = 'logic.AlbumEditor.dec'
        if self.Success:
            if self.get_no() == self.get_min():
                objs.db().albumid = self.get_max()
            else:
                objs.db().albumid = objs.db().prev_id()
                self.get_no()
        else:
            sh.com.cancel(f)

    def _compare_albums(self,old,new):
        f = 'logic.AlbumEditor.compare_albums'
        # Quotes in the text will fail the query, so we screen them
        new[0] = str(new[0]).replace('"','""')
        new[1] = str(new[1]).replace('"','""')
        new[3] = str(new[3]).replace('"','""')
        new[4] = str(new[4]).replace('"','""')
        new[5] = str(new[5]).replace('"','""')
        search = [new[0],new[1],str(new[2]),new[3],new[4],new[5]]
        search = ' '.join(search)
        search = sh.Text(search).delete_duplicate_spaces()
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
                add.append(base % new[i])
        if add:
            add.append('SEARCH="%s"' % search)
            add = 'begin;update ALBUMS set ' + ','.join(add)
            add += ' where ALBUMID=%d;commit;' % objs.db().albumid
            return add



class Directory:
    
    def __init__(self,path,Obfuscate=True):
        if path:
            self.reset (path      = path
                       ,Obfuscate = Obfuscate
                       )
    
    def _set_no(self,i,max_len):
        no = str(i+1)
        while len(no) < max_len:
            no = '0' + no
        return no
    
    def move_tracks(self):
        f = 'logic.Directory.move_tracks'
        if self.Success:
            success = []
            ''' The current algorithm of tracks renumbering guarantees
                that the file list (*unless changed*) will have
                a consecutive numbering of tracks.
            '''
            max_len = len(self._audio)
            max_len = len(str(max_len))
            for i in range(len(self._audio)):
                file     = self._audio[i]
                no       = self._set_no(i,max_len)
                basename = no + sh.Path(file).extension().lower()
                dest     = os.path.join (self._target
                                        ,basename
                                        )
                success.append(sh.File(file=file,dest=dest).move())
            self.Success = not (False in success or None in success)
        else:
            sh.com.cancel(f)
    
    def purge(self):
        f = 'logic.Directory.purge'
        if self.Success:
            if self._tracks:
                sh.log.append (f,_('INFO')
                              ,_('Purge tracks')
                              )
                for track in self._tracks:
                    track.purge()
                    track.save()
                    if not track.Success:
                        self.Success = False
                        break
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def create_target(self):
        f = 'logic.Directory.create_target'
        if self.Success:
            if objs.db().albumid:
                self._target = sh.Home(app_name=PRODUCT).add_share (_('processed')
                                                                   ,str(objs._db.albumid)
                                                                   )
                self.Success = sh.Path(self._target).create()
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def reset(self,path,Obfuscate=True):
        self.values()
        self._path     = path
        self.Obfuscate = Obfuscate
        self.idir      = sh.Directory(self._path)
        self.Success   = self.idir.Success
        
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
        self.renumber_tracks()
        self.save_meta()
        if self.Obfuscate:
            self.create_target()
            self.purge()
            self.move_tracks()
        return self.Success
    
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
                objs.db().albumid = albumid
                if not objs._db.has_track (no      = data[1]
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
        self.Success = True
        self._path   = ''
        self._target = ''
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
                    in TYPES:
                        self._audio.append(file)
            return self._files
        else:
            sh.com.cancel(f)
    
    def renumber_tracks(self):
        ''' We use track NO field instead of an autoincrement, so we
            must keep these fields unique within the same album.
        '''
        f = 'logic.Directory.renumber_tracks'
        if self.Success:
            nos = [i + 1 for i in range(len(self._tracks))]
            count = 0
            for i in range(len(self._tracks)):
                if self._tracks[i]._no != nos[i]:
                    count += 1
                    self._tracks[i]._no = nos[i]
            if count:
                sh.log.append (f,_('WARNING')
                              ,_('%d/%d tracks have been renumbered.') \
                              % (count,len(self._tracks))
                              )
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
        self.albumid = 1
        self._path   = path
        self.connect()
        self.create_albums()
        self.create_tracks()
    
    def best_tracks(self):
        f = 'logic.DB.best_tracks'
        if self.Success:
            try:
                self.dbc.execute ('select RATING,NO,TITLE,LENGTH \
                                   from TRACKS where ALBUMID = ? \
                                   order by RATING desc,NO'
                                  ,(self.albumid,)
                                 )
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def update_track(self,no,data):
        f = 'logic.DB.update_track'
        if self.Success:
            if no and data:
                if len(data) == 4:
                    try:
                        self.dbc.execute ('update TRACKS set TITLE = ?\
                                                 ,LYRICS = ?,COMMENT = ?\
                                                 ,RATING = ? \
                                           where ALBUMID = ? and NO = ?'
                                          ,(data[0],data[1],data[2]
                                           ,data[3],self.albumid,no
                                           )
                                         )
                    except Exception as e:
                        self.fail(f,e)
                else:
                    sh.objs.mes (f,_('ERROR')
                                ,_('Condition "%s" is not observed!') \
                                % '%d == %d' % (len(data),4)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def check_nos(self):
        ''' We use track NO field instead of an autoincrement, so we
            must keep these fields unique within the same album.
            Tracks should have already been renumbered if required
            with 'logic.Directory.renumber_tracks', however, we check
            this again just to be sure.
        '''
        f = 'logic.DB.check_nos'
        if self.Success:
            try:
                self.dbc.execute ('select NO from TRACKS \
                                   where ALBUMID = ? order by NO'
                                  ,(self.albumid,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    result = [item[0] for item in result]
                    nos    = [i + 1 for i in range(len(result))]
                    return result == nos
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_length(self):
        f = 'logic.DB.get_length'
        if self.Success:
            try:
                self.dbc.execute ('select LENGTH from TRACKS \
                                   where ALBUMID = ? order by NO'
                                  ,(self.albumid,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_bitrate(self):
        f = 'logic.DB.get_bitrate'
        if self.Success:
            try:
                self.dbc.execute ('select BITRATE from TRACKS \
                                   where ALBUMID = ? order by NO'
                                  ,(self.albumid,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def delete(self):
        f = 'logic.DB.delete'
        if self.Success:
            try:
                self.dbc.execute ('delete from ALBUMS where ALBUMID = ?'
                                 ,(self.albumid,)
                                 )
                self.dbc.execute ('delete from TRACKS where ALBUMID = ?'
                                 ,(self.albumid,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_rating(self):
        f = 'logic.DB.get_rating'
        if self.Success:
            try:
                self.dbc.execute ('select RATING from TRACKS \
                                   where ALBUMID = ? order by NO'
                                  ,(self.albumid,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def set_rating(self,value):
        f = 'logic.DB.set_rating'
        if self.Success:
            try:
                self.dbc.execute ('update TRACKS set RATING = ? \
                                   where ALBUMID = ?'
                                  ,(value,self.albumid,)
                                 )
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def updateDB(self,query):
        f = 'logic.DB.updateDB'
        if self.Success:
            if query:
                try:
                    self.dbc.executescript(query)
                except Exception as e:
                    sh.objs.mes (f,_('ERROR')
                                ,_('Unable to execute:\n"%s"\n\nDetails: %s')\
                                % (str(query).replace(';',';\n'),str(e))
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def tracks(self):
        f = 'logic.DB.tracks'
        if self.Success:
            try:
                self.dbc.execute ('select   TITLE,NO,LYRICS,COMMENT \
                                           ,BITRATE,LENGTH,RATING \
                                   from     TRACKS where ALBUMID = ? \
                                   order by NO',(self.albumid,)
                                 )
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def search_track(self,search):
        f = 'logic.DB.search_track'
        if self.Success:
            if search:
                search = '%' + search.lower() + '%'
                try:
                    self.dbc.execute ('select   ALBUMID,TITLE,NO,LYRICS\
                                               ,COMMENT,BITRATE,LENGTH\
                                               ,RATING from TRACKS \
                                       where    SEARCH like ? \
                                       order by ALBUMID,NO'
                                      ,(search,)
                                     )
                    return self.dbc.fetchall()
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def next_album(self,search):
        f = 'logic.DB.next_album'
        if self.Success:
            if search:
                search = '%' + search.lower() + '%'
                try:
                    self.dbc.execute ('select   ALBUMID from ALBUMS \
                                       where    ALBUMID > ? \
                                       and      SEARCH like ? \
                                       order by ALBUMID'
                                      ,(self.albumid,search,)
                                     )
                    result = self.dbc.fetchone()
                    if result:
                        return result[0]
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def prev_album(self,search):
        f = 'logic.DB.prev_album'
        if self.Success:
            if search:
                search = '%' + search.lower() + '%'
                try:
                    self.dbc.execute ('select   ALBUMID from ALBUMS \
                                       where    ALBUMID < ? \
                                       and      SEARCH like ? \
                                       order by ALBUMID desc'
                                      ,(self.albumid,search,)
                                     )
                    result = self.dbc.fetchone()
                    if result:
                        return result[0]
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def prev_id(self):
        f = 'logic.DB.prev_id'
        if self.Success:
            try:
                self.dbc.execute ('select   ALBUMID from ALBUMS \
                                   where    ALBUMID < ? \
                                   order by ALBUMID desc'
                                  ,(self.albumid,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def next_id(self):
        f = 'logic.DB.next_id'
        if self.Success:
            try:
                self.dbc.execute ('select ALBUMID from ALBUMS \
                                   where  ALBUMID > ? order by ALBUMID'
                                  ,(self.albumid,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_album(self):
        f = 'logic.DB.get_album'
        if self.Success:
            try:
                self.dbc.execute ('select ALBUM,ARTIST,YEAR,GENRE\
                                         ,COUNTRY,COMMENT from ALBUMS \
                                   where  ALBUMID = ?',(self.albumid,)
                                 )
                return self.dbc.fetchone()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def min_id(self):
        f = 'logic.DB.min_id'
        if self.Success:
            try:
                ''' 'self.dbc.lastrowid' returns 'None' if an album is
                    already in DB.
                '''
                self.dbc.execute ('select   ALBUMID from ALBUMS \
                                   order by ALBUMID'
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
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
                self.dbc.execute ('select   ALBUMID from ALBUMS \
                                   order by ALBUMID desc'
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def has_track(self,no,bitrate):
        ''' Since tags may be missing, we use a track number to identify
            a track. Different bitrates refer to different tracks.
        '''
        f = 'logic.DB.has_track'
        if self.Success:
            try:
                self.dbc.execute ('select TITLE from TRACKS \
                                   where  ALBUMID = ? and NO = ? \
                                   and    BITRATE = ?'
                                  ,(self.albumid,no,bitrate,)
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
        self.decode()
    
    def purge(self):
        f = 'logic.Track.purge'
        if self.Success:
            if self.audio:
                try:
                    self.audio.delete()
                    self.audio.images = {}
                except Exception as e:
                    self.Success = False
                    sh.objs.mes (f,_('WARNING')
                                ,_('Third-party module has failed!\n\nDetails: %s')\
                                % str(e)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def save(self):
        ''' This is only needed if the file was changed by means of
            'phrydy', see, for example, 'self.purge'.
        '''
        f = 'logic.Track.save'
        if self.Success:
            if self.audio:
                try:
                    self.audio.save()
                except Exception as e:
                    self.Success = False
                    sh.objs.mes (f,_('WARNING')
                                ,_('Third-party module has failed!\n\nDetails: %s')\
                                % str(e)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def _decode(self,text):
        try:
            byted = bytes(text,'iso-8859-1')
            return byted.decode('cp1251')
        except UnicodeEncodeError:
            return text
    
    # Fix Cyrillic tags
    def decode(self):
        f = 'logic.Track.decode'
        if self.Success:
            self._artist = self._decode(self._artist)
            self._album  = self._decode(self._album)
            self._title  = self._decode(self._title)
            self._lyrics = self._decode(self._lyrics)
        else:
            sh.com.cancel(f)
    
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
            if not self._album:
                self._album = '?'
            if not self._artist:
                self._artist = '?'
            if not self._genre:
                self._genre = '?'
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
                                ,_('Third-party module has failed!\n\nDetails: %s')\
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
                                ,_('Third-party module has failed!\n\nDetails: %s')\
                                % str(e)
                                )
            return self.audio
        else:
            sh.com.cancel(f)



class Walker:
    
    def __init__(self,path=''):
        if path:
            self.reset(path=path)
    
    def delete_empty(self):
        ''' Delete empty folders. Since 'sh.Directory' instance is
            recreated each time, we can call this procedure at any time
            without the need to reset 'Walker'.
        '''
        f = 'logic.Walker.delete_empty'
        self.dirs()
        if self.Success:
            if self._all_dirs:
                for folder in self._all_dirs:
                    sh.Directory(folder).delete_empty()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
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
                self._all_dirs = list(self._dirs)
                self._dirs = [folder for folder in self._dirs \
                              if not self._embedded(folder)
                             ]
            return self._dirs
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success   = True
        self._path     = ''
        # Folders containing audio files
        self._dirs     = []
        # All folders (including empty ones)
        self._all_dirs = []



objs = Objects()
objs.default()



if __name__ == '__main__':
    sh.objs.mes(Silent=1)
    objs.db().albumid = 7
    Play().best_tracks()
    objs._db.close()
