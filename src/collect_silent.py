#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared as sh
import logic  as lg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('unmusic','../resources/locale')


f = '[unmusic] collect_silent.__main__'
sh.objs.mes(Silent=1)
folder = sh.Home(app_name='unmusic').add_share(_('not processed'))
if sh.Path(folder).create():
    iwalk = lg.Walker(folder)
    dirs  = iwalk.dirs()
    if dirs:
        count = 0
        timer = sh.Timer(f)
        timer.start()
        for folder in dirs:
            if lg.objs.db().Success:
                count += 1
                basename = sh.Path(folder).basename()
                ''' Characters that cannot be decoded can fail the DB even
                    in a Silent mode.
                '''
                basename = sh.Text(basename).delete_unsupported()
                sh.log.append (f,_('INFO')
                              ,_('Process "%s" (%d/%d)') % (basename,count
                                                           ,len(dirs)
                                                           )
                              )
                lg.Directory (path      = folder
                             ,Obfuscate = True
                             ).run()
                ''' In case something went wrong, we should lose only
                    1 album record, not the entire sequence.
                '''
                lg.objs.db().save()
            else:
                sh.com.cancel(f)
        delta = timer.end()
        sh.objs.mes (f,_('INFO')
                    ,_('Operation has taken %s') \
                    % sh.com.human_time(delta)
                    )
    else:
        sh.com.empty(f)
    iwalk.delete_empty()
else:
    sh.com.cancel(f)
