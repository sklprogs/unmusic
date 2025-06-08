#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.paths import Path, Home
from skl_shared.logic import com, Text
from skl_shared.time import Timer
from skl_shared.graphics.progress_bar.controller import ProgressBar

from logic import DB, Walker
from album_editor.logic import Directory


class Collect:
    
    def __init__(self):
        self.unprocessed = Home(app_name='unmusic').add_share(_('not processed'))
        self.Success = DB.Success
        self.folders = []
        self.bar = ProgressBar()
        self.bar.set_title(_('Processing albums'))
    
    def create_unprocessed(self):
        f = '[unmusic] collect.Collect.create_unprocessed'
        if not self.Success:
            rep.cancel(f)
            return
        if not Path(self.unprocessed).create():
            self.Success = False
            rep.cancel(f)
            return
    
    def set_folders(self):
        f = '[unmusic] collect.Collect.set_folders'
        if not self.Success:
            rep.cancel(f)
            return
        self.iwalk = Walker(self.unprocessed)
        self.folders = self.iwalk.get_dirs()
        self.Success = self.iwalk.Success
        if not self.Success:
            rep.cancel(f)
            return
        if not self.folders:
            self.Success = False
            rep.empty(f)
            self.iwalk.delete_empty()
            DB.close()
            return
    
    def store_album(self, folder):
        f = '[unmusic] collect.Collect.fill_db'
        if not self.Success or not DB.Success:
            self.Success = False
            rep.cancel(f)
            return
        basename = Path(folder).get_basename()
        self.bar.update()
        mes = _('Process "{}"').format(basename)
        self.bar.set_info(mes)
        Directory(folder).run()
        ''' In case something went wrong, we should lose only 1 album record,
            not the entire sequence.
        '''
        DB.save()
        self.bar.inc()
        return DB.Success
    
    def loop(self):
        f = '[unmusic] collect.Collect.loop'
        if not self.Success:
            rep.cancel(f)
            return
        timer = Timer(f)
        timer.start()
        self.bar.set_max(len(self.folders))
        self.bar.show()
        for folder in self.folders:
            if not self.store_album(folder):
                break
        delta = timer.end()
        mes = _('Operation has taken {}').format(com.get_human_time(delta))
        Message(f, mes).show_info()
        self.iwalk.delete_empty()
        self.bar.close()
    
    def run(self):
        self.create_unprocessed()
        self.set_folders()
        self.loop()
        #DB.close()
        #Message(f, _('Operation has been completed.')).show_info()
