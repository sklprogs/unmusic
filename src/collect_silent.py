#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import logic as lg


def run(self):
    f = '[unmusic] collect_silent.run'
    sh.GUI_MES = False
    folder = sh.lg.Home(app_name='unmusic').add_share(_('not processed'))
    if not sh.lg.Path(folder).create():
        sh.com.cancel(f)
        return
    iwalk = lg.Walker(folder)
    dirs = iwalk.get_dirs()
    if not dirs:
        sh.com.rep_empty(f)
        iwalk.delete_empty()
        lg.objs.get_db().close()
        mes = _('Goodbye!')
        sh.objs.get_mes(f,mes,True).show_debug()
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
        ''' Characters that cannot be decoded can fail the DB even in
            the Silent mode.
        '''
        basename = sh.lg.Text(basename).delete_unsupported()
        mes = _('Process "{}" ({}/{})').format(basename, count, len(dirs))
        sh.objs.get_mes(f,mes,True).show_info()
        lg.Directory(folder).run()
        ''' In case something went wrong, we should lose only 1 album record,
            not the entire sequence.
        '''
        lg.objs.get_db().save()
    delta = timer.end()
    mes = _('Operation has taken {}')
    mes = mes.format(sh.lg.com.get_human_time(delta))
    sh.objs.get_mes(f,mes,True).show_info()
    iwalk.delete_empty()
    lg.objs.get_db().close()
    mes = _('Goodbye!')
    sh.objs.get_mes(f,mes,True).show_debug()


if __name__ == '__main__':
    run()
