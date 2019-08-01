#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
import logic             as lg
import gui               as gi

import gettext
import skl_shared.gettext_windows
skl_shared.gettext_windows.setup_env()
gettext.install('unmusic','../resources/locale')


class Commands:
    
    def __init__(self):
        pass
        
    def camel_case(self,title):
        words = title.split(' ')
        for word in words:
            if word != word.upper() and len(word) > 1 \
            and word[0].isalpha():
                for sym in word[1:]:
                    if sym in 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЪЬЭЮЯ':
                        return True
    
    def cyphered(self):
        f = '[unmusic] utils.Commands.cyphered'
        if lg.objs.db().Success:
            titles = []
            try:
                '''
                lg.objs._db.dbc.execute ('select TITLE from TRACKS \
                                          order by ALBUMID'
                                        )
                '''
                lg.objs._db.dbc.execute ('select ALBUM from ALBUMS \
                                          order by ALBUM'
                                        )
                titles = lg.objs._db.dbc.fetchall()
                if titles:
                    titles = [item[0] for item in titles]
            except Exception as e:
                mes = _('Operation has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.mes(f,mes).warning()
            result = [title for title in titles \
                      if self.camel_case(title)
                     ]
            print('\n'.join(result))
            print(len(result))
        else:
            sh.com.cancel(f)
    

com = Commands()


if __name__ == '__main__':
    f = '[unmusic] utils.__main__'
    sh.com.start()
    com.cyphered()
    lg.objs.db().close()
    sh.com.end()
