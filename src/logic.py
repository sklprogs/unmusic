#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re
import db

from config import CONFIG, PATHS

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

VERSION = '1.1'
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
        self.Success = DB.Success
    
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
        self.local = PATHS.get_local_collection()
        self.exter = PATHS.get_external_collection()
        self.mobil = PATHS.get_mobile_collection()
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
        albums = DB.get_albums(limit)
        if not albums:
            sh.com.cancel(f)
            return
        old = DB.albumid
        for album in albums:
            DB.albumid = album[0]
            mes = _('Process album ID: {}')
            mes = mes.format(DB.albumid)
            sh.objs.get_mes(f, mes, True).show_debug()
            rates = DB.get_rates()
            if not rates:
                sh.com.rep_empty(f)
                continue
            if min(rates) > 0 and max(rates) <= max_rate:
                album_title = [str(album[2]), str(album[3]), str(album[1])]
                album_title = ' - '.join(album_title)
                item = [album[0], album_title, min(rates), max(rates)]
                self.rates.append(item)
        DB.albumid = old
        return self.rates



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
    
    def restore_id(self):
        f = '[unmusic] logic.Commands.restore_id'
        if not CONFIG.Success:
            sh.com.cancel(f)
            return
        if not DB.Success:
            sh.com.cancel(f)
            return
        min_ = DB.get_min_id()
        max_ = DB.get_max_id()
        if not min_ or not max_:
            sh.com.rep_empty(f)
            return
        if min_ <= CONFIG.new['cur_id'] <= max_:
            DB.albumid = CONFIG.new['cur_id']
        else:
            sub = f"{min_} <= {CONFIG.new['cur_id']} <= {max_}"
            mes = _('Condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f, mes).show_warning()
    
    def decode_back(self, text):
        try:
            byted = bytes(text, 'cp1251')
            return byted.decode('utf-8')
        except:
            return text



DB = db.DB(PATHS.get_db())
com = Commands()
com.restore_id()



if __name__ == '__main__':
    f = '[unmusic] logic.__main__'
    ibad = BadMusic()
    ibad.rates = [[1]]
    ibad.get_sizes()
    DB.close()
