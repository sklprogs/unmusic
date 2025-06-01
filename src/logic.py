#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re
import db

from config import CONFIG, PATHS

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.paths import Directory
from skl_shared_qt.logic import com
from skl_shared_qt.table import Table
from skl_shared_qt.graphics.debug.controller import DEBUG

VERSION = '1.1'
#NOTE: Do not localize (being stored in DB)
GENRES = ('?', 'Alternative Rock', 'Ambient', 'Black Metal', 'Blues'
         ,'Brutal Death Metal', 'Chanson', 'Classical', 'Death Metal'
         ,'Death Metal/Grindcore', 'Death/Black Metal'
         ,'Death/Thrash Metal', 'Deathcore', 'Electronic', 'Ethnic', 'Game'
         ,'Goregrind', 'Grindcore', 'Heavy Metal', 'Industrial Metal'
         ,'Melodic Death Metal', 'Metal', 'Pop', 'Power Metal', 'Rap'
         ,'Relaxation', 'Rock', 'Soundtrack', 'Technical Brutal Death Metal'
         ,'Technical Death Metal', 'Thrash Metal', 'Vocal')


class Walker:
    
    def __init__(self, path=''):
        if path:
            self.reset(path)
    
    def delete_empty(self):
        ''' Delete empty folders. Since 'Directory' instance is recreated each
            time, we can call this procedure at any time without the need to
            reset 'Walker'.
        '''
        f = '[unmusic] logic.Walker.delete_empty'
        self.get_dirs()
        if not self.Success:
            rep.cancel(f)
            return
        if not self.dirs:
            rep.empty(f)
            return
        for folder in self.dirs:
            Directory(folder).delete_empty()
    
    def reset(self, path):
        self.set_values()
        self.path = path
        self.idir = Directory(self.path)
        self.Success = self.idir.Success
    
    def get_dirs(self):
        f = '[unmusic] logic.Walker.get_dirs'
        if not self.Success:
            rep.cancel(f)
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
    
    def export_config(self):
        f = '[unmusic] logic.Commands.export_config'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        if not DB.Success:
            rep.cancel(f)
            return
        CONFIG.new['cur_id'] = DB.albumid
        #TODO: Save CONFIG.new['delete']
    
    def restore_id(self):
        f = '[unmusic] logic.Commands.restore_id'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        if not DB.Success:
            rep.cancel(f)
            return
        min_ = DB.get_min_id()
        max_ = DB.get_max_id()
        if not min_ or not max_:
            rep.empty(f)
            return
        if not min_ <= CONFIG.new['cur_id'] <= max_:
            sub = f"{min_} <= {CONFIG.new['cur_id']} <= {max_}"
            mes = _('Condition "{}" is not observed!').format(sub)
            Message(f, mes, True).show_warning()
            return
        DB.albumid = CONFIG.new['cur_id']
        mes = _('Current album: #{}').format(DB.albumid)
        Message(f, mes).show_info()
    
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
