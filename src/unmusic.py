#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import time
import skl_shared.shared as sh
import logic             as lg
import gui               as gi

import gettext
import skl_shared.gettext_windows
skl_shared.gettext_windows.setup_env()
gettext.install('unmusic','../resources/locale')


class Copy:
    
    def __init__(self):
        self.values()
        self.gui = gi.Copy()
        self.bindings()
    
    def update_progress(self,i):
        f = '[unmusic] unmusic.Copy.update_progress'
        if self.Success:
            # Prevent ZeroDivisionError
            if self._ids:
                percent = (100 * (i + 1)) // len(self._ids)
            else:
                percent = 0
            gi.objs.progress()._item.widget['value'] = percent
            # This is required to fill the progress bar on-the-fly
            sh.objs.root().idle()
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
                objs.waitbox().reset (func    = f
                                     ,message = _('Waiting for {}').format(carrier_sh)
                                     )
                objs._waitbox.show()
                while not os.path.isdir(carrier):
                    time.sleep(1)
                objs._waitbox.close()    
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel()
    
    def get_settings(self,event=None):
        f = '[unmusic] unmusic.Copy.get_settings'
        if self.Success:
            self._genre = self.gui.opt_gnr.choice
            if self.gui.opt_yer.choice == _('Not set'):
                pass
            elif self.gui.opt_yer.choice == '=':
                self._year = sh.lg.Input (title = f
                                         ,value = self.gui.ent_yer.get()
                                         ).integer()
            elif self.gui.opt_yer.choice == '>=':
                self._syear = sh.lg.Input (title = f
                                          ,value = self.gui.ent_yer.get()
                                          ).integer()
            elif self.gui.opt_yer.choice == '<=':
                self._eyear = sh.lg.Input (title = f
                                          ,value = self.gui.ent_yer.get()
                                          ).integer()
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format (self.gui.opt_yer.choice
                                 ,'; '.join(gi.ITEMS_YEAR)
                                 )
                sh.objs.mes(f,mes).error()
            self._source = lg.objs.default().ihome.add_share(self.gui.opt_src.choice)
            self._target = lg.objs._default.ihome.add_share(self.gui.opt_trg.choice)
            self._limit  = sh.lg.Input (title = f
                                       ,value = self.gui.ent_lim.get()
                                       ).integer()
        else:
            sh.com.cancel(f)
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()
    
    def bindings(self):
        self.gui.btn_str.action = self.start
    
    def values(self):
        self._ids    = []
        self._sizes  = []
        self._dirs   = []
        self._query  = ''
        self._source = ''
        self._target = ''
        self._genre  = _('All')
        self._limit  = 100
        self._year   = 0
        self._syear  = 0
        self._eyear  = 0
        # At least 30 MiB should remain free on the target device
        self._minfr  = 31457280
        self.Success = lg.objs.db().Success
    
    def confirm(self):
        f = '[unmusic] unmusic.Copy.copy'
        if self.Success:
            total = sum(self._sizes)
            free  = sh.lg.Path(self._target).free_space()
            cond  = total and free and total + self._minfr < free
            if cond:
                free  = sh.lg.com.human_size (bsize     = free
                                             ,LargeOnly = True
                                             )
                total = sh.lg.com.human_size(total,LargeOnly=1)
                message  = _('Selected albums: {}').format(len(self._ids))
                message += '\n'
                message += _('Total size: {}').format(total)
                message += '\n'
                message += _('Free space: {}').format(free)
                message += '\n\n'
                message += _('Continue?')
                return sh.objs.mes(f,message).question()
            elif not total:
                # Do not fail here since we may change settings after
                sh.com.lazy(f)
            else:
                free = sh.lg.com.human_size (bsize     = free
                                            ,LargeOnly = True
                                            )
                required = sh.lg.com.human_size (bsize     = total + self._minfr
                                                ,LargeOnly = True
                                                )
                message  = _('Not enough free space on "{}"!')
                message  = message.format(self._target)
                message += '\n'
                message += _('Free space: {}').format(free)
                message += '\n'
                message += _('Required: {}').format(required)
                sh.objs.mes(f,message).warning()
        else:
            sh.com.cancel(f)
    
    def copy(self):
        f = '[unmusic] unmusic.Copy.copy'
        if self.Success:
            if self.confirm():
                sh.Geometry(gi.objs.progress().obj).activate()
                gi.objs._progress.add()
                gi.objs._progress._items[-1].label.text(_('Copy progress'))
                sh.objs.root().idle()
                gi.objs._progress.show()
                for i in range(len(self._ids)):
                    myid      = str(self._ids[i])
                    source    = os.path.join(self._source,myid)
                    target    = os.path.join(self._target,myid)
                    source_sh = sh.lg.Text(source).shorten (max_len = 30
                                                           ,FromEnd = True
                                                           )
                    target_sh = sh.lg.Text(target).shorten (max_len = 30
                                                           ,FromEnd = True
                                                           )
                    message = '({}/{}) {} -> {}'.format (i + 1
                                                        ,len(self._ids)
                                                        ,source_sh
                                                        ,target_sh
                                                        )
                    gi.objs._progress._items[-1].label.text(message)
                    self.update_progress(i)
                    idir = sh.lg.Directory (path = source
                                           ,dest = target
                                           )
                    idir.copy()
                    if not idir.Success:
                        self.Success = False
                        break
                gi.objs._progress.close()
            else:
                mes = _('Operation has been canceled by the user.')
                sh.objs.mes(f,mes,True).info()
        else:
            sh.com.cancel(f)
    
    def sizes(self):
        f = '[unmusic] unmusic.Copy.sizes'
        if self.Success:
            self._sizes = []
            if self._ids:
                objs.waitbox().reset (func    = f
                                     ,message = _('Calculate required space')
                                     )
                objs._waitbox.show()
                for myid in self._ids:
                    mydir = os.path.join(self._source,str(myid))
                    idir  = sh.lg.Directory(mydir)
                    self.Success = idir.Success
                    if self.Success:
                        self._sizes.append(idir.size())
                    else:
                        sh.com.cancel(f)
                        break
                objs._waitbox.close()
            else:
                sh.com.lazy(f)
        else:
            sh.com.cancel(f)
    
    def select_albums(self):
        f = '[unmusic] unmusic.Copy.select_albums'
        if self.Success:
            if self._ids:
                text = lg.objs.db().brief(self._ids)
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
                    selected = ibox.selected()
                    poses = []
                    for item in selected:
                        try:
                            poses.append(lst.index(item))
                        except ValueError:
                            self.Success = False
                            mes = _('Wrong input data!')
                            sh.objs.mes(f,mes).error()
                    ids = []
                    for pos in poses:
                        try:
                            ids.append(self._ids[pos])
                        except IndexError:
                            mes = _('Wrong input data!')
                            sh.objs.mes(f,mes).error()
                    ''' Allow an empty list here to cancel copying if no
                        albums are selected.
                    '''
                    self._ids = ids
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch(self):
        f = '[unmusic] unmusic.Copy.fetch'
        if self.Success:
            try:
                if self._genre == _('Light'):
                    lst = list(self._ids) + list(lg.LIGHT)
                elif self._genre == _('Heavy'):
                    lst = list(self._ids) + list(lg.HEAVY)
                else:
                    lst = list(self._ids)
                lg.objs.db().dbc.execute(self._query,lst)
                result = lg.objs._db.dbc.fetchall()
                if result:
                    self._ids = [item[0] for item in result]
                else:
                    sh.com.empty(f)
                    self.Success = False
            except Exception as e:
                self.Success = False
                mes = _('Operation has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.mes(f,mes).error()
        else:
            sh.com.cancel(f)
    
    def query(self):
        f = '[unmusic] unmusic.Copy.query'
        if self.Success:
            ids = lg.objs.db().rated()
            if ids:
                self._ids = ids
                # We assume that 'self._ids' are already distinct
                self._query = 'select ALBUMID from ALBUMS \
                               where ALBUMID in (%s)' \
                               % ','.join('?'*len(self._ids))
                if self._genre in (_('All'),_('Any')):
                    pass
                elif self._genre == _('Light'):
                    self._query += ' and GENRE in (%s)' \
                                   % ','.join('?'*len(lg.LIGHT))
                elif self._genre == _('Heavy'):
                    self._query += ' and GENRE in (%s)' \
                                   % ','.join('?'*len(lg.HEAVY))
                else:
                    self.Success = False
                    genres = (_('All'),_('Any'),_('Light'),_('Heavy'))
                    mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                    mes = mes.format(self._genre,'; '.join(genres))
                    sh.objs.mes(f,mes).error()
                ''' If an exact year is set then only this year should
                    be used; otherwise, a starting-ending years range
                    should be used.
                '''
                if self._year:
                    self._query += ' and YEAR = %d' % self._year
                else:
                    if self._syear:
                        self._query += ' and YEAR >= %d' % self._syear
                    if self._eyear:
                        self._query += ' and YEAR <= %d' % self._eyear
                self._query += ' order by ALBUMID'
                if self._limit:
                    self._query += ' limit %d' % self._limit
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = '[unmusic] unmusic.Copy.debug'
        if self.Success:
            if self._ids:
                '''
                mes = '; '.join([str(albumid) for albumid in self._ids])
                sh.objs.mes(f,mes,True).debug()
                '''
                ids = lg.objs.db().brief(self._ids)
                ids = ids.splitlines()
                ids.sort()
                sh.fast_txt('\n'.join(ids))
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def start(self,event=None):
        # Do not reset GUI here
        self.values()
        self.get_settings()
        self.wait_carrier(self._source)
        self.wait_carrier(self._target)
        self.query()
        self.fetch()
        self.select_albums()
        self.sizes()
        self.copy()



class Tracks:
    
    
    def __init__(self):
        self.Active  = False
        self.Success = lg.objs.db().Success
        self.gui     = gi.Tracks(height=400)
        self.gui.close()
        self.bindings()
    
    def decypher(self,event=None):
        f = '[unmusic] unmusic.Tracks.decypher'
        if self.Success:
            for track in self.gui._tracks:
                title = track.ent_tit.get()
                title = lg.objs.caesar().decypher(title)
                track.ent_tit.clear_text()
                track.ent_tit.insert(title)
        else:
            sh.com.cancel(f)
    
    def cypher(self,event=None):
        f = '[unmusic] unmusic.Tracks.cypher'
        if self.Success:
            for track in self.gui._tracks:
                title = track.ent_tit.get()
                title = lg.objs.caesar().cypher(title)
                track.ent_tit.clear_text()
                track.ent_tit.insert(title)
        else:
            sh.com.cancel(f)
    
    def decode(self,event=None):
        f = '[unmusic] unmusic.Tracks.decode'
        if self.Success:
            for track in self.gui._tracks:
                title = track.ent_tit.get()
                title = lg.com.decode_back(title)
                track.ent_tit.clear_text()
                track.ent_tit.insert(title)
        else:
            sh.com.cancel(f)
    
    def _dump_search(self,old,new):
        f = '[unmusic] unmusic.Tracks._dump'
        mes = _('Not implemented yet!')
        sh.objs.mes(f,mes).info()
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
                                lg.objs.db().update_track (no   = i + 1
                                                          ,data = new_record
                                                          )
                                # We're in loop - do not use 'return'
                                Dump = True
                            else:
                                mes = _('A track title should be indicated.')
                                sh.objs.mes(f,mes).warning()
                    else:
                        self.Success = False
                        mes = _('Wrong input data!')
                        sh.objs.mes(f,mes).error()
                return Dump
            else:
                sub = '{} = {}'.format(len(old),len(new))
                mes = _('Condition "{}" is not observed!').format(sub)
                sh.objs.mes(f,mes).error()
        else:
            sh.com.empty(f)
    
    def dump(self):
        f = '[unmusic] unmusic.Tracks.dump'
        if self.Success:
            if lg.objs.db().check_nos():
                Extended = False
                if self.gui._tracks:
                    Extended = self.gui._tracks[0].Extended
                old = lg.objs._db.tracks()
                new = self.gui.dump()
                if Extended:
                    return self._dump_search(old,new)
                else:
                    return self._dump(old,new)
            else:
                mes = _('Track numbers should be sequential!')
                sh.objs.mes(f,mes).warning()
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
                lg.objs.db().save()
        else:
            sh.com.cancel(f)
    
    def bindings(self):
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
                    track  = self.gui._tracks[i]
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
                        track.ent_len.insert(sh.lg.com.human_time(float(record[6])))
                        track.ent_len.disable()
                        track.opt_rtg.set(record[7])
                    else:
                        self.Success = False
                        mes = _('Wrong input data: "{}"!').format(data)
                        sh.objs.mes(f,mes).error()
                self.gui.after_add()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def reload(self,event=None):
        self.fill()
        self.show()
    
    def fill(self,event=None):
        f = '[unmusic] unmusic.Tracks.fill'
        if self.Success:
            self.gui.reset()
            data = lg.objs.db().tracks()
            if data:
                for i in range(len(data)):
                    self.gui.add()
                    mes = _('Load #{}.').format(i+1)
                    self.gui.update_info(mes)
                    record = data[i]
                    track  = self.gui._tracks[i]
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
                        track.ent_len.insert(sh.lg.com.human_time(float(record[5])))
                        track.ent_len.disable()
                        track.opt_rtg.set(record[6])
                    else:
                        self.Success = False
                        mes = _('Wrong input data: "{}"!').format(data)
                        sh.objs.mes(f,mes).error()
                self.gui.after_add()
            else:
                mes = _('No tracks are associated with this album.')
                sh.objs.mes(f,mes).info()
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
        self.values()
        self.gui   = gi.AlbumEditor()
        self.logic = lg.AlbumEditor()
        self.bindings()
        
    def prev_unrated(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.prev_unrated'
        if self.Success:
            self.save()
            self.logic.prev_rated()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def next_unrated(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.next_unrated'
        if self.Success:
            self.save()
            self.logic.next_rated()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def update_presence(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.update_presence'
        if self.Success:
            local     = lg.objs.default().ihome.add_share(_('local collection'))
            external  = lg.objs._default.ihome.add_share(_('external collection'))
            mobile    = lg.objs._default.ihome.add_share(_('mobile collection'))
            plocal    = os.path.join(local,str(lg.objs.db().albumid))
            pexternal = os.path.join(external,str(lg.objs._db.albumid))
            pmobile   = os.path.join(mobile,str(lg.objs._db.albumid))
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
            albumid = lg.objs.db().max_id()
            if albumid:
                lg.objs._db.albumid = albumid
                self.fill()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def go_start(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.go_start'
        if self.Success:
            ''' #NOTE: If we change 'albumid' BEFORE saving, then
                a wrong DB record will be overwritten!
            '''
            self.save()
            albumid = lg.objs.db().min_id()
            if albumid:
                lg.objs._db.albumid = albumid
                self.fill()
            else:
                sh.com.empty(f)
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
                        data = lg.objs.db().has_id(albumid)
                        if data:
                            lg.objs._db.albumid = albumid
                            self.fill()
                        else:
                            mes = _('No matches!')
                            sh.objs.mes(f,mes).info()
                    else:
                        mes = _('Wrong input data: "{}"!')
                        mes = mes.format(albumid)
                        sh.objs.mes(f,mes).warning()
                else:
                    mes = _('Wrong input data: "{}"!')
                    mes = mes.format(albumid)
                    sh.objs.mes(f,mes).warning()
            else:
                sh.com.lazy(f)
        else:
            sh.com.cancel(f)
    
    def cypher(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.cypher'
        if self.Success:
            artist  = self.gui.ent_art.get()
            album   = self.gui.ent_alb.get()
            genre   = self.gui.opt_gnr.choice
            artist  = lg.objs.caesar().cypher(artist)
            album   = lg.objs._caesar.cypher(album)
            genre   = lg.objs._caesar.cypher(genre)
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
            artist = lg.objs.caesar().decypher(artist)
            album  = lg.objs._caesar.decypher(album)
            genre  = lg.objs._caesar.decypher(genre)
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
    
    def values(self):
        self._defimg   = None
        self._image    = None
        self._path_def = sh.objs.pdir().add('..','resources','cd.png')
    
    def default_image(self):
        if not self._defimg:
            self._defimg = sh.Image().open(self._path_def)
        return self._defimg
        
    def zoom_image(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.zoom_image'
        if self.Success:
            if self._image:
                viewer = gi.ImageViewer()
                viewer.lbl.widget.config(image=self._image)
                viewer.lbl.widget.image = self._image
                viewer.show()
            else:
                # This should not happen
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def set_image(self,image):
        f = '[unmusic] unmusic.AlbumEditor.set_image'
        if self.Success:
            if image:
                try:
                    ipic = sh.Image()
                    ipic._bytes = image
                    ipic.loader()
                    self._image = ipic.image()
                    ipic = sh.Image()
                    ipic._bytes = image
                    ipic.loader()
                    ''' These are dimensions of 'self.gui.frm_img' when
                        the default image is loaded.
                    '''
                    ipic.thumbnail(130,212)
                    thumb = ipic.image()
                except Exception as e:
                    ''' Do not fail 'Success' here - it can just be
                        an incorrectly ripped image.
                    '''
                    thumb = None
                    mes = _('Third-party module has failed!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.mes(f,mes).warning()
            else:
                self._image = self.default_image()
                thumb = self._image
            self.gui.lbl_img.widget.config(image=thumb)
            # Prevent the garbage collector from deleting the image
            self.gui.lbl_img.widget.image = thumb
        else:
            sh.com.cancel(f)
    
    def play(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.play'
        if self.Success:
            choice  = self.gui.opt_ply.choice
            default = _('Play')
            if choice == default:
                sh.com.lazy(f)
            elif choice == _('All'):
                self.gui.opt_ply.set(default)
                lg.Play().all_tracks()
            elif choice == _('Good'):
                self.gui.opt_ply.set(default)
                lg.Play().good_tracks()
            elif choice == _('Best'):
                self.gui.opt_ply.set(default)
                lg.Play().good_tracks(9)
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(choice,';'.join(gi.PLAY))
                sh.objs.mes(f,mes).error()
        else:
            sh.com.cancel(f)
    
    def length(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.length'
        if self.Success:
            total = lg.objs.db().get_length()
            if total:
                mes = _('{} ({} tracks)')
                mes = mes.format (sh.lg.com.human_time(sum(total))
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
    
    def bitrate(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.bitrate'
        if self.Success:
            mean = self.logic.mean_bitrate()
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
            rating = self.logic.mean_rating()
            if isinstance(rating,float):
                ''' If an album has more songs with rating X that with
                    rating Y, we should consider that the album has
                    an overall rating of X. Thus, we use 'round' instead
                    of 'int'.
                '''
                self.gui.opt_rtg.set(round(rating))
            elif rating is None:
                sh.com.empty(f)
            else:
                mes = _('Wrong input data: "{}"!').format(rating)
                sh.objs.mes(f,mes).error()
        else:
            sh.com.cancel(f)
    
    def _set_rating(self):
        f = '[unmusic] unmusic.AlbumEditor._set_rating'
        value = sh.lg.Input (title = f
                            ,value = self.gui.opt_rtg.choice
                            ).integer()
        lg.objs._db.set_rating(value)
    
    def set_rating(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.set_rating'
        if self.Success:
            rating = self.logic.mean_rating()
            if isinstance(rating,float):
                mes = _('Tracks are of a mixed rating. Do you want to assign the same rating to all of them?')
                if rating == int(rating):
                    self._set_rating()
                elif sh.objs.mes(f,mes).question():
                    self._set_rating()
                else:
                    self.get_rating()
            elif rating is None:
                sh.com.empty(f)
            else:
                mes = _('Wrong input data: "{}"!').format(rating)
                sh.objs.mes(f,mes).error()
        else:
            sh.com.cancel(f)
    
    def dump(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.dump'
        if self.Success:
            old = lg.objs.db().get_album()
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
                            sh.objs.mes(f,mes).warning()
                            if old[0]:
                                new[0] = old[0]
                            else:
                                # Do not localize (being stored in DB)
                                new[0] = '?'
                        if not new[1]:
                            mes = _('An artist should be indicated.')
                            sh.objs.mes(f,mes).warning()
                            if old[1]:
                                new[1] = old[1]
                            else:
                                # Do not localize (being stored in DB)
                                new[1] = '?'
                        # Do not warn if a year is not set
                        if new[2]:
                            new[2] = sh.lg.Input (title = f
                                                 ,value = new[2]
                                                 ).integer()
                        else:
                            # We need to return integer anyway
                            new[2] = old[2]
                        if old == new:
                            mes = _('No changes!')
                            sh.objs.mes(f,mes,True).info()
                        else:
                            mes = _('Some fields have been updated.')
                            sh.objs.mes(f,mes,True).info()
                            query = self.logic._compare_albums(old,new)
                            lg.objs._db.updateDB(query)
                            return query
                    else:
                        sh.com.empty(f)
                else:
                    sub = '{} = {}'.format(len(old)-1,len(new))
                    mes = _('The condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.mes(f,mes).error()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def search_track(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.search_track'
        if self.Success:
            search = self.gui.ent_sr2.get()
            if search:
                data = lg.objs.db().search_track(search)
                if data:
                    objs.tracks().fill_search(data=data)
                    objs._tracks.show()
                else:
                    mes = _('No matches!')
                    sh.objs.mes(f,mes).info()
            else:
                sh.com.lazy(f)
        else:
            sh.com.cancel(f)
    
    def search_album(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.search_album'
        if self.Success:
            self.save()
            old = lg.objs.db().albumid
            # Not 1, because we use '<' and '>' in search
            lg.objs._db.albumid = 0
            self.search_next_album(Save=False)
            if lg.objs._db.albumid == 0:
                lg.objs._db.albumid = old
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
            search = self.gui.ent_src.get()
            if search:
                old     = lg.objs.db().albumid
                albumid = lg.objs._db.next_album(search)
                if albumid:
                    lg.objs._db.albumid = albumid
                    self.fill()
                else:
                    lg.objs._db.albumid = old
                    mes = _('No matches!')
                    sh.objs.mes(f,mes).info()
            else:
                self.gui.btn_spr.inactive()
                self.gui.btn_snx.inactive()
                sh.com.lazy(f)
        else:
            sh.com.cancel(f)
    
    def search_prev_album(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.search_prev_album'
        if self.Success:
            ''' #NOTE: Make sure that actual 'albumid' is not changed
                prior to 'self.search_prev_album'.
            '''
            self.save()
            search = self.gui.ent_src.get()
            if search:
                old     = lg.objs.db().albumid
                albumid = lg.objs._db.prev_album(search)
                if albumid:
                    lg.objs._db.albumid = albumid
                    self.fill()
                else:
                    lg.objs._db.albumid = old
                    mes = _('No matches!')
                    sh.objs.mes(f,mes).info()
            else:
                self.gui.btn_spr.inactive()
                self.gui.btn_snx.inactive()
                sh.com.lazy(f)
        else:
            sh.com.cancel(f)
    
    def prev(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.prev'
        if self.Success:
            self.save()
            self.logic.dec()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def next(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.next'
        if self.Success:
            self.save()
            self.logic.inc()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def tracks(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.tracks'
        if self.Success:
            objs.tracks().fill()
            if objs._tracks.gui._tracks:
                objs._tracks.show()
        else:
            sh.com.cancel(f)
    
    def delete(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.delete'
        if self.Success:
            mes = _('Are you sure you want to permanently delete record #{}?')
            mes = mes.format(lg.objs.db().albumid)
            if sh.objs.mes(f,mes).question():
                mes = _('Delete #{}.').format(lg.objs._db.albumid)
                self.gui.update_info(text=mes)
                lg.objs._db.delete()
                lg.objs._db.albumid = self.logic.get_max()
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
                lg.objs.db().save()
        else:
            sh.com.cancel(f)
    
    def create(self,event=None):
        f = '[unmusic] unmusic.AlbumEditor.create'
        if self.Success:
            lg.objs.db().add_album(('?','?',2000,'?','','',''))
            lg.objs._db.albumid = self.logic.get_max()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def bindings(self):
        self.gui.widget.protocol("WM_DELETE_WINDOW",self.close)
        self.gui.btn_cyp.action = self.cypher
        self.gui.btn_dec.action = self.decode
        self.gui.btn_del.action = self.delete
        self.gui.btn_dez.action = self.decypher
        self.gui.btn_nxt.action = self.next
        self.gui.btn_prv.action = self.prev
        self.gui.btn_rec.action = self.create
        self.gui.btn_rld.action = self.fill
        self.gui.btn_sav.action = self.save
        self.gui.btn_snx.action = self.search_next_album
        self.gui.btn_spr.action = self.search_prev_album
        self.gui.btn_trk.action = self.tracks
        self.gui.opt_rtg.action = self.set_rating
        self.gui.opt_ply.action = self.play
        sh.com.bind (obj      = self.gui
                    ,bindings = '<Alt-n>'
                    ,action   = self.next_unrated
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = '<Alt-p>'
                    ,action   = self.prev_unrated
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
                    ,action   = self.tracks
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = '<Control-n>'
                    ,action   = self.create
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = '<Alt-Left>'
                    ,action   = self.prev
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = '<Alt-Right>'
                    ,action   = self.next
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
        self.Success = self.logic.Success = lg.objs.db().Success
        lg.objs._db.albumid = self.logic.get_max()
        self.fill()
    
    def update_album_search(self):
        f = '[unmusic] unmusic.AlbumEditor.update_album_search'
        if self.Success:
            search = self.gui.ent_src.get()
            self.gui.btn_spr.inactive()
            self.gui.btn_snx.inactive()
            if search:
                albumid = lg.objs._db.next_album(search)
                if albumid:
                    self.gui.btn_snx.active()
                albumid = lg.objs._db.prev_album(search)
                if albumid:
                    self.gui.btn_spr.active()
        else:
            sh.com.cancel(f)
    
    def update_meter(self):
        f = '[unmusic] unmusic.AlbumEditor.update_meter'
        if self.Success:
            _max = self.logic.get_max()
            self.gui.lbl_mtr.text ('{} / {}'.format (self.logic.get_no()
                                                    ,_max
                                                    )
                                  )
            if lg.objs.db().albumid < _max:
                self.gui.btn_nxt.active()
            else:
                self.gui.btn_nxt.inactive()
            if lg.objs._db.albumid == self.logic.get_min():
                self.gui.btn_prv.inactive()
            else:
                self.gui.btn_prv.active()
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
            data = lg.objs.db().get_album()
            if data:
                if len(data) == 7:
                    mes = _('Load #{}.').format(lg.objs._db.albumid)
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
                    self.bitrate()
                    self.length()
                    self.set_image(data[6])
                    self.update()
                    if objs.tracks().Active:
                        objs._tracks.reload()
                else:
                    mes = _('Wrong input data: "{}"!').format(data)
                    sh.objs.mes(f,mes).error()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()



class Menu:
    
    def __init__(self):
        self.gui = gi.Menu()
        self.bindings()
        
    def copy(self,event=None):
        objs.copy().show()
    
    def album_editor(self,event=None):
        objs.editor().reset()
        objs._editor.show()
    
    def collect(self,event=None):
        ''' If an artist and/or album title were changed and originally
            were not empty, there is no easy way to tell if we are
            dealing with the same album or not. So, it's best to add
            tags to DB only once.
        '''
        f = '[unmusic] unmusic.Menu.collect'
        folder = sh.lg.Home(app_name='unmusic').add_share(_('not processed'))
        Obfuscate = self.gui.cbx_obf.get()
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
                        itext    = sh.lg.Text(basename)
                        itext.delete_unsupported()
                        itext.shorten(max_len=15)
                        mes = _('Process "{}" ({}/{})')
                        mes = mes.format (itext.text
                                         ,count
                                         ,len(dirs)
                                         )
                        gi.objs.wait().reset (func    = f
                                             ,message = mes
                                             )
                        gi.objs._wait.show()
                        lg.Directory (path      = folder
                                     ,Obfuscate = Obfuscate
                                     ).run()
                        ''' In case something went wrong, we should lose 
                            only 1 album record, not the entire sequence.
                        '''
                        lg.objs.db().save()
                    else:
                        sh.com.cancel(f)
                gi.objs.wait().close()
                delta = timer.end()
                mes = _('Operation has taken {}')
                mes = mes.format(sh.lg.com.human_time(delta))
                sh.objs.mes(f,mes).info()
                objs.editor().reset()
                objs._editor.show()
            else:
                sh.com.empty(f)
            iwalk.delete_empty()
            lg.objs.db().save()
        else:
            sh.com.cancel(f)
    
    def prepare(self,event=None):
        f = '[unmusic] unmusic.Menu.prepare'
        mes = _('Not implemented yet!')
        sh.objs.mes(f,mes).info()
    
    def bindings(self):
        self.gui._a[0].action = self.album_editor
        self.gui._a[1].action = self.prepare
        self.gui._a[2].action = self.collect
        self.gui._a[3].action = self.copy
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()



class Objects:
    
    def __init__(self):
        self._editor = self._tracks = self._copy = self._waitbox = None
    
    def waitbox(self):
        if self._waitbox is None:
            self._waitbox = sh.WaitBox(gi.ICON)
        return self._waitbox
    
    def copy(self):
        if self._copy is None:
            self._copy = Copy()
        return self._copy
    
    def editor(self):
        if self._editor is None:
            self._editor = AlbumEditor()
        return self._editor
    
    def tracks(self):
        if self._tracks is None:
            self._tracks = Tracks()
        return self._tracks


objs = Objects()



if __name__ == '__main__':
    f = '[unmusic] unmusic.__main__'
    sh.com.start()
    Menu().show()
    lg.objs.db().save()
    lg.objs._db.close()
    mes = _('Goodbye!')
    sh.objs.mes(f,mes,True).debug()
    sh.com.end()
