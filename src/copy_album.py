#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import time

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import config as cf
import logic as lg
import gui.albums as ga
import gui.tracks as gt


class Copy:
    
    def __init__(self):
        self.set_values()
        self.gui = gi.Copy()
        self.set_bindings()
    
    def wait_carrier(self, carrier):
        f = '[unmusic] album_editor.controller.Copy.wait_carrier'
        if not self.Success:
            sh.com.cancel()
            return
        if not carrier:
            sh.com.rep_empty(f)
            return
        carrier = os.path.realpath(carrier)
        carrier_sh = sh.lg.Text(carrier).shorten (max_len = 25
                                                 ,encloser = '"'
                                                 ,FromEnd = True
                                                 )
        mes = _('Waiting for {}').format(carrier_sh)
        objs.get_waitbox().reset (func = f
                                 ,message = mes
                                 )
        objs.waitbox.show()
        while not os.path.isdir(carrier):
            time.sleep(1)
        objs.waitbox.close()
    
    def get_settings(self):
        f = '[unmusic] album_editor.controller.Copy.get_settings'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.genre = self.gui.opt_gnr.choice
        if self.gui.opt_yer.choice == _('Not set'):
            pass
        elif self.gui.opt_yer.choice == '=':
            self.year = sh.lg.Input (title = f
                                    ,value = self.gui.ent_yer.get()
                                    ).get_integer()
        elif self.gui.opt_yer.choice == '>=':
            self.syear = sh.lg.Input (title = f
                                      ,value = self.gui.ent_yer.get()
                                      ).get_integer()
        elif self.gui.opt_yer.choice == '<=':
            self.eyear = sh.lg.Input (title = f
                                      ,value = self.gui.ent_yer.get()
                                      ).get_integer()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format (self.gui.opt_yer.choice
                             ,'; '.join(gi.ITEMS_YEAR)
                             )
            sh.objs.get_mes(f, mes).show_error()
        self.source = cf.objs.get_paths().ihome.add_share(self.gui.opt_src.choice)
        self.target = lg.objs.default.ihome.add_share(self.gui.opt_trg.choice)
        self.limit = sh.lg.Input (title = f
                                 ,value = self.gui.ent_lim.get()
                                 ).get_integer()
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()
    
    def set_bindings(self):
        self.gui.btn_str.action = self.start
    
    def set_values(self):
        self.ids = []
        self.sizes = []
        self.dirs = []
        self.query = ''
        self.source = ''
        self.target = ''
        self.genre = _('All')
        self.limit = 100
        self.year = 0
        self.syear = 0
        self.eyear = 0
        # At least 30 MiB should remain free on the target device
        self.minfr = 31457280
        self.Success = lg.objs.get_db().Success
    
    def confirm(self):
        f = '[unmusic] album_editor.controller.Copy.copy'
        if not self.Success:
            sh.com.cancel(f)
            return
        total = sum(self.sizes)
        free = sh.lg.Path(self.target).get_free_space()
        cond = total and free and total + self.minfr < free
        if cond:
            free = sh.lg.com.get_human_size (bsize = free
                                            ,LargeOnly = True
                                            )
            total = sh.lg.com.get_human_size(total,LargeOnly=1)
            message = _('Selected albums: {}').format(len(self.ids))
            message += '\n'
            message += _('Total size: {}').format(total)
            message += '\n'
            message += _('Free space: {}').format(free)
            message += '\n\n'
            message += _('Continue?')
            return sh.objs.get_mes(f,message).show_question()
        elif not total:
            # Do not fail here since we may change settings after
            sh.com.rep_lazy(f)
        else:
            free = sh.lg.com.get_human_size (bsize = free
                                            ,LargeOnly = True
                                            )
            bsize = total + self.minfr
            required = sh.lg.com.get_human_size (bsize = bsize
                                                ,LargeOnly = True
                                                )
            message = _('Not enough free space on "{}"!')
            message = message.format(self.target)
            message += '\n'
            message += _('Free space: {}').format(free)
            message += '\n'
            message += _('Required: {}').format(required)
            sh.objs.get_mes(f,message).show_warning()
    
    def copy(self):
        f = '[unmusic] album_editor.controller.Copy.copy'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.confirm():
            mes = _('Operation has been canceled by the user.')
            sh.objs.get_mes(f, mes, True).show_info()
            return
        gi.objs.progress.show()
        for i in range(len(self.ids)):
            myid = str(self.ids[i])
            source = os.path.join(self.source,myid)
            target = os.path.join(self.target,myid)
            source_sh = sh.lg.Text(source).shorten (max_len = 30
                                                   ,FromEnd = True
                                                   )
            target_sh = sh.lg.Text(target).shorten (max_len = 30
                                                   ,FromEnd = True
                                                   )
            message = f'({i + 1}/{len(self.ids)}) {source_sh} -> {target_sh}'
            gi.objs.progress.set_text(message)
            gi.objs.progress.update(i, len(self.ids))
            idir = sh.lg.Directory (path = source
                                   ,dest = target
                                   )
            idir.copy()
            if not idir.Success:
                self.Success = False
                break
        gi.objs.progress.close()
    
    def get_sizes(self):
        f = '[unmusic] album_editor.controller.Copy.get_sizes'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.sizes = []
        if not self.ids:
            sh.com.rep_lazy(f)
            return
        gi.objs.get_progress().set_text(_('Calculate required space'))
        gi.objs.progress.show()
        for i in range(len(self.ids)):
            gi.objs.progress.update(i, len(self.ids))
            mydir = os.path.join(self.source, str(self.ids[i]))
            idir = sh.lg.Directory(mydir)
            self.Success = idir.Success
            if self.Success:
                self.sizes.append(idir.get_size())
            else:
                sh.com.cancel(f)
                break
        gi.objs.progress.close()
    
    def select_albums(self):
        f = '[unmusic] album_editor.controller.Copy.select_albums'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.ids:
            sh.com.rep_empty(f)
            return
        text = lg.objs.get_db().get_brief(self.ids)
        if not text:
            sh.com.rep_empty(f)
            return
        lst = text.splitlines()
        ibox = sh.MultCBoxesC (text = text
                              ,MarkAll = True
                              ,width = 1024
                              ,height = 768
                              ,icon = gi.ICON
                              )
        ibox.show()
        # Always a list
        selected = ibox.get_selected()
        poses = []
        for item in selected:
            try:
                poses.append(lst.index(item))
            except ValueError:
                self.Success = False
                mes = _('Wrong input data!')
                sh.objs.get_mes(f, mes).show_error()
        ids = []
        for pos in poses:
            try:
                ids.append(self.ids[pos])
            except IndexError:
                mes = _('Wrong input data!')
                sh.objs.get_mes(f, mes).show_error()
        # Allow an empty list here to cancel copying if no albums are selected
        self.ids = ids
    
    def fetch(self):
        f = '[unmusic] album_editor.controller.Copy.fetch'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            if self.genre == _('Light'):
                lst = list(self.ids) + list(lg.LIGHT)
            elif self.genre == _('Heavy'):
                lst = list(self.ids) + list(lg.HEAVY)
            else:
                lst = list(self.ids)
            lg.objs.get_db().dbc.execute(self.query,lst)
            result = lg.objs.db.dbc.fetchall()
            if result:
                self.ids = [item[0] for item in result]
            else:
                sh.com.rep_empty(f)
                self.Success = False
        except Exception as e:
            self.Success = False
            mes = _('Operation has failed!\n\nDetails: {}')
            mes = mes.format(e)
            sh.objs.get_mes(f, mes).show_error()
    
    def set_query(self):
        f = '[unmusic] album_editor.controller.Copy.set_query'
        if not self.Success:
            sh.com.cancel(f)
            return
        ids = lg.objs.get_db().get_rated()
        if not ids:
            sh.com.rep_empty(f)
            return
        self.ids = ids
        # We assume that 'self.ids' are already distinct
        self.query = 'select ALBUMID from ALBUMS where ALBUMID in (%s)' \
                      % ','.join('?'*len(self.ids))
        if self.genre in (_('All'),_('Any')):
            pass
        elif self.genre == _('Light'):
            self.query += ' and GENRE in (%s)' % ','.join('?' * len(lg.LIGHT))
        elif self.genre == _('Heavy'):
            self.query += ' and GENRE in (%s)' % ','.join('?' * len(lg.HEAVY))
        else:
            self.Success = False
            genres = (_('All'), _('Any'), _('Light'), _('Heavy'))
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(self.genre, '; '.join(genres))
            sh.objs.get_mes(f, mes).show_error()
        ''' If an exact year is set then only this year should be used;
            otherwise, a starting-ending years range should be used.
        '''
        if self.year:
            self.query += ' and YEAR = %d' % self.year
        else:
            if self.syear:
                self.query += ' and YEAR >= %d' % self.syear
            if self.eyear:
                self.query += ' and YEAR <= %d' % self.eyear
        self.query += ' order by ALBUMID'
        if self.limit:
            self.query += ' limit %d' % self.limit
    
    def debug(self):
        f = '[unmusic] album_editor.controller.Copy.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.ids:
            sh.com.rep_empty(f)
            return
        '''
        mes = '; '.join([str(albumid) for albumid in self.ids])
        sh.objs.get_mes(f, mes, True).show_debug()
        '''
        ids = lg.objs.get_db().get_brief(self.ids)
        ids = ids.splitlines()
        ids.sort()
        sh.fast_txt('\n'.join(ids))
    
    def start(self):
        # Do not reset GUI here
        self.set_values()
        self.get_settings()
        self.wait_carrier(self.source)
        self.wait_carrier(self.target)
        self.set_query()
        self.fetch()
        self.select_albums()
        self.get_sizes()
        self.copy()
