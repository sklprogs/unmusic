#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sqlite3
import skl_shared.shared as sh
from skl_shared.localize import _
import logic as lg
import gui as gi


class Image:
    
    def __init__(self):
        self.dir = sh.Home('unmusic').add_share('thumbs')
        self.Success = sh.Path(self.dir).create()
        self.path = ''
        self.albumid = 0
        self.bytes = None
        self.Present = False
        self.Processed = False
        self.Skipped = False
    
    def save(self):
        f = '[unmusic] utils.Image.save'
        if self.Success:
            if self.path:
                if os.path.exists(self.path):
                    mes = _('File "{}" already exists.')
                    mes = mes.format(self.path)
                    sh.objs.get_mes(f,mes,True).show_debug()
                    self.Present = True
                elif self.bytes:
                    mes = _('Save "{}"').format(self.path)
                    sh.objs.get_mes(f,mes,True).show_info()
                    iimage = sh.Image()
                    iimage.bytes_ = self.bytes
                    iimage.get_loader()
                    self.Processed = iimage.save(self.path,'JPEG')
                else:
                    mes = _('Album {} has no cover!')
                    mes = mes.format(self.albumid)
                    sh.objs.get_mes(f,mes,True).show_debug()
                    self.Skipped = True
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_path(self):
        f = '[unmusic] utils.Image.set_path'
        if self.Success:
            name = str(self.albumid)
            if name:
                name += '.jpg'
                self.path = os.path.join(self.dir,name)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def reset(self,albumid,bytes_):
        self.path = ''
        self.albumid = albumid
        self.bytes = bytes_
        self.Present = False
        self.Processed = False
        self.Skipped = False
    
    def run(self):
        self.set_path()
        self.save()



class Commands:
    
    def __init__(self):
        self.path = '/home/pete/.config/unmusic/unmusic.db'
        self.clone = '/tmp/unmusic.db'
    
    def extract_images(self):
        f = '[unmusic] utils.Commands.extract_images'
        idb = DB(self.path,self.clone)
        idb.connect()
        data = idb.fetch_images()
        if data:
            errors = 0
            present = 0
            processed = 0
            skipped = 0
            iimage = Image()
            for row in data:
                iimage.reset(row[0],row[1])
                iimage.run()
                if iimage.Present:
                    present += 1
                elif iimage.Skipped:
                    skipped += 1
                elif iimage.Processed:
                    processed += 1
                else:
                    errors += 1
            mes = _('Files in total: {}, processed: {}, already existing: {}, skipped: {}, errors: {}')
            mes = mes.format(len(data),processed,present,skipped,errors)
            sh.objs.get_mes(f,mes,True).show_info()
        else:
            sh.com.rep_empty(f)
        idb.close()
    
    def alter(self):
        if os.path.exists(self.clone):
            sh.File(self.clone).delete()
        # Alter DB and add/remove some columns
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connect()
        idb.connectw()
        idb.fetch()
        idb.create_tables()
        idb.fill()
        idb.savew()
        idb.close()
        idb.closew()
        
    def is_camel_case(self,title):
        words = title.split(' ')
        for word in words:
            if word != word.upper() and len(word) > 1 \
            and word[0].isalpha():
                for sym in word[1:]:
                    if sym in 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЪЬЭЮЯ':
                        return True
    
    def show_cyphered(self):
        f = '[unmusic] utils.Commands.show_cyphered'
        if lg.objs.get_db().Success:
            titles = []
            #query = 'select TITLE from TRACKS order by ALBUMID'
            query = 'select ALBUM from ALBUMS order by ALBUM'
            try:
                lg.objs.db.dbc.execute(query)
                titles = lg.objs.db.dbc.fetchall()
                if titles:
                    titles = [item[0] for item in titles]
            except Exception as e:
                mes = _('Operation has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.get_mes(f,mes).show_warning()
            result = [title for title in titles \
                      if self.is_camel_case(title)
                     ]
            print('\n'.join(result))
            print(len(result))
        else:
            sh.com.cancel(f)



class DB:
    
    def __init__(self,path,clone):
        self.albums = ()
        self.tracks = ()
        self.path = path
        self.clone = clone
        self.Success = self.clone and sh.File(self.path).Success
    
    def fetch_images(self):
        f = '[unmusic] utils.DB.fetch_images'
        if self.Success:
            mes = _('Fetch data')
            sh.objs.get_mes(f,mes,True).show_debug()
            query = 'select ALBUMID,IMAGE from ALBUMS order by ALBUMID'
            try:
                self.dbc.execute(query)
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_tables(self):
        self.create_albums()
        self.create_tracks()
    
    def fetch(self):
        self.fetch_albums()
        self.fetch_tracks()
    
    def fail(self,f,e):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self.path,e)
        sh.objs.get_mes(f,mes).show_warning()
    
    def fail_clone(self,f,e):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self.clone,e)
        sh.objs.get_mes(f,mes).show_warning()
    
    def savew(self):
        f = '[unmusic] utils.DB.savew'
        if self.Success:
            try:
                self.dbw.commit()
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
        
    def connect(self):
        f = '[unmusic] utils.DB.connect'
        if self.Success:
            try:
                self.db = sqlite3.connect(self.path)
                self.dbc = self.db.cursor()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def connectw(self):
        f = '[unmusic] utils.DB.connectw'
        if self.Success:
            try:
                self.dbw = sqlite3.connect(self.clone)
                self.dbcw = self.dbw.cursor()
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def fetch_albums(self):
        f = '[unmusic] utils.DB.fetch_albums'
        if self.Success:
            mes = _('Fetch data from {}').format('ALBUMS')
            sh.objs.get_mes(f,mes,True).show_info()
            # 8 columns to fetch
            query = 'select ALBUMID,ALBUM,ARTIST,YEAR,GENRE,COUNTRY \
                    ,COMMENT,SEARCH from ALBUMS'
            try:
                self.dbc.execute(query)
                self.albums = self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def fetch_tracks(self):
        f = '[unmusic] utils.DB.fetch_tracks'
        if self.Success:
            mes = _('Fetch data from {}').format('TRACKS')
            sh.objs.get_mes(f,mes,True).show_info()
            # 9 columns to fetch
            query = 'select ALBUMID,TITLE,NO,LYRICS,COMMENT,SEARCH \
                    ,BITRATE,LENGTH,RATING from TRACKS'
            try:
                self.dbc.execute(query)
                self.tracks = self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_albums(self):
        f = '[unmusic] utils.DB.create_albums'
        if self.Success:
            # 8 columns by now
            query = 'create table ALBUMS (\
                     ALBUMID integer primary key autoincrement \
                    ,ALBUM   text    \
                    ,ARTIST  text    \
                    ,YEAR    integer \
                    ,GENRE   text    \
                    ,COUNTRY text    \
                    ,COMMENT text    \
                    ,SEARCH  text    \
                                         )'
            self._create_table(f,query)
        else:
            sh.com.cancel(f)
    
    def _create_table(self,f,query):
        try:
            self.dbcw.execute(query)
        except Exception as e:
            self.fail_clone(f,e)
    
    def create_tracks(self):
        f = '[unmusic] utils.DB.create_tracks'
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
            self._create_table(f,query)
        else:
            sh.com.cancel(f)
    
    def _fill_albums(self):
        f = '[unmusic] utils.DB._fill_albums'
        query = 'insert into ALBUMS values (?,?,?,?,?,?,?,?)'
        for row in self.albums:
            self._fill_row(f,query,row)
    
    def _fill_tracks(self):
        f = '[unmusic] utils.DB._fill_tracks'
        query = 'insert into TRACKS values (?,?,?,?,?,?,?,?,?)'
        for row in self.tracks:
            self._fill_row(f,query,row)
    
    def _fill_row(self,f,query,row):
        try:
            self.dbcw.execute(query,row)
        except Exception as e:
            self.Success = False
            self.fail(f,e)
            return
    
    def fill(self):
        f = '[unmusic] utils.DB.fill'
        if self.Success:
            if self.albums and self.tracks:
                mes = _('Copy "{}" to "{}"').format (self.path
                                                    ,self.clone
                                                    )
                sh.objs.get_mes(f,mes,True).show_info()
                self._fill_albums()
                self._fill_tracks()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
                          
    def close(self):
        f = '[unmusic] utils.DB.close'
        if self.Success:
            try:
                self.dbc.close()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def closew(self):
        f = '[unmusic] utils.DB.closew'
        if self.Success:
            try:
                self.dbcw.close()
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)


com = Commands()


if __name__ == '__main__':
    f = '[unmusic] utils.__main__'
    sh.com.start()
    com.extract_images()
    #com.alter()
    #lg.objs.get_db().close()
    sh.com.end()
