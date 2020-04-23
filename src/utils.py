#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
import logic             as lg
import gui               as gi
from skl_shared.localize import _


class Commands:
    
    def __init__(self):
        pass
        
    def is_camel_case(self,title):
        words = title.split(' ')
        for word in words:
            if word != word.upper() and len(word) > 1 \
            and word[0].isalpha():
                for sym in word[1:]:
                    if sym in 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЪЬЭЮЯ':
                        return True
    
    def show_cyphered(self):
        f = '[unmusic] utils.Commands.show_cyphered'
        if lg.objs.get_db().Success:
            titles = []
            try:
                '''
                lg.objs.db.dbc.execute ('select TITLE from TRACKS \
                                         order by ALBUMID'
                                       )
                '''
                lg.objs.db.dbc.execute ('select ALBUM from ALBUMS \
                                         order by ALBUM'
                                       )
                titles = lg.objs.db.dbc.fetchall()
                if titles:
                    titles = [item[0] for item in titles]
            except Exception as e:
                mes = _('Operation has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.get_mes(f,mes).show_warning()
            result = [title for title in titles \
                      if self.is_camel_case(title)
                     ]
            print('\n'.join(result))
            print(len(result))
        else:
            sh.com.cancel(f)
    

com = Commands()


if __name__ == '__main__':
    f = '[unmusic] utils.__main__'
    sh.com.start()
    com.show_cyphered()
    lg.objs.get_db().close()
    sh.com.end()
