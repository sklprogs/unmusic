#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import sys

import skl_shared.shared as sh
from skl_shared.localize import _


class DB:
    
    def __init__(self,path):
        self.Success = True
        self.albumid = 1
        self.path = path
        self.connect()
        self.create_albums()
        self.create_tracks()
    
    def get_albums(self,limit=0):
        f = '[unmusic] db.DB.get_albums'
        if self.Success:
            query = 'select ALBUMID,ALBUM,ARTIST,YEAR from ALBUMS \
                     order by ALBUMID'
            if limit:
                query += ' limit ?'
            try:
                # limit=0 provides an empty ouput
                if limit:
                    self.dbc.execute(query,(limit,))
                else:
                    self.dbc.execute(query)
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_rates(self):
        ''' When operating on entire albums (e.g., deleting bad music),
            we need to know minimum and maximum ratings
            (e.g., 0 < album rate < 5 for ALL tracks of bad albums).
        '''
        f = '[unmusic] db.DB.get_rates'
        if self.Success:
            query = 'select RATING from TRACKS where ALBUMID = ? \
                     order by NO'
            try:
                self.dbc.execute(query,(self.albumid,))
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_prev_rated(self,rating=0,albumid=None):
        f = '[unmusic] db.DB.get_prev_rated'
        if self.Success:
            if albumid is None:
                albumid = self.albumid
            query = 'select ALBUMID from TRACKS where ALBUMID < ? \
                     and RATING = ? order by ALBUMID desc'
            try:
                self.dbc.execute(query,(albumid,rating,))
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_next_rated(self,rating=0,albumid=None):
        f = '[unmusic] db.DB.get_next_rated'
        if self.Success:
            if albumid is None:
                albumid = self.albumid
            query = 'select ALBUMID from TRACKS where ALBUMID > ? \
                     and RATING = ? order by ALBUMID'
            try:
                self.dbc.execute(query,(albumid,rating,))
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_brief(self,ids):
        f = '[unmusic] db.DB.get_brief'
        if self.Success:
            if ids:
                ''' Sometimes ARTIST + YEAR + ALBUM combinations are
                    identical, e.g., there are several CDs for the same
                    album or there are identical albums of a different
                    quality. This leads to identical IDs at
                    'unmusic.Copy.select_albums'. To avoid this, we add
                    ALBUMID.
                '''
                query = 'select ALBUMID,ARTIST,YEAR,ALBUM from ALBUMS \
                         where ALBUMID in ({})'
                query = query.format(','.join('?'*len(ids)))
                try:
                    self.dbc.execute(query,ids)
                    result = self.dbc.fetchall()
                    if result:
                        lst = [str(item[0]) + ': ' + ' - '.join ([item[1]
                                                                 ,str(item[2])
                                                                 ,item[3]
                                                                 ]
                                                                )\
                               for item in result
                              ]
                        return '\n'.join(lst)
                        
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_unknown_genre(self,limit=0):
        f = '[unmusic] db.DB.get_unknown_genre'
        if self.Success:
            query1 = 'select ALBUMID from ALBUMS where GENRE = ? \
                      limit ? order by ALBUMID'
            query2 = 'select ALBUMID from ALBUMS where GENRE = ? \
                      order by ALBUMID'
            try:
                if limit:
                    self.dbc.execute(query1,('?',limit,))
                else:
                    self.dbc.execute(query2,('?',))
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_rated(self,rating=0,limit=0):
        f = '[unmusic] db.DB.get_unrated'
        if self.Success:
            query = 'select distinct ALBUMID from TRACKS \
                     where RATING = ?'
            if limit:
                query += ' limit ?'
            try:
                if limit:
                    self.dbc.execute(query,(rating,limit,))
                else:
                    self.dbc.execute(query,(rating,))
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_good_tracks(self,rating=8):
        f = '[unmusic] db.DB.get_good_tracks'
        if self.Success:
            query = 'select TITLE,NO,LYRICS,COMMENT,BITRATE,LENGTH \
                    ,RATING from TRACKS where ALBUMID = ? \
                     and RATING >= ? order by NO'
            try:
                self.dbc.execute(query,(self.albumid,rating,))
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def has_id(self,albumid):
        ''' A major difference from 'get_album': we do not need
            to assign 'self.albumid' to establish whether the input is
            valid or not.
        '''
        f = '[unmusic] db.DB.has_id'
        if self.Success:
            query = 'select ALBUMID from ALBUMS where ALBUMID = ?'
            try:
                self.dbc.execute(query,(albumid,))
                return self.dbc.fetchone()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def update_track(self,no,data):
        f = '[unmusic] db.DB.update_track'
        if self.Success:
            if no and data:
                if len(data) == 4:
                    query = 'update TRACKS set TITLE = ?,LYRICS = ? \
                            ,COMMENT = ?,RATING = ? where ALBUMID = ? \
                             and NO = ?'
                    try:
                        self.dbc.execute (query,(data[0],data[1],data[2]
                                                ,data[3],self.albumid,no
                                                )
                                         )
                    except Exception as e:
                        self.fail(f,e)
                else:
                    sub = '{} = {}'.format(len(data),4)
                    mes = _('Condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.get_mes(f,mes).show_error()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def check_nos(self):
        ''' We use track NO field instead of an autoincrement, so we
            must keep these fields unique within the same album.
            Tracks should have already been renumbered if required
            with 'unmusic.logic.Directory.renumber_tracks', however, we check
            this again just to be sure.
        '''
        f = '[unmusic] db.DB.check_nos'
        if self.Success:
            query = 'select NO from TRACKS where ALBUMID = ? \
                     order by NO'
            try:
                self.dbc.execute(query,(self.albumid,))
                result = self.dbc.fetchall()
                if result:
                    result = [item[0] for item in result]
                    nos = [i + 1 for i in range(len(result))]
                    return result == nos
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_length(self):
        f = '[unmusic] db.DB.get_length'
        if self.Success:
            query = 'select LENGTH from TRACKS where ALBUMID = ? \
                     order by NO'
            try:
                self.dbc.execute(query,(self.albumid,))
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_bitrate(self):
        f = '[unmusic] db.DB.get_bitrate'
        if self.Success:
            query = 'select BITRATE from TRACKS where ALBUMID = ? \
                     order by NO'
            try:
                self.dbc.execute(query,(self.albumid,))
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def delete(self):
        f = '[unmusic] db.DB.delete'
        if self.Success:
            query1 = 'delete from ALBUMS where ALBUMID = ?'
            query2 = 'delete from TRACKS where ALBUMID = ?'
            try:
                self.dbc.execute(query1,(self.albumid,))
                self.dbc.execute(query2,(self.albumid,))
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_rating(self):
        f = '[unmusic] db.DB.get_rating'
        if self.Success:
            query = 'select RATING from TRACKS where ALBUMID = ? \
                     order by NO'
            try:
                self.dbc.execute(query,(self.albumid,))
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def set_rating(self,value):
        f = '[unmusic] db.DB.set_rating'
        if self.Success:
            query = 'update TRACKS set RATING = ? where ALBUMID = ?'
            try:
                self.dbc.execute(query,(value,self.albumid,))
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def updateDB(self,query):
        f = '[unmusic] db.DB.updateDB'
        if self.Success:
            if query:
                try:
                    self.dbc.executescript(query)
                except Exception as e:
                    mes = _('Unable to execute:\n"{}"\n\nDetails: {}')
                    mes = mes.format(str(query).replace(';',';\n'),e)
                    sh.objs.get_mes(f,mes).show_error()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_tracks(self):
        f = '[unmusic] db.DB.get_tracks'
        if self.Success:
            query = 'select TITLE,NO,LYRICS,COMMENT,BITRATE,LENGTH \
                    ,RATING from TRACKS where ALBUMID = ? order by NO'
            try:
                self.dbc.execute(query,(self.albumid,))
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def search_track(self,pattern,limit=50):
        f = '[unmusic] db.DB.search_track'
        if self.Success:
            if pattern:
                query = 'select ALBUMID,TITLE,NO,LYRICS,COMMENT,BITRATE\
                        ,LENGTH,RATING from TRACKS where SEARCH like ? \
                         order by ALBUMID,NO limit ?'
                pattern = '%' + pattern.lower() + '%'
                try:
                    self.dbc.execute(query,(pattern,limit,))
                    return self.dbc.fetchall()
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_next_album(self,search):
        f = '[unmusic] db.DB.get_next_album'
        if self.Success:
            if search:
                query = 'select ALBUMID from ALBUMS where ALBUMID > ? \
                         and SEARCH like ? order by ALBUMID'
                search = '%' + search.lower() + '%'
                try:
                    self.dbc.execute(query,(self.albumid,search,))
                    result = self.dbc.fetchone()
                    if result:
                        return result[0]
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_prev_album(self,search):
        f = '[unmusic] db.DB.get_prev_album'
        if self.Success:
            if search:
                query = 'select ALBUMID from ALBUMS where ALBUMID < ? \
                         and SEARCH like ? order by ALBUMID desc'
                search = '%' + search.lower() + '%'
                try:
                    self.dbc.execute(query,(self.albumid,search,))
                    result = self.dbc.fetchone()
                    if result:
                        return result[0]
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_prev_id(self):
        f = '[unmusic] db.DB.get_prev_id'
        if self.Success:
            query = 'select ALBUMID from ALBUMS where ALBUMID < ? \
                     order by ALBUMID desc'
            try:
                self.dbc.execute(query,(self.albumid,))
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_next_id(self):
        f = '[unmusic] db.DB.get_next_id'
        if self.Success:
            query = 'select ALBUMID from ALBUMS where ALBUMID > ? \
                     order by ALBUMID'
            try:
                self.dbc.execute(query,(self.albumid,))
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_album(self):
        f = '[unmusic] db.DB.get_album'
        if self.Success:
            query = 'select ALBUM,ARTIST,YEAR,GENRE,COUNTRY,COMMENT \
                     from ALBUMS where ALBUMID = ?'
            try:
                self.dbc.execute(query,(self.albumid,))
                return self.dbc.fetchone()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_min_id(self):
        f = '[unmusic] db.DB.get_min_id'
        if self.Success:
            query = 'select ALBUMID from ALBUMS order by ALBUMID'
            try:
                ''' 'self.dbc.lastrowid' returns 'None' if an album is
                    already in DB.
                '''
                self.dbc.execute(query)
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_max_id(self):
        f = '[unmusic] db.DB.get_max_id'
        if self.Success:
            query = 'select ALBUMID from ALBUMS order by ALBUMID desc'
            try:
                ''' 'self.dbc.lastrowid' returns 'None' if an album is
                    already in DB.
                '''
                self.dbc.execute(query)
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
        f = '[unmusic] db.DB.has_track'
        if self.Success:
            query = 'select TITLE from TRACKS where ALBUMID = ? \
                     and NO = ? and BITRATE = ?'
            try:
                self.dbc.execute(query,(self.albumid,no,bitrate,))
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def has_album(self,artist,year,album):
        f = '[unmusic] db.DB.has_album'
        if self.Success:
            query = 'select ALBUMID from ALBUMS where ARTIST = ? \
                     and YEAR = ? and ALBUM = ?'
            try:
                self.dbc.execute(query,(artist,year,album,))
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
        f = '[unmusic] db.DB.print'
        if self.Success:
            ''' 'self.dbc.description' is 'None' without performing 
                'select' first
             '''
            if not Selected:
                self.dbc.execute('select * from %s' % table)
            headers = [cn[0] for cn in self.dbc.description]
            rows = self.dbc.fetchall()
            sh.lg.Table (headers = headers
                        ,rows = rows
                        ,Shorten = Shorten
                        ,MaxRow = MaxRow
                        ,MaxRows = MaxRows
                        ).print()
        else:
            sh.com.cancel(f)
    
    def add_track(self,data):
        f = '[unmusic] db.DB.add_track'
        if self.Success:
            if data:
                query = 'insert into TRACKS values (?,?,?,?,?,?,?,?,?)'
                try:
                    self.dbc.execute(query,data)
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def add_album(self,data):
        f = '[unmusic] db.DB.add_album'
        if self.Success:
            if data:
                query = 'insert into ALBUMS values (NULL,?,?,?,?,?,?,?)'
                try:
                    self.dbc.execute(query,data)
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def create_tracks(self):
        f = '[unmusic] db.DB.create_tracks'
        if self.Success:
            # 9 columns by now
            query = 'create table if not exists TRACKS (\
                     ALBUMID integer \
                    ,TITLE   text    \
                    ,NO      integer \
                    ,LYRICS  text    \
                    ,COMMENT text    \
                    ,SEARCH  text    \
                    ,BITRATE integer \
                    ,LENGTH  integer \
                    ,RATING  integer \
                                                       )'
            try:
                self.dbc.execute(query)
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_albums(self):
        f = '[unmusic] db.DB.create_albums'
        if self.Success:
            # 8 columns by now
            query = 'create table if not exists ALBUMS (\
                     ALBUMID integer primary key autoincrement \
                    ,ALBUM   text    \
                    ,ARTIST  text    \
                    ,YEAR    integer \
                    ,GENRE   text    \
                    ,COUNTRY text    \
                    ,COMMENT text    \
                    ,SEARCH  text    \
                                                       )'
            try:
                self.dbc.execute(query)
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def save(self):
        f = '[unmusic] db.DB.save'
        if self.Success:
            mes = _('Save "{}"').format(self.path)
            sh.objs.get_mes(f,mes,True).show_info()
            try:
                self.db.commit()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def fail(self,func,error):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self.path,error)
        sh.objs.get_mes(func,mes).show_warning()
        ''' We need to quit as soon as possible, otherwise, folders
            will be obfuscated, but the info about them will not be
            stored in the DB!
        '''
        sys.exit()
    
    def close(self):
        f = '[unmusic] db.DB.close'
        if self.Success:
            try:
                self.dbc.close()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def connect(self):
        f = '[unmusic] db.DB.connect'
        if self.Success:
            try:
                self.db = sqlite3.connect(self.path)
                self.dbc = self.db.cursor()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
