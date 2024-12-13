#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.message.controller as ms
from skl_shared_qt.paths import Path, Home
from skl_shared_qt.logic import com, Text
from skl_shared_qt.time import Timer

from logic import DB, Walker
from album_editor.logic import Directory


def run():
    f = '[unmusic] collect_silent.run'
    ms.GRAPHICAL = False
    folder = Home(app_name='unmusic').add_share(_('not processed'))
    if not Path(folder).create():
        ms.rep.cancel(f)
        return
    iwalk = Walker(folder)
    dirs = iwalk.get_dirs()
    if not dirs:
        ms.rep.empty(f)
        iwalk.delete_empty()
        DB.close()
        ms.Message(f, _('Goodbye!')).show_debug()
        return
    count = 0
    timer = Timer(f)
    timer.start()
    for folder in dirs:
        if not DB.Success:
            ms.rep.cancel(f)
            continue
        count += 1
        basename = Path(folder).get_basename()
        ''' Characters that cannot be decoded can fail the DB even in
            the Silent mode.
        '''
        basename = Text(basename).delete_unsupported()
        mes = _('Process "{}" ({}/{})').format(basename, count, len(dirs))
        ms.Message(f, mes).show_info()
        Directory(folder).run()
        ''' In case something went wrong, we should lose only 1 album record,
            not the entire sequence.
        '''
        DB.save()
    delta = timer.end()
    mes = _('Operation has taken {}').format(com.get_human_time(delta))
    ms.Message(f, mes).show_info()
    iwalk.delete_empty()
    DB.close()
    ms.Message(f, _('Goodbye!')).show_debug()


if __name__ == '__main__':
    run()
