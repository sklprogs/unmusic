#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
import logic             as lg

import gettext
import skl_shared.gettext_windows
skl_shared.gettext_windows.setup_env()
gettext.install('unmusic','../resources/locale')


f = '[unmusic] collect_silent.__main__'
sh.GUI_MES = False
folder = sh.lg.Home(app_name='unmusic').add_share(_('not processed'))
if sh.lg.Path(folder).create():
    iwalk = lg.Walker(folder)
    dirs  = iwalk.dirs()
    if dirs:
        count = 0
        timer = sh.lg.Timer(f)
        timer.start()
        for folder in dirs:
            if lg.objs.db().Success:
                count += 1
                basename = sh.lg.Path(folder).basename()
                ''' Characters that cannot be decoded can fail the DB even
                    in a Silent mode.
                '''
                basename = sh.lg.Text(basename).delete_unsupported()
                mes = _('Process "{}" ({}/{})').format (basename
                                                       ,count
                                                       ,len(dirs)
                                                       )
                sh.objs.mes(f,mes,True).info()
                lg.Directory(folder).run()
                ''' In case something went wrong, we should lose only
                    1 album record, not the entire sequence.
                '''
                lg.objs.db().save()
            else:
                sh.com.cancel(f)
        delta = timer.end()
        mes = _('Operation has taken {}')
        mes = mes.format(sh.lg.com.human_time(delta))
        sh.objs.mes(f,mes,True).info()
    else:
        sh.com.empty(f)
    iwalk.delete_empty()
else:
    sh.com.cancel(f)
