#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from config import PATHS
import logic as lg


class Collection:
    
    def __init__(self):
        self.set_paths()
    
    def set_paths(self):
        self.local = PATHS.get_local_collection()
        self.external = PATHS.get_external_collection()
        self.mobile = PATHS.get_mobile_collection()
    
    def get_local_album(self, albumid=None):
        if albumid is None:
            return os.path.join(self.local, str(lg.objs.get_db().albumid))
        else:
            return os.path.join(self.local, str(albumid))
    
    def get_ext_album(self, albumid=None):
        if albumid is None:
            return os.path.join(self.external, str(lg.objs.get_db().albumid))
        else:
            return os.path.join(self.external, str(albumid))
    
    def get_mob_album(self, albumid=None):
        if albumid is None:
            return os.path.join(self.mobile, str(lg.objs.get_db().albumid))
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



class AlbumEditor:
    
    def __init__(self):
        self.Success = True
    
    def _has_any_album(self, albumids):
        for albumid in albumids:
            if COLLECTION.has_any_album(albumid):
                return albumid
    
    def set_prev_unrated(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.set_prev_unrated'
        if not self.Success:
            sh.com.cancel(f)
            return
        albumids = lg.objs.get_db().get_prev_unrated(lg.objs.db.albumid)
        self._set_unrated(albumids)
    
    def set_next_unrated(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.set_next_unrated'
        if not self.Success:
            sh.com.cancel(f)
            return
        albumids = lg.objs.get_db().get_next_unrated(lg.objs.db.albumid)
        self._set_unrated(albumids)
    
    def _set_unrated(self, albumids):
        f = '[unmusic] album_editor.logic.AlbumEditor._set_unrated'
        if not albumids:
            mes = _('No more matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        albumid = self._has_any_album(albumids)
        if albumid is None:
            mes = _('No more matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        lg.objs.db.albumid = albumid
        self.check_no()
    
    def set_prev_rated(self, rating=0):
        # This code is orphaned, but may be useful in the future
        f = '[unmusic] album_editor.logic.AlbumEditor.set_prev_rated'
        if not self.Success:
            sh.com.cancel(f)
            return
        albumid = lg.objs.get_db().get_prev_rated(rating, lg.objs.db.albumid)
        if not albumid:
            mes = _('No more matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        lg.objs.db.albumid = albumid
        self.check_no()
    
    def set_next_rated(self, rating=0):
        # This code is orphaned, but may be useful in the future
        f = '[unmusic] album_editor.logic.AlbumEditor.set_next_rated'
        if not self.Success:
            sh.com.cancel(f)
            return
        albumid = lg.objs.get_db().get_next_rated(rating, lg.objs.db.albumid)
        if not albumid:
            mes = _('No more matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        lg.objs.db.albumid = albumid
        self.check_no()
    
    def get_mean_bitrate(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.get_mean_bitrate'
        if not self.Success:
            sh.com.cancel(f)
            return
        mean = lg.objs.get_db().get_bitrate()
        if not mean:
            sh.com.rep_empty(f)
            return
        mean = [rating for rating in mean if rating]
        if not mean:
            return 0
        # Return 'int' since we don't need 'float' here
        return sum(mean) // len(mean)
    
    def get_mean_rating(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.get_mean_rating'
        if not self.Success:
            sh.com.cancel(f)
            return 0.0
        mean = lg.objs.get_db().get_rates()
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
        f = '[unmusic] album_editor.logic.AlbumEditor.check_no'
        if self.Success:
            lg.objs.get_db().albumid = sh.lg.Input(f, lg.objs.get_db().albumid).get_integer()
        else:
            sh.com.cancel(f)
        return lg.objs.get_db().albumid
    
    def get_min(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.get_min'
        if not self.Success:
            sh.com.cancel(f)
            return 0
        return sh.lg.Input(f, lg.objs.get_db().get_min_id()).get_integer()
    
    def get_max(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.get_max'
        if not self.Success:
            sh.com.cancel(f)
            return 0
        _max = lg.objs.get_db().get_max_id()
        if not isinstance(_max, int):
            mes = _('The database is empty. You need to fill it first.')
            sh.objs.get_mes(f, mes).show_warning()
            return 0
        return _max
    
    def inc(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.inc'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.check_no() == self.get_max():
            lg.objs.get_db().albumid = self.get_min()
        else:
            lg.objs.get_db().albumid = lg.objs.get_db().get_next_id()
            self.check_no()
    
    def dec(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.dec'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.check_no() == self.get_min():
            lg.objs.get_db().albumid = self.get_max()
        else:
            lg.objs.get_db().albumid = lg.objs.get_db().get_prev_id()
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
            add += ' where ALBUMID=%d;commit;' % lg.objs.get_db().albumid
            return add


COLLECTION = Collection()
