#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import time
import skl_shared.shared as sh
from skl_shared.localize import _
import logic as lg
import gui as gi


class Copy:
    
    def __init__(self):
        self.set_values()
        self.gui = gi.Copy()
        self.set_bindings()
    
    def update_progress(self,i):
        f = '[unmusic] unmusic.Copy.update_progress'
        if self.Success:
            # Prevent ZeroDivisionError
            if self.ids:
                percent = (100 * (i + 1)) // len(self.ids)
            else:
                percent = 0
            gi.objs.get_progress().item.widget['value'] = percent
            # This is required to fill the progress bar on-the-fly
            sh.objs.get_root().update_idle()
        else:
            sh.com.cancel(f)
    
    def wait_carrier(self,carrier,event=None):
        f = '[unmusic] unmusic.Copy.wait_carrier'
        if self.Success:
            if carrier:
                carrier    = os.path.realpath(carrier)
                carrier_sh = sh.lg.Text(carrier).shorten (max_len = 25
                                                         ,Enclose = True
                                                         ,FromEnd = True
                                                         )
                objs.get_waitbox().reset (func    = f
                                     ,message = _('Waiting for {}').format(carrier_sh)
                                     )
                objs.waitbox.show()
                while not os.path.isdir(carrier):
                    time.sleep(1)
                objs.waitbox.close()    
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel()
    
    def get_settings(self,event=None):
        f = '[unmusic] unmusic.Copy.get_settings'
        if self.Success:
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
                sh.objs.get_mes(f,mes).show_error()
            self.source = lg.objs.get_default().ihome.add_share(self.gui.opt_src.choice)
            self.target = lg.objs.default.ihome.add_share(self.gui.opt_trg.choice)
            self.limit  = sh.lg.Input (title = f
                                       ,value = self.gui.ent_lim.get()
                                       ).get_integer()
        else:
            sh.com.cancel(f)
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()
    
    def set_bindings(self):
        self.gui.btn_str.action = self.start
    
    def set_values(self):
        self.ids    = []
        self.sizes  = []
        self.dirs   = []
        self.query  = ''
        self.source = ''
        self.target = ''
        self.genre  = _('All')
        self.limit  = 100
        self.year   = 0
        self.syear  = 0
        self.eyear  = 0
        # At least 30 MiB should remain free on the target device
        self.minfr   = 31457280
        self.Success = lg.objs.get_db().Success
    
    def confirm(self):
        f = '[unmusic] unmusic.Copy.copy'
        if self.Success:
            total = sum(self.sizes)
            free  = sh.lg.Path(self.target).get_free_space()
            cond  = total and free and total + self.minfr < free
            if cond:
                free = sh.lg.com.get_human_size (bsize     = free
                                                ,LargeOnly = True
                                                )
                total = sh.lg.com.get_human_size(total,LargeOnly=1)
                message  = _('Selected albums: {}').format(len(self.ids))
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
                free = sh.lg.com.get_human_size (bsize     = free
                                                ,LargeOnly = True
                                                )
                bsize = total + self.minfr
                required = sh.lg.com.get_human_size (bsize     = bsize
                                                    ,LargeOnly = True
                                                    )
                message  = _('Not enough free space on "{}"!')
                message  = message.format(self.target)
                message += '\n'
                message += _('Free space: {}').format(free)
                message += '\n'
                message += _('Required: {}').format(required)
                sh.objs.get_mes(f,message).show_warning()
        else:
            sh.com.cancel(f)
    
    def copy(self):
        f = '[unmusic] unmusic.Copy.copy'
        if self.Success:
            if self.confirm():
                sh.Geometry(gi.objs.get_progress().obj).activate()
                gi.objs.progress.add()
                gi.objs.progress.items[-1].label.set_text(_('Copy progress'))
                sh.objs.get_root().update_idle()
                gi.objs.progress.show()
                for i in range(len(self.ids)):
                    myid      = str(self.ids[i])
                    source    = os.path.join(self.source,myid)
                    target    = os.path.join(self.target,myid)
                    source_sh = sh.lg.Text(source).shorten (max_len = 30
                                                           ,FromEnd = True
                                                           )
                    target_sh = sh.lg.Text(target).shorten (max_len = 30
                                                           ,FromEnd = True
                                                           )
                    message = '({}/{}) {} -> {}'.format (i + 1
                                                        ,len(self.ids)
                                                        ,source_sh
                                                        ,target_sh
                                                        )
                    gi.objs.progress.items[-1].label.set_text(message)
                    self.update_progress(i)
                    idir = sh.lg.Directory (path = source
                                           ,dest = target
                                           )
                    idir.copy()
                    if not idir.Success:
                        self.Success = False
                        break
                gi.objs.progress.close()
            else:
                mes = _('Operation has been canceled by the user.')
                sh.objs.get_mes(f,mes,True).show_info()
        else:
            sh.com.cancel(f)
    
    def get_sizes(self):
        f = '[unmusic] unmusic.Copy.get_sizes'
        if self.Success:
            self.sizes = []
            if self.ids:
                objs.get_waitbox().reset (func    = f
                                         ,message = _('Calculate required space')
                                         )
                objs.waitbox.show()
                for myid in self.ids:
                    mydir = os.path.join(self.source,str(myid))
                    idir  = sh.lg.Directory(mydir)
                    self.Success = idir.Success
                    if self.Success:
                        self.sizes.append(idir.get_size())
                    else:
                        sh.com.cancel(f)
                        break
                objs.waitbox.close()
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def select_albums(self):
        f = '[unmusic] unmusic.Copy.select_albums'
        if self.Success:
            if self.ids:
                text = lg.objs.get_db().get_brief(self.ids)
                if text:
                    lst  = text.splitlines()
                    ibox = sh.MultCBoxesC (text    = text
                                          ,MarkAll = True
                                          ,width   = 1024
                                          ,height  = 768
                                          ,icon    = gi.ICON
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
                            sh.objs.get_mes(f,mes).show_error()
                    ids = []
                    for pos in poses:
                        try:
                            ids.append(self.ids[pos])
                        except IndexError:
                            mes = _('Wrong input data!')
                            sh.objs.get_mes(f,mes).show_error()
                    ''' Allow an empty list here to cancel copying if no
                        albums are selected.
                    '''
                    self.ids = ids
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch(self):
        f = '[unmusic] unmusic.Copy.fetch'
        if self.Success:
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
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.cancel(f)
    
    def set_query(self):
        f = '[unmusic] unmusic.Copy.set_query'
        if self.Success:
            ids = lg.objs.get_db().get_rated()
            if ids:
                self.ids = ids
                # We assume that 'self.ids' are already distinct
                self.query = 'select ALBUMID from ALBUMS \
                              where ALBUMID in (%s)' \
                              % ','.join('?'*len(self.ids))
                if self.genre in (_('All'),_('Any')):
                    pass
                elif self.genre == _('Light'):
                    self.query += ' and GENRE in (%s)' \
                                   % ','.join('?'*len(lg.LIGHT))
                elif self.genre == _('Heavy'):
                    self.query += ' and GENRE in (%s)' \
                                   % ','.join('?'*len(lg.HEAVY))
                else:
                    self.Success = False
                    genres = (_('All'),_('Any'),_('Light'),_('Heavy'))
                    mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                    mes = mes.format(self.genre,'; '.join(genres))
                    sh.objs.get_mes(f,mes).show_error()
                ''' If an exact year is set then only this year should
                    be used; otherwise, a starting-ending years range
                    should be used.
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
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = '[unmusic] unmusic.Copy.debug'
        if self.Success:
            if self.ids:
                '''
                mes = '; '.join([str(albumid) for albumid in self.ids])
                sh.objs.get_mes(f,mes,True).show_debug()
                '''
                ids = lg.objs.get_db().get_brief(self.ids)
                ids = ids.splitlines()
                ids.sort()
                sh.fast_txt('\n'.join(ids))
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def start(self,event=None):
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



class Tracks:
    
    def __init__(self):
        self.Active  = False
        self.Success = lg.objs.get_db().Success
        self.gui     = gi.Tracks(height=400)
        self.gui.close()
        self.set_bindings()
    
    def decypher(self,event=None):
        f = '[unmusic] unmusic.Tracks.decypher'
        if self.Success:
            for track in self.gui.tracks:
                title = track.ent_tit.get()
                title = lg.objs.get_caesar().decypher(title)
                track.ent_tit.clear_text()
                track.ent_tit.insert(title)
        else:
            sh.com.cancel(f)
    
    def cypher(self,event=None):
        f = '[unmusic] unmusic.Tracks.cypher'
        if self.Success:
            for track in self.gui.tracks:
                title = track.ent_tit.get()
                title = lg.objs.get_caesar().cypher(title)
                track.ent_tit.clear_text()
                track.ent_tit.insert(title)
        else:
            sh.com.cancel(f)
    
    def decode(self,event=None):
        f = '[unmusic] unmusic.Tracks.decode'
        if self.Success:
            for track in self.gui.tracks:
                title = track.ent_tit.get()
                title = lg.com.decode_back(title)
                track.ent_tit.clear_text()
                track.ent_tit.insert(title)
        else:
            sh.com.cancel(f)
    
    def _dump_search(self,old,new):
        f = '[unmusic] unmusic.Tracks._dump'
        mes = _('Not implemented yet!')
        sh.objs.get_mes(f,mes).show_info()
        return False
    
    def _dump(self,old,new):
        if old and new:
            if len(old) == len(new):
                Dump = False
                for i in range(len(old)):
                    if len(old[i]) == 7 and len(new[i]) == 4:
                        old_record = [old[i][0],old[i][2],old[i][3]
                                     ,old[i][6]
                                     ]
                        new_record = [new[i][0],new[i][1],new[i][2]
                                     ,new[i][3]
                                     ]
                        if old_record != new_record:
                            if new[i][0]:
                                mes = _('Edit #{}.').format(i+1)
                                self.gui.update_info(mes)
                                lg.objs.get_db().update_track (no   = i + 1
                                                          ,data = new_record
                                                          )
                                # We're in loop - do not use 'return'
                                Dump = True
                            else:
                                mes = _('A track title should be indicated.')
                                sh.objs.get_mes(f,mes).show_warning()
                    else:
                        self.Success = False
                        mes = _('Wrong input data!')
                        sh.objs.get_mes(f,mes).show_error()
                return Dump
            else:
                sub = '{} = {}'.format(len(old),len(new))
                mes = _('Condition "{}" is not observed!').format(sub)
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.rep_empty(f)
    
    def dump(self):
        f = '[unmusic] unmusic.Tracks.dump'
        if self.Success:
            if lg.objs.get_db().check_nos():
                Extended = False
                if self.gui.tracks:
                    Extended = self.gui.tracks[0].Extended
                old = lg.objs.db.get_tracks()
                new = self.gui.dump()
                if Extended:
                    return self._dump_search(old,new)
                else:
                    return self._dump(old,new)
            else:
                mes = _('Track numbers should be sequential!')
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.cancel(f)
    
    def save(self,event=None):
        ''' #NOTE: this should be done before 'albumid' is changed,
            otherwise, a wrong DB record will be overwritten!
        '''
        f = '[unmusic] unmusic.Tracks.save'
        if self.Success:
            if self.dump():
                self.gui.update_info(_('Save DB.'))
                lg.objs.get_db().save()
        else:
            sh.com.cancel(f)
    
    def set_bindings(self):
        self.gui.widget.protocol("WM_DELETE_WINDOW",self.close)
        self.gui.btn_cyp.action = self.cypher
        self.gui.btn_dez.action = self.decypher
        self.gui.btn_dec.action = self.decode
        self.gui.btn_rld.action = self.reload
        self.gui.btn_sav.action = self.save
        sh.com.bind (obj      = self.gui.parent
                    ,bindings = ('<F5>','<Control-r>')
                    ,action   = self.reload
                    )
        sh.com.bind (obj      = self.gui.parent
                    ,bindings = ('<F2>','<Control-s>')
                    ,action   = self.save
                    )
        sh.com.bind (obj      = self.gui.parent
                    ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                    ,action   = self.close
                    )
    
    def fill_search(self,data):
        f = '[unmusic] unmusic.Tracks.fill_search'
        if self.Success:
            self.gui.reset()
            if data:
                for i in range(len(data)):
                    self.gui.add(Extended=True)
                    record = data[i]
                    track  = self.gui.tracks[i]
                    if len(record) == 8:
                        track.ent_aid.enable()
                        track.ent_aid.clear_text()
                        track.ent_aid.insert(record[0])
                        track.ent_aid.disable()
                        track.ent_tno.enable()
                        track.ent_tno.clear_text()
                        track.ent_tno.insert(str(record[2]))
                        track.ent_tno.disable()
                        track.ent_tit.clear_text()
                        track.ent_tit.insert(record[1])
                        track.ent_lyr.clear_text()
                        track.ent_lyr.insert(record[3])
                        track.ent_com.clear_text()
                        track.ent_com.insert(record[4])
                        track.ent_bit.enable()
                        track.ent_bit.clear_text()
                        track.ent_bit.insert(str(record[5]//1000)+'k')
                        track.ent_bit.disable()
                        track.ent_len.enable()
                        track.ent_len.clear_text()
                        track.ent_len.insert(sh.lg.com.get_human_time(float(record[6])))
                        track.ent_len.disable()
                        track.opt_rtg.set(record[7])
                    else:
                        self.Success = False
                        mes = _('Wrong input data: "{}"!').format(data)
                        sh.objs.get_mes(f,mes).show_error()
                self.gui.add_after()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def reload(self,event=None):
        self.fill()
        self.show()
    
    def fill(self,event=None):
        f = '[unmusic] unmusic.Tracks.fill'
        if self.Success:
            self.gui.reset()
            data = lg.objs.get_db().get_tracks()
            if data:
                for i in range(len(data)):
                    self.gui.add()
                    mes = _('Load #{}.').format(i+1)
                    self.gui.update_info(mes)
                    record = data[i]
                    track  = self.gui.tracks[i]
                    if len(record) == 7:
                        track.ent_tno.enable()
                        track.ent_tno.clear_text()
                        track.ent_tno.insert(str(record[1]))
                        track.ent_tno.disable()
                        track.ent_tit.clear_text()
                        track.ent_tit.insert(record[0])
                        track.ent_lyr.clear_text()
                        track.ent_lyr.insert(record[2])
                        track.ent_com.clear_text()
                        track.ent_com.insert(record[3])
                        track.ent_bit.enable()
                        track.ent_bit.clear_text()
                        track.ent_bit.insert(str(record[4]//1000)+'k')
                        track.ent_bit.disable()
                        track.ent_len.enable()
                        track.ent_len.clear_text()
                        track.ent_len.insert(sh.lg.com.get_human_time(float(record[5])))
                        track.ent_len.disable()
                        track.opt_rtg.set(record[6])
                    else:
                        self.Success = False
                        mes = _('Wrong input data: "{}"!').format(data)
                        sh.objs.get_mes(f,mes).show_error()
                self.gui.add_after()
            else:
                mes = _('No tracks are associated with this album.')
                sh.objs.get_mes(f,mes).show_info()
        else:
            sh.com.cancel(f)
    
    def show(self,event=None):
        self.Active = True
        self.gui.show()
    
    def close(self,event=None):
        self.Active = False
        self.gui.close()



class AlbumEditor:
    
    def __init__(self):
        self.set_values()
        self.gui   = gi.AlbumEditor()
        self.logic = lg.AlbumEditor()
        self.set_bindings()
        
    def go_prev_unrated(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.go_prev_unrated'
        if self.Success:
            self.save()
            self.logic.get_prev_rated()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def go_next_unrated(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.go_next_unrated'
        if self.Success:
            self.save()
            self.logic.get_next_rated()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def update_presence(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.update_presence'
        if self.Success:
            local     = lg.objs.get_default().ihome.add_share(_('local collection'))
            external  = lg.objs.default.ihome.add_share(_('external collection'))
            mobile    = lg.objs.default.ihome.add_share(_('mobile collection'))
            plocal    = os.path.join(local,str(lg.objs.get_db().albumid))
            pexternal = os.path.join(external,str(lg.objs.db.albumid))
            pmobile   = os.path.join(mobile,str(lg.objs.db.albumid))
            if os.path.exists(plocal):
                self.gui.cbx_loc.enable()
                self.gui.lbl_loc.enable()
            else:
                self.gui.cbx_loc.disable()
                self.gui.lbl_loc.disable()
            if os.path.exists(pexternal):
                self.gui.cbx_ext.enable()
                self.gui.lbl_ext.enable()
            else:
                self.gui.cbx_ext.disable()
                self.gui.lbl_ext.disable()
            if os.path.exists(pmobile):
                self.gui.cbx_mob.enable()
                self.gui.lbl_mob.enable()
            else:
                self.gui.cbx_mob.disable()
                self.gui.lbl_mob.disable()
        else:
            sh.com.cancel(f)
    
    def set_genre(self,genre):
        f = '[unmusic] unmusic.AlbumEditor.set_genre'
        if self.Success:
            genre = str(genre)
            if not genre:
                # Do not localize (being stored in DB)
                genre = '?'
            items = list(lg.GENRES)
            if not genre in items:
                items.append(genre)
            self.gui.opt_gnr.reset (items   = items
                                   ,default = genre
                                   )
        else:
            sh.com.cancel(f)
    
    def go_end(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.go_end'
        if self.Success:
            ''' #NOTE: If we change 'albumid' BEFORE saving, then
                a wrong DB record will be overwritten!
            '''
            self.save()
            albumid = lg.objs.get_db().get_max_id()
            if albumid:
                lg.objs.db.albumid = albumid
                self.fill()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def go_start(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.go_start'
        if self.Success:
            ''' #NOTE: If we change 'albumid' BEFORE saving, then
                a wrong DB record will be overwritten!
            '''
            self.save()
            albumid = lg.objs.get_db().get_min_id()
            if albumid:
                lg.objs.db.albumid = albumid
                self.fill()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def search_id(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.search_id'
        if self.Success:
            ''' #NOTE: If we change 'albumid' BEFORE saving, then
                a wrong DB record will be overwritten!
            '''
            self.save()
            albumid = self.gui.ent_ids.get()
            if albumid:
                if str(albumid).isdigit():
                    albumid = int(albumid)
                    if albumid > 0:
                        data = lg.objs.get_db().has_id(albumid)
                        if data:
                            lg.objs.db.albumid = albumid
                            self.fill()
                        else:
                            mes = _('No matches!')
                            sh.objs.get_mes(f,mes).show_info()
                    else:
                        mes = _('Wrong input data: "{}"!')
                        mes = mes.format(albumid)
                        sh.objs.get_mes(f,mes).show_warning()
                else:
                    mes = _('Wrong input data: "{}"!')
                    mes = mes.format(albumid)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def cypher(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.cypher'
        if self.Success:
            artist  = self.gui.ent_art.get()
            album   = self.gui.ent_alb.get()
            genre   = self.gui.opt_gnr.choice
            artist  = lg.objs.get_caesar().cypher(artist)
            album   = lg.objs.caesar.cypher(album)
            genre   = lg.objs.caesar.cypher(genre)
            self.gui.ent_art.clear_text()
            self.gui.ent_art.insert(artist)
            self.gui.ent_alb.clear_text()
            self.gui.ent_alb.insert(album)
            self.set_genre(genre)
        else:
            sh.com.cancel(f)
    
    def decypher(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.decypher'
        if self.Success:
            artist = self.gui.ent_art.get()
            album  = self.gui.ent_alb.get()
            genre  = self.gui.opt_gnr.choice
            artist = lg.objs.get_caesar().decypher(artist)
            album  = lg.objs.caesar.decypher(album)
            genre  = lg.objs.caesar.decypher(genre)
            self.gui.ent_art.clear_text()
            self.gui.ent_art.insert(artist)
            self.gui.ent_alb.clear_text()
            self.gui.ent_alb.insert(album)
            self.set_genre(genre)
        else:
            sh.com.cancel(f)
    
    def decode(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.decode'
        if self.Success:
            artist  = self.gui.ent_art.get()
            album   = self.gui.ent_alb.get()
            comment = self.gui.ent_com.get()
            artist  = lg.com.decode_back(artist)
            album   = lg.com.decode_back(album)
            comment = lg.com.decode_back(comment)
            self.gui.ent_art.clear_text()
            self.gui.ent_art.insert(artist)
            self.gui.ent_alb.clear_text()
            self.gui.ent_alb.insert(album)
            self.gui.ent_com.clear_text()
            self.gui.ent_com.insert(comment)
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.defimg   = None
        self.image    = None
        self.defpath = sh.objs.get_pdir().add('..','resources','cd.png')
    
    def get_default_image(self):
        if not self.defimg:
            self.defimg = sh.Image().open(self.defpath)
        return self.defimg
        
    def zoom_image(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.zoom_image'
        if self.Success:
            if self.image:
                viewer = gi.ImageViewer()
                viewer.lbl.widget.config(image=self.image)
                viewer.lbl.widget.image = self.image
                viewer.show()
            else:
                # This should not happen
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_image(self,image):
        f = '[unmusic] unmusic.AlbumEditor.set_image'
        if self.Success:
            if image:
                try:
                    ipic = sh.Image()
                    ipic.bytes_ = image
                    ipic.get_loader()
                    self.image = ipic.get_image()
                    ipic = sh.Image()
                    ipic.bytes_ = image
                    ipic.get_loader()
                    ''' These are dimensions of 'self.gui.frm_img' when
                        the default image is loaded.
                    '''
                    ipic.get_thumbnail(130,212)
                    thumb = ipic.get_image()
                except Exception as e:
                    ''' Do not fail 'Success' here - it can just be
                        an incorrectly ripped image.
                    '''
                    thumb = None
                    mes = _('Third-party module has failed!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                self.image = self.get_default_image()
                thumb = self.image
            self.gui.lbl_img.widget.config(image=thumb)
            # Prevent the garbage collector from deleting the image
            self.gui.lbl_img.widget.image = thumb
        else:
            sh.com.cancel(f)
    
    def play(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.play'
        if self.Success:
            choice = self.gui.opt_ply.choice
            default = _('Play')
            if choice == default:
                sh.com.rep_lazy(f)
            elif choice == _('All'):
                self.gui.opt_ply.set(default)
                lg.Play().play_all_tracks()
            elif choice == _('Good'):
                self.gui.opt_ply.set(default)
                lg.Play().play_good_tracks()
            elif choice == _('Best'):
                self.gui.opt_ply.set(default)
                lg.Play().play_good_tracks(9)
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(choice,';'.join(gi.PLAY))
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.cancel(f)
    
    def get_length(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.get_length'
        if self.Success:
            total = lg.objs.get_db().get_length()
            if total:
                mes = _('{} ({} tracks)')
                mes = mes.format (sh.lg.com.get_human_time(sum(total))
                                 ,len(total)
                                 )
            else:
                mes = '?'
            self.gui.ent_len.enable()
            self.gui.ent_len.clear_text()
            self.gui.ent_len.insert(mes)
            self.gui.ent_len.disable()
        else:
            sh.com.cancel(f)
    
    def get_bitrate(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.get_bitrate'
        if self.Success:
            mean = self.logic.get_mean_bitrate()
            if mean:
                mes = '%dk' % (mean // 1000)
            else:
                mes = '?'
            self.gui.ent_bit.enable()
            self.gui.ent_bit.clear_text()
            self.gui.ent_bit.insert(mes)
            self.gui.ent_bit.disable()
        else:
            sh.com.cancel(f)
    
    def get_rating(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.get_rating'
        if self.Success:
            rating = self.logic.get_mean_rating()
            if isinstance(rating,float):
                ''' If an album has more songs with rating X that with
                    rating Y, we should consider that the album has
                    an overall rating of X. Thus, we use 'round' instead
                    of 'int'.
                '''
                self.gui.opt_rtg.set(round(rating))
            elif rating is None:
                sh.com.rep_empty(f)
            else:
                mes = _('Wrong input data: "{}"!').format(rating)
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.cancel(f)
    
    def _set_rating(self):
        f = '[unmusic] unmusic.AlbumEditor._set_rating'
        value = sh.lg.Input(f,self.gui.opt_rtg.choice).get_integer()
        lg.objs.db.set_rating(value)
    
    def set_rating(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.set_rating'
        if self.Success:
            rating = self.logic.get_mean_rating()
            if isinstance(rating,float):
                mes = _('Tracks are of a mixed rating. Do you want to assign the same rating to all of them?')
                if rating == int(rating):
                    self._set_rating()
                elif sh.objs.get_mes(f,mes).show_question():
                    self._set_rating()
                else:
                    self.get_rating()
            elif rating is None:
                sh.com.rep_empty(f)
            else:
                mes = _('Wrong input data: "{}"!').format(rating)
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.cancel(f)
    
    def dump(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.dump'
        if self.Success:
            old = lg.objs.get_db().get_album()
            if old:
                new = self.gui.dump()
                # '-1' since we don't dump IMAGE field
                if len(old) - 1 == len(new):
                    old = list(old)
                    new = list(new)
                    old = old[:-1]
                    if [item for item in new if item]:
                        if not new[0]:
                            mes = _('An album title should be indicated.')
                            sh.objs.get_mes(f,mes).show_warning()
                            if old[0]:
                                new[0] = old[0]
                            else:
                                # Do not localize (being stored in DB)
                                new[0] = '?'
                        if not new[1]:
                            mes = _('An artist should be indicated.')
                            sh.objs.get_mes(f,mes).show_warning()
                            if old[1]:
                                new[1] = old[1]
                            else:
                                # Do not localize (being stored in DB)
                                new[1] = '?'
                        # Do not warn if a year is not set
                        if new[2]:
                            new[2] = sh.lg.Input(f,new[2]).get_integer()
                        else:
                            # We need to return integer anyway
                            new[2] = old[2]
                        if old == new:
                            mes = _('No changes!')
                            sh.objs.get_mes(f,mes,True).show_info()
                        else:
                            mes = _('Some fields have been updated.')
                            sh.objs.get_mes(f,mes,True).show_info()
                            query = self.logic._compare_albums(old,new)
                            lg.objs.db.updateDB(query)
                            return query
                    else:
                        sh.com.rep_empty(f)
                else:
                    sub = '{} = {}'.format(len(old)-1,len(new))
                    mes = _('The condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.get_mes(f,mes).show_error()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def search_track(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.search_track'
        if self.Success:
            pattern = self.gui.ent_sr2.get()
            if pattern:
                data = lg.objs.get_db().search_track(pattern)
                if data:
                    objs.get_tracks().fill_search(data=data)
                    objs.tracks.show()
                else:
                    mes = _('No matches!')
                    sh.objs.get_mes(f,mes).show_info()
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def search_album(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.search_album'
        if self.Success:
            self.save()
            old = lg.objs.get_db().albumid
            # Not 1, because we use '<' and '>' in search
            lg.objs.db.albumid = 0
            self.search_next_album(Save=False)
            if lg.objs.db.albumid == 0:
                lg.objs.db.albumid = old
        else:
            sh.com.cancel(f)
    
    def search_next_album(self,event=None,Save=True):
        f = '[unmusic] unmusic.AlbumEditor.search_next_album'
        if self.Success:
            ''' #NOTE: If we change 'albumid' BEFORE saving, then
                a wrong DB record will be overwritten! Since
                'self.search_album' is generally a wrapper over this
                procedure and changes 'albumid', we should be careful
                about this.
            '''
            if Save:
                self.save()
            pattern = self.gui.ent_src.get()
            if pattern:
                old     = lg.objs.get_db().albumid
                albumid = lg.objs.db.get_next_album(pattern)
                if albumid:
                    lg.objs.db.albumid = albumid
                    self.fill()
                else:
                    lg.objs.db.albumid = old
                    mes = _('No matches!')
                    sh.objs.get_mes(f,mes).show_info()
            else:
                self.gui.btn_spr.inactivate()
                self.gui.btn_snx.inactivate()
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def search_prev_album(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.search_prev_album'
        if self.Success:
            ''' #NOTE: Make sure that actual 'albumid' is not changed
                prior to 'self.search_prev_album'.
            '''
            self.save()
            pattern = self.gui.ent_src.get()
            if pattern:
                old     = lg.objs.get_db().albumid
                albumid = lg.objs.db.get_prev_album(pattern)
                if albumid:
                    lg.objs.db.albumid = albumid
                    self.fill()
                else:
                    lg.objs.db.albumid = old
                    mes = _('No matches!')
                    sh.objs.get_mes(f,mes).show_info()
            else:
                self.gui.btn_spr.inactivate()
                self.gui.btn_snx.inactivate()
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def go_prev(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.go_prev'
        if self.Success:
            self.save()
            self.logic.dec()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def go_next(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.go_next'
        if self.Success:
            self.save()
            self.logic.inc()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def show_tracks(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.show_tracks'
        if self.Success:
            objs.get_tracks().fill()
            if objs.tracks.gui.tracks:
                objs.tracks.show()
        else:
            sh.com.cancel(f)
    
    def delete(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.delete'
        if self.Success:
            mes = _('Are you sure you want to permanently delete record #{}?')
            mes = mes.format(lg.objs.get_db().albumid)
            if sh.objs.get_mes(f,mes).show_question():
                mes = _('Delete #{}.').format(lg.objs.db.albumid)
                self.gui.update_info(text=mes)
                lg.objs.db.delete()
                lg.objs.db.albumid = self.logic.get_max()
                self.fill()
        else:
            sh.com.cancel(f)
    
    def save(self,event=None):
        ''' #NOTE: this should be done before 'albumid' is changed,
            otherwise, a wrong DB record will be overwritten!
        '''
        f = '[unmusic] unmusic.AlbumEditor.save'
        if self.Success:
            if self.dump():
                self.gui.update_info(_('Save DB.'))
                lg.objs.get_db().save()
        else:
            sh.com.cancel(f)
    
    def create(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.create'
        if self.Success:
            lg.objs.get_db().add_album(('?','?',2000,'?','','',''))
            lg.objs.db.albumid = self.logic.get_max()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def set_bindings(self):
        self.gui.widget.protocol("WM_DELETE_WINDOW",self.close)
        self.gui.btn_cyp.action = self.cypher
        self.gui.btn_dec.action = self.decode
        self.gui.btn_del.action = self.delete
        self.gui.btn_dez.action = self.decypher
        self.gui.btn_nxt.action = self.go_next
        self.gui.btn_prv.action = self.go_prev
        self.gui.btn_rec.action = self.create
        self.gui.btn_rld.action = self.fill
        self.gui.btn_sav.action = self.save
        self.gui.btn_snx.action = self.search_next_album
        self.gui.btn_spr.action = self.search_prev_album
        self.gui.btn_trk.action = self.show_tracks
        self.gui.opt_rtg.action = self.set_rating
        self.gui.opt_ply.action = self.play
        sh.com.bind (obj      = self.gui
                    ,bindings = '<Alt-n>'
                    ,action   = self.go_next_unrated
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = '<Alt-p>'
                    ,action   = self.go_prev_unrated
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = ('<F5>','<Control-r>')
                    ,action   = self.fill
                    )
        sh.com.bind (obj      = self.gui.ent_ids
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.search_id
                    )
        sh.com.bind (obj      = self.gui.ent_src
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.search_album
                    )
        sh.com.bind (obj      = self.gui.ent_sr2
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.search_track
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = ('<F2>','<Control-s>')
                    ,action   = self.save
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = ('<F4>','<Control-t>','<Alt-t>')
                    ,action   = self.show_tracks
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = '<Control-n>'
                    ,action   = self.create
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = '<Alt-Left>'
                    ,action   = self.go_prev
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = '<Alt-Right>'
                    ,action   = self.go_next
                    )
        sh.com.bind (obj      = self.gui.lbl_img
                    ,bindings = '<ButtonRelease-1>'
                    ,action   = self.zoom_image
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = '<Alt-Home>'
                    ,action   = self.go_start
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = '<Alt-End>'
                    ,action   = self.go_end
                    )
    
    def reset(self):
        f = '[unmusic] unmusic.AlbumEditor.reset'
        self.Success = self.logic.Success = lg.objs.get_db().Success
        lg.objs.db.albumid = self.logic.get_max()
        self.fill()
    
    def update_album_search(self):
        f = '[unmusic] unmusic.AlbumEditor.update_album_search'
        if self.Success:
            pattern = self.gui.ent_src.get()
            self.gui.btn_spr.inactivate()
            self.gui.btn_snx.inactivate()
            if pattern:
                albumid = lg.objs.db.get_next_album(pattern)
                if albumid:
                    self.gui.btn_snx.activate()
                albumid = lg.objs.db.get_prev_album(pattern)
                if albumid:
                    self.gui.btn_spr.activate()
        else:
            sh.com.cancel(f)
    
    def update_meter(self):
        f = '[unmusic] unmusic.AlbumEditor.update_meter'
        if self.Success:
            max_ = self.logic.get_max()
            self.gui.lbl_mtr.set_text ('{} / {}'.format (self.logic.get_no()
                                                        ,max_
                                                        )
                                      )
            if lg.objs.get_db().albumid < max_:
                self.gui.btn_nxt.activate()
            else:
                self.gui.btn_nxt.inactivate()
            if lg.objs.db.albumid == self.logic.get_min():
                self.gui.btn_prv.inactivate()
            else:
                self.gui.btn_prv.activate()
        else:
            sh.com.cancel(f)
    
    def update(self):
        f = '[unmusic] unmusic.AlbumEditor.update'
        if self.Success:
            self.update_meter()
            self.update_album_search()
            self.update_presence()
        else:
            sh.com.cancel(f)
    
    def fill(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.fill'
        if self.Success:
            self.logic.get_no()
            data = lg.objs.get_db().get_album()
            if data:
                if len(data) == 7:
                    mes = _('Load #{}.').format(lg.objs.db.albumid)
                    self.gui.update_info(mes)
                    self.gui.clear_entries()
                    self.gui.ent_alb.insert(data[0])
                    self.gui.ent_art.insert(data[1])
                    self.gui.ent_yer.insert(data[2])
                    genre = data[3]
                    self.set_genre(genre)
                    self.gui.ent_cnt.insert(data[4])
                    self.gui.ent_com.insert(data[5])
                    self.get_rating()
                    self.get_bitrate()
                    self.get_length()
                    self.set_image(data[6])
                    self.update()
                    if objs.get_tracks().Active:
                        objs.tracks.reload()
                else:
                    mes = _('Wrong input data: "{}"!').format(data)
                    sh.objs.get_mes(f,mes).show_error()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()



class Menu:
    
    def __init__(self):
        self.gui = gi.Menu()
        self.set_bindings()
    
    def delete_bad(self,event=None):
        f = '[unmusic] unmusic.Menu.delete_bad'
        ibad = lg.BadMusic()
        objs.get_waitbox().reset (func    = f
                                 ,message = _('Calculate ratings')
                                 )
        objs.waitbox.show()
        data = ibad.get_rates()
        objs.waitbox.close()
        if data:
            mes = _('Insert all required media to calculate space to be freed.\n\nContinue?')
            ques = sh.objs.get_mes(f,mes).show_question()
            if ques:
                objs.waitbox.reset (func    = f
                                   ,message = _('Calculate sizes')
                                   )
                objs.waitbox.show()
                ibad.get_sizes()
                objs.waitbox.close()
                ibad.report()
                if ibad.sizes:
                    sizes = [item for item in ibad.sizes if item]
                    total_size = 0
                    for item in sizes:
                        total_size += item
                    total_size = sh.com.get_human_size (bsize     = total_size
                                                       ,LargeOnly = True
                                                       )
                    affected = ibad.get_affected_carriers()
                    if affected:
                        affected = ', '.join(affected)
                    else:
                        affected = _('N/A')
                    mes = _('Affected carriers: {}.\nSpace to be freed: {}.\nNumber of albums to delete: {}.\nThe list of directories to be deleted is below. Continue?\n\n{}')
                    mes = mes.format (affected
                                     ,total_size
                                     ,len(ibad.dellst)
                                     ,'\n'.join(ibad.dellst)
                                     )
                    ques = sh.objs.get_mes(f,mes).show_question()
                    if ques:
                        objs.waitbox.reset (func    = f
                                           ,message = _('Delete albums')
                                           )
                        objs.waitbox.show()
                        ibad.delete()
                        objs.waitbox.close()
                    else:
                        mes = _('Operation has been canceled by the user.')
                        sh.objs.get_mes(f,mes,True).show_info()
                else:
                    sh.com.rep_empty(f)
            else:
                mes = _('Operation has been canceled by the user.')
                sh.objs.get_mes(f,mes,True).show_info()
        else:
            mes = _('Nothing to do!')
            sh.objs.get_mes(f,mes).show_info()
        
    def copy(self,event=None):
        objs.get_copy().show()
    
    def album_editor(self,event=None):
        objs.get_editor().reset()
        objs.editor.show()
    
    def collect(self,event=None):
        ''' If an artist and/or album title were changed and originally
            were not empty, there is no easy way to tell if we are
            dealing with the same album or not. So, it's best to add
            tags to DB only once.
        '''
        f = '[unmusic] unmusic.Menu.collect'
        folder = sh.lg.Home(app_name='unmusic').add_share(_('not processed'))
        if sh.lg.Path(folder).create():
            iwalk = lg.Walker(folder)
            dirs  = iwalk.get_dirs()
            if dirs:
                count = 0
                timer = sh.lg.Timer(f)
                timer.start()
                for folder in dirs:
                    if lg.objs.get_db().Success:
                        count += 1
                        basename = sh.lg.Path(folder).get_basename()
                        itext = sh.lg.Text(basename)
                        itext.delete_unsupported()
                        itext.shorten(max_len=15)
                        mes = _('Process "{}" ({}/{})')
                        mes = mes.format (itext.text
                                         ,count
                                         ,len(dirs)
                                         )
                        gi.objs.get_wait().reset (func    = f
                                                 ,message = mes
                                                 )
                        gi.objs.wait.show()
                        lg.Directory(folder).run()
                        ''' In case something went wrong, we should
                            lose only 1 album record, not the entire
                            sequence.
                        '''
                        lg.objs.get_db().save()
                    else:
                        sh.com.cancel(f)
                gi.objs.get_wait().close()
                delta = timer.end()
                mes = _('Operation has taken {}')
                mes = mes.format(sh.lg.com.get_human_time(delta))
                sh.objs.get_mes(f,mes).show_info()
                objs.get_editor().reset()
                objs.editor.show()
            else:
                sh.com.rep_empty(f)
            iwalk.delete_empty()
            lg.objs.get_db().save()
        else:
            sh.com.cancel(f)
    
    def prepare(self,event=None):
        f = '[unmusic] unmusic.Menu.prepare'
        mes = _('Not implemented yet!')
        sh.objs.get_mes(f,mes).show_info()
    
    def set_bindings(self):
        self.gui.a[0].action = self.album_editor
        self.gui.a[1].action = self.prepare
        self.gui.a[2].action = self.collect
        self.gui.a[3].action = self.copy
        self.gui.a[4].action = self.delete_bad
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()



class Objects:
    
    def __init__(self):
        self.editor = self.tracks = self.copy_ = self.waitbox = None
    
    def get_waitbox(self):
        if self.waitbox is None:
            self.waitbox = sh.WaitBox(gi.ICON)
        return self.waitbox
    
    def get_copy(self):
        if self.copy_ is None:
            self.copy_ = Copy()
        return self.copy_
    
    def get_editor(self):
        if self.editor is None:
            self.editor = AlbumEditor()
        return self.editor
    
    def get_tracks(self):
        if self.tracks is None:
            self.tracks = Tracks()
        return self.tracks


objs = Objects()



if __name__ == '__main__':
    f = '[unmusic] unmusic.__main__'
    sh.com.start()
    Menu().show()
    lg.objs.get_db().save()
    lg.objs.db.close()
    mes = _('Goodbye!')
    sh.objs.get_mes(f,mes,True).show_debug()
    sh.com.end()
