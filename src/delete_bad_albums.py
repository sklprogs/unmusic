#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.root.controller import ROOT
from skl_shared_qt.logic import com as shcom
from skl_shared_qt.paths import File, Directory as shDirectory
from skl_shared_qt.graphics.progress_bar.controller import PROGRESS
ROOT.get_root()

from logic import DB
from album_editor.logic import DeleteTracks


class DeleteBadAlbums:
    
    def __init__(self):
        self.Success = True
        self.rating = 7
        self.limit = 100
        self.size = 0
        self.folders = []
        self.files = []
        self.albums = {}
    
    def set_albums(self):
        f = '[unmusic] utils.delete_bad_albums.DeleteBadAlbums.set_albums'
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
        f = '[unmusic] utils.delete_bad_albums.DeleteBadAlbums.debug'
        if not self.Success:
            rep.cancel(f)
            return
        for id_ in self.albums:
            if len(self.albums[id_]) > 1:
                print(f'ID: {id_}, track nos: {self.albums[id_]}')
    
    def loop(self):
        f = '[unmusic] utils.delete_bad_albums.DeleteBadAlbums.loop'
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
        f = '[unmusic] utils.delete_bad_albums.DeleteBadAlbums.delete'
        if not self.Success:
            rep.cancel(f)
            return
        size = shcom.get_human_size(self.size, True)
        mes = _('Delete {} tracks ({}) with rating < {} from {} albums ({} folders on all carriers)?')
        mes = mes.format(len(self.files), size, self.rating, len(self.albums), len(self.folders))
        if not Message(f, mes, True).show_question():
            mes = _('Operation has been canceled by the user.')
            Message(f, mes).show_info()
            return
        for file in self.files:
            if not File(file).delete():
                break
        for folder in self.folders:
            shDirectory(folder).delete_empty()
    
    def run(self):
        self.set_albums()
        self.loop()
        self.delete()


if __name__ == '__main__':
    f = '[unmusic] unmusic.utils.delete_bad_albums.__main__'
    DeleteBadAlbums().run()
    ROOT.end()
