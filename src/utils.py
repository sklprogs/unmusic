#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg
import logic     as lg
import gui       as gi

import gettext, gettext_windows
gettext_windows.setup_env()
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
                sh.objs.mes (f,_('WARNING')
                            ,_('Operation has failed!\n\nDetails: %s')\
                            % str(e)
                            )
            result = [title for title in titles \
                      if self.camel_case(title)
                     ]
            print('\n'.join(result))
            print(len(result))
        else:
            sh.com.cancel(f)
    

com = Commands()


if __name__ == '__main__':
    f = 'tests.__main__'
    sg.objs.start()
    com.cyphered()
    lg.objs.db().close()
    sg.objs.end()
