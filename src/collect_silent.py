#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import logic as lg


f = '[unmusic] collect_silent.__main__'
sh.GUI_MES = False
folder = sh.lg.Home(app_name='unmusic').add_share(_('not processed'))
if sh.lg.Path(folder).create():
    iwalk = lg.Walker(folder)
    dirs = iwalk.get_dirs()
    if dirs:
        count = 0
        timer = sh.lg.Timer(f)
        timer.start()
        for folder in dirs:
            if lg.objs.get_db().Success:
                count += 1
                basename = sh.lg.Path(folder).get_basename()
                ''' Characters that cannot be decoded can fail the DB
                    even in a Silent mode.
                '''
                basename = sh.lg.Text(basename).delete_unsupported()
                mes = _('Process "{}" ({}/{})').format (basename
                                                       ,count
                                                       ,len(dirs)
                                                       )
                sh.objs.get_mes(f,mes,True).show_info()
                lg.Directory(folder).run()
                ''' In case something went wrong, we should lose only
                    1 album record, not the entire sequence.
                '''
                lg.objs.get_db().save()
            else:
                sh.com.cancel(f)
        delta = timer.end()
        mes = _('Operation has taken {}')
        mes = mes.format(sh.lg.com.get_human_time(delta))
        sh.objs.get_mes(f,mes,True).show_info()
    else:
        sh.com.rep_empty(f)
    iwalk.delete_empty()
    lg.objs.get_db().close()
    mes = _('Goodbye!')
    sh.objs.get_mes(f,mes,True).show_debug()
else:
    sh.com.cancel(f)
