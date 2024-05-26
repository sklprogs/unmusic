#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared_qt.shared as sh
from skl_shared_qt.localize import _

from config import CONFIG
import logic as lg
from album_editor.controller import ALBUM_EDITOR


class Menu:
    
    def __init__(self):
        self.gui = gi.Menu()
        self.set_bindings()
    
    def delete_bad(self):
        f = '[unmusic] album_editor.controller.Menu.delete_bad'
        ibad = lg.BadMusic()
        objs.get_waitbox().reset (func = f
                                 ,message = _('Calculate ratings')
                                 )
        objs.waitbox.show()
        data = ibad.get_rates()
        objs.waitbox.close()
        if not data:
            mes = _('Nothing to do!')
            sh.objs.get_mes(f, mes).show_info()
            return
        mes = _('Insert all required media to calculate space to be freed.\n\nContinue?')
        ques = sh.objs.get_mes(f, mes).show_question()
        if not ques:
            mes = _('Operation has been canceled by the user.')
            sh.objs.get_mes(f, mes, True).show_info()
            return
        objs.waitbox.reset (func = f
                           ,message = _('Calculate sizes')
                           )
        objs.waitbox.show()
        ibad.get_sizes()
        objs.waitbox.close()
        ibad.report()
        if not ibad.sizes:
            sh.com.rep_empty(f)
            return
        sizes = [item for item in ibad.sizes if item]
        total_size = 0
        for item in sizes:
            total_size += item
        total_size = sh.com.get_human_size (bsize = total_size
                                           ,LargeOnly = True
                                           )
        affected = ibad.get_affected_carriers()
        if affected:
            affected = ', '.join(affected)
        else:
            affected = _('N/A')
        mes = _('Affected carriers: {}.\nSpace to be freed: {}.\nNumber of albums to delete: {}.\nThe list of directories to be deleted is below. Continue?\n\n{}')
        mes = mes.format (affected, total_size, len(ibad.dellst)
                         ,'\n'.join(ibad.dellst)
                         )
        ques = sh.objs.get_mes(f, mes).show_question()
        if not ques:
            mes = _('Operation has been canceled by the user.')
            sh.objs.get_mes(f, mes, True).show_info()
            return
        objs.waitbox.reset (func = f
                           ,message = _('Delete albums')
                           )
        objs.waitbox.show()
        ibad.delete()
        objs.waitbox.close()
        
    def copy(self):
        objs.get_copy().show()
    
    def album_editor(self):
        objs.get_editor().reset()
        objs.editor.show()
    
    def collect(self):
        ''' If an artist and/or album title were changed and originally
            were not empty, there is no easy way to tell if we are
            dealing with the same album or not. So, it's best to add
            tags to DB only once.
        '''
        f = '[unmusic] album_editor.controller.Menu.collect'
        folder = sh.lg.Home(app_name='unmusic').add_share(_('not processed'))
        if not sh.lg.Path(folder).create():
            sh.com.cancel(f)
            return
        iwalk = lg.Walker(folder)
        dirs = iwalk.get_dirs()
        if not dirs:
            sh.com.rep_empty(f)
            iwalk.delete_empty()
            lg.objs.get_db().save()
            return
        count = 0
        timer = sh.lg.Timer(f)
        timer.start()
        for folder in dirs:
            if not lg.objs.get_db().Success:
                sh.com.cancel(f)
                continue
            count += 1
            basename = sh.lg.Path(folder).get_basename()
            itext = sh.lg.Text(basename)
            itext.delete_unsupported()
            itext.shorten(max_len=15)
            mes = _('Process "{}" ({}/{})')
            mes = mes.format(itext.text, count, len(dirs))
            gi.objs.get_wait().reset (func = f
                                     ,message = mes
                                     )
            gi.objs.wait.show()
            lg.Directory(folder).run()
            ''' In case something went wrong, we should loose only 1 album
                record, not the entire sequence.
            '''
            lg.objs.get_db().save()
        gi.objs.get_wait().close()
        delta = timer.end()
        mes = _('Operation has taken {}')
        mes = mes.format(sh.lg.com.get_human_time(delta))
        sh.objs.get_mes(f, mes).show_info()
        objs.get_editor().reset()
        objs.editor.show()
        iwalk.delete_empty()
        lg.objs.get_db().save()
    
    def prepare(self):
        f = '[unmusic] album_editor.controller.Menu.prepare'
        mes = _('Not implemented yet!')
        sh.objs.get_mes(f, mes).show_info()
    
    def set_bindings(self):
        self.gui.a[0].action = self.album_editor
        self.gui.a[1].action = self.prepare
        self.gui.a[2].action = self.collect
        self.gui.a[3].action = self.copy
        self.gui.a[4].action = self.delete_bad
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()


if __name__ == '__main__':
    f = '[unmusic] unmusic.__main__'
    sh.com.start()
    if CONFIG.Success:
        ALBUM_EDITOR.reset()
        ALBUM_EDITOR.show()
    else:
        mes = _('Invalid configuration!')
        #FIX: quit app normally after common dialog
        #sh.objs.get_mes(f, mes).show_error()
        idebug = sh.Debug(f, mes)
        idebug.show()
    sh.com.end()
