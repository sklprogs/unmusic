#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sqlite3

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from skl_shared.basic_text import Shorten
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.progress_bar.controller import PROGRESS
from skl_shared.graphics.debug.controller import DEBUG
from skl_shared.paths import File, Directory
from skl_shared.logic import com as shcom

ROOT.get_root()

from config import PATHS
from logic import DB
from album_editor.logic import DeleteTracks


class DeleteBad:
    
    def __init__(self):
        self.Success = True
        self.rating = 7
        self.limit = 0
        self.size = 0
        self.folders = []
        self.files = []
        self.albums = {}
    
    def set_albums(self):
        f = '[unmusic] utils.DeleteBad.set_albums'
        if not self.Success:
            rep.cancel(f)
            return
        data = DB.get_bad_albums(self.rating, self.limit)
        if not data:
            self.Success = False
            rep.empty(f)
            return
        for id_, nos in data:
            if id_ in self.albums:
                self.albums[id_] += [nos]
            else:
                self.albums[id_] = [nos]
    
    def debug(self):
        f = '[unmusic] utils.DeleteBad.debug'
        if not self.Success:
            rep.cancel(f)
            return
        desc = []
        for id_ in self.albums:
            mes = _('Process album #{}').format(id_)
            Message(f, mes).show_debug()
            DB.albumid = id_
            data = DB.get_album()
            if not data:
                rep.empty(f)
                break
            album, artist, year = data[0], data[1], data[2]
            row = _('{}: {} - {} - {} ({} tracks)')
            row = row.format(id_, artist, year, album, len(self.albums[id_]))
            desc.append(row)
        DEBUG.reset(f, '\n'.join(desc))
        DEBUG.show()
    
    def loop(self):
        f = '[unmusic] utils.DeleteBad.loop'
        if not self.Success:
            rep.cancel(f)
            return
        PROGRESS.set_value(0)
        PROGRESS.set_max(len(self.albums))
        PROGRESS.show()
        for id_ in self.albums:
            PROGRESS.update()
            mes = _('Calculate the size of album #{}').format(id_)
            PROGRESS.set_info(mes)
            DB.albumid = id_
            idelete = DeleteTracks()
            idelete.nos = self.albums[id_]
            idelete.set_carriers()
            idelete.set_files()
            idelete.set_size()
            self.folders += idelete.carriers
            self.files += idelete.files
            self.size += idelete.size
            PROGRESS.inc()
        PROGRESS.close()
    
    def delete(self):
        f = '[unmusic] utils.DeleteBad.delete'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.files:
            rep.lazy(f)
            return
        size = shcom.get_human_size(self.size, True)
        mes = _('Delete {} tracks ({}) with rating < {} from {} albums ({} folders on all carriers)?')
        mes = mes.format(len(self.files), size, self.rating, len(self.albums)
                        ,len(self.folders))
        if not Message(f, mes, True).show_question():
            mes = _('Operation has been canceled by the user.')
            Message(f, mes).show_info()
            return
        PROGRESS.set_title(_('Delete tracks'))
        PROGRESS.set_value(0)
        PROGRESS.set_max(len(self.files))
        PROGRESS.show()
        for file in self.files:
            PROGRESS.update()
            mes = _('Delete {}').format(file)
            mes = Shorten(mes, 33, True).run()
            PROGRESS.set_info(mes)
            if not File(file).delete():
                break
            PROGRESS.inc()
        PROGRESS.close()
        for folder in self.folders:
            Directory(folder).delete_empty()
    
    def run(self):
        self.set_albums()
        self.loop()
        #self.debug()
        self.delete()



class Shrink:
    ''' Shrink local collection by deleting those albums whose *names*
        (contents identity is not checked) are present in external collection.
    '''
    def __init__(self):
        self.Success = True
        self.path_external = PATHS.get_external_collection()
        self.path_local = PATHS.get_local_collection()
        self.albums_external = []
        self.albums_local = []
    
    def set_albums(self):
        f = '[unmusic] utils.Shrink.set_albums'
        if not self.Success:
            rep.cancel(f)
            return
        PROGRESS.set_value(0)
        PROGRESS.set_max(2)
        PROGRESS.show()
        PROGRESS.update()
        PROGRESS.set_info(_('Read external collection'))
        self.albums_external = Directory(self.path_external).get_rel_dirs()
        PROGRESS.inc()
        PROGRESS.update()
        PROGRESS.set_info(_('Read local collection'))
        self.albums_local = Directory(self.path_local).get_rel_dirs()
        PROGRESS.inc()
        PROGRESS.close()
        if not self.albums_external or not self.albums_local:
            self.Success = False
            rep.empty_output(f)
    
    def _delete(self, albumid):
        f = '[unmusic] utils.Shrink._delete'
        if not albumid:
            rep.empty(f)
            return
        path = PATHS.get_local_album(albumid)
        if not path:
            rep.empty(f)
            return
        mes = _('Delete {}').format(albumid)
        PROGRESS.set_info(mes)
        return Directory(path).delete()
    
    def delete(self):
        f = '[unmusic] utils.Shrink.delete'
        if not self.Success:
            rep.cancel(f)
            return
        duplicate = [album for album in self.albums_local \
                    if album in self.albums_external]
        if not duplicate:
            mes = _('There are no duplicates!')
            Message(f, mes, True).show_info()
            return
        mes = _('Do you really want to delete {} albums?').format(len(duplicate))
        answer = Message(f, mes, True).show_question()
        if not answer:
            mes = _('Operation has been canceled by the user.')
            Message(f, mes, True).show_info()
            return
        deleted = 0
        PROGRESS.set_title(_('Delete albums'))
        PROGRESS.set_value(0)
        PROGRESS.set_max(len(duplicate))
        PROGRESS.show()
        for album in duplicate:
            PROGRESS.update()
            if self._delete(album):
                deleted += 1
            PROGRESS.inc()
        PROGRESS.close()
        mes = _('{} albums have been deleted!').format(deleted)
        Message(f, mes, True).show_info()
    
    def run(self):
        self.set_albums()
        self.delete()



class Commands:
    
    def __init__(self):
        self.path = '/home/pete/.config/unmusic/unmusic.db'
        self.clone = '/tmp/unmusic.db'
    
    def alter(self):
        if os.path.exists(self.clone):
            File(self.clone).delete()
        # Alter DB and add/remove some columns
        Clone(self.path, self.clone).run()



class Clone:
    
    def __init__(self, path, clone):
        self.albums = ()
        self.tracks = ()
        self.path = path
        self.clone = clone
        self.Success = self.clone and File(self.path).Success
    
    def run(self):
        self.connect()
        self.connectw()
        self.fetch()
        self.create_tables()
        self.fill()
        self.savew()
        self.close()
        self.closew()
    
    def fetch_images(self):
        f = '[unmusic] utils.Clone.fetch_images'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Fetch data')
        Message(f, mes).show_debug()
        query = 'select ALBUMID,IMAGE from ALBUMS order by ALBUMID'
        try:
            self.dbc.execute(query)
            return self.dbc.fetchall()
        except Exception as e:
            self.fail(f, e)
    
    def create_tables(self):
        self.create_albums()
        self.create_tracks()
    
    def fetch(self):
        self.fetch_albums()
        self.fetch_tracks()
    
    def fail(self,f,e):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}').format(self.path, e)
        Message(f, mes, True).show_warning()
    
    def fail_clone(self, f, e):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}').format(self.clone, e)
        Message(f, mes, True).show_warning()
    
    def savew(self):
        f = '[unmusic] utils.Clone.savew'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.dbw.commit()
        except Exception as e:
            self.fail_clone(f, e)
        
    def connect(self):
        f = '[unmusic] utils.Clone.connect'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.db = sqlite3.connect(self.path)
            self.dbc = self.db.cursor()
        except Exception as e:
            self.fail(f, e)
                          
    def connectw(self):
        f = '[unmusic] utils.Clone.connectw'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.dbw = sqlite3.connect(self.clone)
            self.dbcw = self.dbw.cursor()
        except Exception as e:
            self.fail_clone(f, e)
    
    def fetch_albums(self):
        f = '[unmusic] utils.Clone.fetch_albums'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Fetch data from {}').format('ALBUMS')
        Message(f, mes).show_info()
        # 8 columns to fetch
        query = 'select ALBUMID, ALBUM, ARTIST, YEAR, GENRE, COUNTRY, COMMENT \
                ,SEARCH from ALBUMS'
        try:
            self.dbc.execute(query)
            self.albums = self.dbc.fetchall()
        except Exception as e:
            self.fail(f, e)
    
    def fetch_tracks(self):
        f = '[unmusic] utils.Clone.fetch_tracks'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Fetch data from {}').format('TRACKS')
        Message(f, mes).show_info()
        # 9 columns to fetch
        query = 'select ALBUMID, TITLE, NO, LYRICS, COMMENT, SEARCH, BITRATE \
                ,LENGTH, RATING from TRACKS'
        try:
            self.dbc.execute(query)
            self.tracks = self.dbc.fetchall()
        except Exception as e:
            self.fail(f, e)
    
    def create_albums(self):
        f = '[unmusic] utils.Clone.create_albums'
        if not self.Success:
            rep.cancel(f)
            return
        # 9 columns by now
        query = 'create table ALBUMS (\
                 ALBUMID integer primary key autoincrement \
                ,ALBUM   text    \
                ,ARTIST  text    \
                ,YEAR    integer \
                ,GENRE   text    \
                ,COUNTRY text    \
                ,COMMENT text    \
                ,SEARCH  text    \
                ,RATING  float   \
                                     )'
        self._create_table(f, query)
    
    def _create_table(self, f, query):
        try:
            self.dbcw.execute(query)
        except Exception as e:
            self.fail_clone(f, e)
    
    def create_tracks(self):
        f = '[unmusic] utils.Clone.create_tracks'
        if not self.Success:
            rep.cancel(f)
            return
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
        self._create_table(f, query)
    
    def _get_mean(self, ratings):
        if 0 in ratings:
            return 0
        else:
            return round(sum(ratings) / len(ratings), 2)
    
    def _fill_albums(self):
        f = '[unmusic] utils.Clone._fill_albums'
        query = 'insert into ALBUMS values (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        for i in range(len(self.albums)):
            row = self.albums[i]
            DB.albumid = row[0]
            ratings = DB.get_rates()
            if ratings:
                rating = self._get_mean(ratings)
            else:
                rating = 0
                rep.empty(f)
                mes = _('Tracks of album #{} have no rating!').format(DB.albumid)
                Message(f, mes).show_warning()
                self.Success = False
                return
            if i % 100 == 0:
                mes = _('Album ID: {}. Rating: {}').format(row[0], rating)
                Message(f, mes).show_debug()
            row += (rating,)
            self._fill_row(f, query, row)
    
    def _fill_tracks(self):
        f = '[unmusic] utils.Clone._fill_tracks'
        query = 'insert into TRACKS values (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        for row in self.tracks:
            self._fill_row(f, query, row)
    
    def _fill_row(self, f, query, row):
        try:
            self.dbcw.execute(query, row)
        except Exception as e:
            self.Success = False
            self.fail(f, e)
            return
    
    def fill(self):
        f = '[unmusic] utils.Clone.fill'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.albums or not self.tracks:
            rep.empty(f)
            return
        mes = _('Copy "{}" to "{}"').format(self.path, self.clone)
        Message(f, mes).show_info()
        self._fill_albums()
        self._fill_tracks()
                          
    def close(self):
        f = '[unmusic] utils.Clone.close'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.dbc.close()
        except Exception as e:
            self.fail(f, e)
                          
    def closew(self):
        f = '[unmusic] utils.Clone.closew'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.dbcw.close()
        except Exception as e:
            self.fail_clone(f, e)


com = Commands()


if __name__ == '__main__':
    f = '[unmusic] utils.__main__'
    #com.alter()
    #Shrink().run()
    DeleteBad().run()
    #TODO: Delete when closing the graphics is fixed
    mes = _('Operation has been completed.')
    Message(f, mes, True).show_info()
    mes = _('Goodbye!')
    Message(f, mes).show_debug()
    ROOT.end()
