#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg
import logic     as lg
import gui       as gi

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install(lg.PRODUCT,'../resources/locale')



class Tracks:
    
    
    def __init__(self):
        self.Success = lg.objs.db().Success
        self.gui     = gi.Tracks(height=400)
    
    def fill_search(self,data):
        f = 'controller.Tracks.fill_search'
        if self.Success:
            self.gui.reset()
            if data:
                for i in range(len(data)):
                    self.gui.add(Extended=True)
                    record = data[i]
                    track  = self.gui._tracks[i]
                    if len(record) == 8:
                        track.w_aid.read_only(False)
                        track.w_aid.clear_text()
                        track.w_aid.insert(record[0])
                        track.w_aid.read_only(True)
                        track.w_tno.clear_text()
                        track.w_tno.insert(str(record[2]))
                        track.w_tit.clear_text()
                        track.w_tit.insert(record[1])
                        track.w_lyr.clear_text()
                        track.w_lyr.insert(record[3])
                        track.w_com.clear_text()
                        track.w_com.insert(record[4])
                        track.w_bit.read_only(False)
                        track.w_bit.clear_text()
                        track.w_bit.insert(str(record[5]//1000)+'k')
                        track.w_bit.read_only(True)
                        track.w_len.read_only(False)
                        track.w_len.clear_text()
                        track.w_len.insert(sh.com.human_time(float(record[6])))
                        track.w_len.read_only(True)
                        track.w_rtg.set(record[7])
                    else:
                        self.Success = False
                        sh.objs.mes (f,_('ERROR')
                                    ,_('Wrong input data: "%s"!') \
                                    % str(data)
                                    )
                self.gui.after_add()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def fill(self):
        f = 'controller.Tracks.fill'
        if self.Success:
            self.gui.reset()
            data = lg.objs.db().tracks()
            if data:
                for i in range(len(data)):
                    self.gui.add()
                    record = data[i]
                    track  = self.gui._tracks[i]
                    if len(record) == 7:
                        track.w_tno.clear_text()
                        track.w_tno.insert(str(record[1]))
                        track.w_tit.clear_text()
                        track.w_tit.insert(record[0])
                        track.w_lyr.clear_text()
                        track.w_lyr.insert(record[2])
                        track.w_com.clear_text()
                        track.w_com.insert(record[3])
                        track.w_bit.read_only(False)
                        track.w_bit.clear_text()
                        track.w_bit.insert(str(record[4]//1000)+'k')
                        track.w_bit.read_only(True)
                        track.w_len.read_only(False)
                        track.w_len.clear_text()
                        track.w_len.insert(sh.com.human_time(float(record[5])))
                        track.w_len.read_only(True)
                        track.w_rtg.set(record[6])
                    else:
                        self.Success = False
                        sh.objs.mes (f,_('ERROR')
                                    ,_('Wrong input data: "%s"!') \
                                    % str(data)
                                    )
                self.gui.after_add()
            else:
                sh.objs.mes (f,_('INFO')
                            ,_('No tracks are associated with this album.')
                            )
        else:
            sh.com.cancel(f)
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()



class AlbumEditor:
    
    def __init__(self):
        self.gui   = gi.AlbumEditor()
        self.logic = lg.AlbumEditor()
        self.bindings()
        
    def length(self,event=None):
        f = 'controller.AlbumEditor.length'
        if self.Success:
            total = lg.objs.db().get_length()
            if total:
                mes = _('%s (%d tracks)') % (sh.com.human_time(sum(total))
                                            ,len(total)
                                            )
            else:
                mes = '?'
            self.gui.body.w_len.read_only(False)
            self.gui.body.w_len.clear_text()
            self.gui.body.w_len.insert(mes)
            self.gui.body.w_len.read_only(True)
        else:
            sh.com.cancel(f)
    
    def bitrate(self,event=None):
        f = 'controller.AlbumEditor.bitrate'
        if self.Success:
            mean = self.logic.mean_bitrate()
            if mean:
                mes = '%dk' % (mean // 1000)
            else:
                mes = '?'
            self.gui.body.w_bit.read_only(False)
            self.gui.body.w_bit.clear_text()
            self.gui.body.w_bit.insert(mes)
            self.gui.body.w_bit.read_only(True)
        else:
            sh.com.cancel(f)
    
    def get_rating(self,event=None):
        f = 'controller.AlbumEditor.get_rating'
        if self.Success:
            rating = self.logic.mean_rating()
            if isinstance(rating,float):
                ''' If an album has more songs with rating X that with
                    rating Y, we should consider that the album has
                    an overall rating of X. Thus, we use 'round' instead
                    of 'int'.
                '''
                self.gui.top_area.w_rtg.set(round(rating))
            elif rating is None:
                sh.com.empty(f)
            else:
                sh.objs.mes (f,_('ERROR')
                            ,_('Wrong input data: "%s"!') % str(rating)
                            )
        else:
            sh.com.cancel(f)
    
    def _set_rating(self):
        f = 'controller.AlbumEditor._set_rating'
        value = sh.Input (title = f
                         ,value = self.gui.top_area.w_rtg.choice
                         ).integer()
        lg.objs._db.set_rating(value)
    
    def set_rating(self,event=None):
        f = 'controller.AlbumEditor.set_rating'
        if self.Success:
            rating = self.logic.mean_rating()
            if isinstance(rating,float):
                if rating == int(rating):
                    self._set_rating()
                elif sg.Message (f,_('QUESTION')
                                ,_('Tracks are of a mixed rating. Do you want to assign the same rating to all of them?')
                                ).Yes:
                    self._set_rating()
                else:
                    self.get_rating()
            elif rating is None:
                sh.com.empty(f)
            else:
                sh.objs.mes (f,_('ERROR')
                            ,_('Wrong input data: "%s"!') % str(rating)
                            )
        else:
            sh.com.cancel(f)
    
    def dump(self,event=None):
        f = 'controller.AlbumEditor.dump'
        if self.Success:
            old = lg.objs.db().get_album()
            if old:
                new = self.gui.dump()
                if len(old) == len(new):
                    old = list(old)
                    new = list(new)
                    if [item for item in new if item]:
                        if not new[0]:
                            sh.objs.mes (f,_('WARNING')
                                        ,_('An album title should be indicated.')
                                        )
                            if old[0]:
                                new[0] = old[0]
                            else:
                                # Do not localize (being stored in DB)
                                new[0] = '?'
                        if not new[1]:
                            sh.objs.mes (f,_('WARNING')
                                        ,_('An artist should be indicated.')
                                        )
                            if old[1]:
                                new[1] = old[1]
                            else:
                                # Do not localize (being stored in DB)
                                new[1] = '?'
                        # Do not warn if a year is not set
                        if new[2]:
                            new[2] = sh.Input (title = f
                                              ,value = new[2]
                                              ).integer()
                        else:
                            # We need to return integer anyway
                            new[2] = old[2]
                        if old == new:
                            sh.log.append (f,_('INFO')
                                          ,_('No changes!')
                                          )
                        else:
                            sh.log.append (f,_('INFO')
                                          ,_('Some fields have been updated.')
                                          )
                            query = self.logic._compare_albums(old,new)
                            lg.objs._db.updateDB(query)
                            return query
                    else:
                        sh.com.empty(f)
                else:
                    sh.objs.mes (f,_('ERROR')
                                ,_('The condition "%s" is not observed!')\
                                % ('%d == %d' % (len(old),len(new)))
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def search_track(self,event=None):
        f = 'controller.AlbumEditor.search_track'
        if self.Success:
            search = self.gui.top_area.ent_sr2.get()
            if search:
                data = lg.objs.db().search_track(search)
                if data:
                    objs.tracks().fill_search(data=data)
                    objs._tracks.show()
                else:
                    sh.objs.mes (f,_('INFO')
                                ,_('No matches!')
                                )
            else:
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do!')
                              )
        else:
            sh.com.cancel(f)
    
    def search_album(self,event=None):
        f = 'controller.AlbumEditor.search_album'
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
        f = 'controller.AlbumEditor.search_next_album'
        if self.Success:
            ''' #NOTE: If we change 'albumid' BEFORE saving, then
                a wrong DB record will be overwritten! Since
                'self.search_album' is generally a wrapper over this
                procedure and changes 'albumid', we should be careful
                about this.
            '''
            if Save:
                self.save()
            search = self.gui.top_area.ent_src.get()
            if search:
                old     = lg.objs.db().albumid
                albumid = lg.objs._db.next_album(search)
                if albumid:
                    lg.objs._db.albumid = albumid
                    self.fill()
                else:
                    lg.objs._db.albumid = old
                    sh.objs.mes (f,_('INFO')
                                ,_('No matches!')
                                )
            else:
                self.gui.top_area.btn_spr.inactive()
                self.gui.top_area.btn_snx.inactive()
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do!')
                              )
        else:
            sh.com.cancel(f)
    
    def search_prev_album(self,event=None):
        f = 'controller.AlbumEditor.search_prev_album'
        if self.Success:
            ''' #NOTE: Make sure that actual 'albumid' is not changed
                prior to 'self.search_prev_album'.
            '''
            self.save()
            search = self.gui.top_area.ent_src.get()
            if search:
                old     = lg.objs.db().albumid
                albumid = lg.objs._db.prev_album(search)
                if albumid:
                    lg.objs._db.albumid = albumid
                    self.fill()
                else:
                    lg.objs._db.albumid = old
                    sh.objs.mes (f,_('INFO')
                                ,_('No matches!')
                                )
            else:
                self.gui.top_area.btn_spr.inactive()
                self.gui.top_area.btn_snx.inactive()
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do!')
                              )
        else:
            sh.com.cancel(f)
    
    def prev(self,event=None):
        f = 'controller.AlbumEditor.prev'
        if self.Success:
            self.save()
            self.logic.dec()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def next(self,event=None):
        f = 'controller.AlbumEditor.next'
        if self.Success:
            self.save()
            self.logic.inc()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def tracks(self,event=None):
        f = 'controller.AlbumEditor.tracks'
        if self.Success:
            objs.tracks().fill()
            if objs._tracks.gui._tracks:
                objs._tracks.show()
        else:
            sh.com.cancel()
    
    def delete(self,event=None):
        f = 'controller.AlbumEditor.delete'
        if self.Success:
            if sg.Message (f,_('QUESTION')
                          ,_('Are you sure you want to permanently delete record #%d?')\
                          % lg.objs.db().albumid
                          ).Yes:
                self.gui.bottom_area.update (text = _('Delete #%d.') \
                                                    % lg.objs._db.albumid
                                            )
                lg.objs._db.delete()
                lg.objs._db.albumid = self.logic.get_max()
                self.fill()
        else:
            sh.com.cancel(f)
    
    def save(self,event=None):
        ''' #NOTE: this should be done before 'albumid' is changed,
            otherwise, a wrong DB record will be overwritten!
        '''
        f = 'controller.AlbumEditor.save'
        if self.Success:
            if self.dump():
                self.gui.bottom_area.update(_('Save DB.'))
                lg.objs.db().save()
        else:
            sh.com.cancel(f)
    
    def create(self,event=None):
        f = 'controller.AlbumEditor.create'
        if self.Success:
            lg.objs.db().add_album(('?','?',2000,'?','','',''))
            lg.objs._db.albumid = self.logic.get_max()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def bindings(self):
        self.gui.widget.protocol("WM_DELETE_WINDOW",self.close)
        self.gui.top_area.btn_nxt.action    = self.next
        self.gui.top_area.btn_prv.action    = self.prev
        self.gui.top_area.btn_spr.action    = self.search_prev_album
        self.gui.top_area.btn_snx.action    = self.search_next_album
        self.gui.top_area.w_rtg.action      = self.set_rating
        self.gui.bottom_area.btn_trk.action = self.tracks
        self.gui.bottom_area.btn_rec.action = self.create
        self.gui.bottom_area.btn_sav.action = self.save
        self.gui.bottom_area.btn_rld.action = self.fill
        self.gui.bottom_area.btn_del.action = self.delete
        sg.bind (obj      = self.gui
                ,bindings = ['<F5>','<Control-r>']
                ,action   = self.fill
                )
        sg.bind (obj      = self.gui.top_area.ent_src
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.search_album
                )
        sg.bind (obj      = self.gui.top_area.ent_sr2
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.search_track
                )
        sg.bind (obj      = self.gui
                ,bindings = ['<F2>','<Control-s>']
                ,action   = self.save
                )
        sg.bind (obj      = self.gui
                ,bindings = ['<F4>','<Control-t>','<Alt-t>']
                ,action   = self.tracks
                )
        sg.bind (obj      = self.gui
                ,bindings = '<Control-n>'
                ,action   = self.create
                )
        sg.bind (obj      = self.gui
                ,bindings = '<Alt-Left>'
                ,action   = self.prev
                )
        sg.bind (obj      = self.gui
                ,bindings = '<Alt-Right>'
                ,action   = self.next
                )
    
    def reset(self):
        f = 'controller.AlbumEditor.reset'
        self.Success = self.logic.Success = lg.objs.db().Success
        lg.objs._db.albumid = self.logic.get_max()
        self.fill()
    
    def update_album_search(self):
        f = 'controller.AlbumEditor.update_album_search'
        if self.Success:
            search = self.gui.top_area.ent_src.get()
            self.gui.top_area.btn_spr.inactive()
            self.gui.top_area.btn_snx.inactive()
            if search:
                albumid = lg.objs._db.next_album(search)
                if albumid:
                    self.gui.top_area.btn_snx.active()
                albumid = lg.objs._db.prev_album(search)
                if albumid:
                    self.gui.top_area.btn_spr.active()
        else:
            sh.com.cancel(f)
    
    def update_meter(self):
        f = 'controller.AlbumEditor.update_meter'
        if self.Success:
            _max = self.logic.get_max()
            self.gui.top_area.lbl_mtr.text ('%d / %d' % (self.logic.get_no()
                                                        ,_max
                                                        )
                                           )
            if lg.objs.db().albumid < _max:
                self.gui.top_area.btn_nxt.active()
            else:
                self.gui.top_area.btn_nxt.inactive()
            if lg.objs._db.albumid == self.logic.get_min():
                self.gui.top_area.btn_prv.inactive()
            else:
                self.gui.top_area.btn_prv.active()
        else:
            sh.com.cancel(f)
    
    def update(self):
        f = 'controller.AlbumEditor.update'
        if self.Success:
            self.update_meter()
            self.update_album_search()
        else:
            sh.com.cancel(f)
    
    def fill(self,event=None):
        f = 'controller.AlbumEditor.fill'
        if self.Success:
            self.logic.get_no()
            data = lg.objs.db().get_album()
            if data:
                if len(data) == 6:
                    self.gui.bottom_area.update (_('Load #%d.') \
                                                % lg.objs._db.albumid
                                                )
                    self.gui.body.reset()
                    self.gui.body.w_alb.insert(data[0])
                    self.gui.body.w_art.insert(data[1])
                    self.gui.body.w_yer.insert(data[2])
                    genre = data[3]
                    if not genre:
                        # Do not localize (being stored in DB)
                        genre = '?'
                    items = list(gi.GENRES)
                    if not genre in items:
                        items.append(genre)
                    self.gui.body.w_gnr.reset (items   = items
                                              ,default = genre
                                              )
                    self.gui.body.w_cnt.insert(data[4])
                    self.gui.body.w_com.insert(data[5])
                    self.get_rating()
                    self.bitrate()
                    self.length()
                    self.update()
                else:
                    sh.objs.mes (f,_('ERROR')
                                ,_('Wrong input data: "%s"!') \
                                % str(data)
                                )
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
        
    def album_editor(self,event=None):
        objs.editor().reset()
        objs._editor.show()
    
    def collect(self,event=None,folder='/home/pete/tmp/meta'):
        ''' If an artist and/or album title were changed and originally
            were not empty, there is no easy way to tell if we are
            dealing with the same album or not. So, it's best to add
            tags to DB only once.
        '''
        f = 'controller.Menu.collect'
        dirs = lg.Walker(folder).dirs()
        if dirs:
            timer = sh.Timer(f)
            timer.start()
            for folder in dirs:
                lg.Directory(path=folder).run()
            delta = timer.end()
            sh.objs.mes (f,_('INFO')
                        ,_('Operation has taken %s') \
                        % sh.com.human_time(delta)
                        )
            objs.editor().reset()
            objs._editor.show()
        else:
            sh.com.empty(f)
    
    def prepare(self,event=None):
        f = 'controller.Menu.prepare'
        sh.objs.mes (f,_('INFO')
                    ,_('Not implemented yet!')
                    )
    
    def obfuscate(self,event=None):
        f = 'controller.Menu.obfuscate'
        sh.objs.mes (f,_('INFO')
                    ,_('Not implemented yet!')
                    )
    
    def bindings(self):
        self.gui.parent.widget.protocol("WM_DELETE_WINDOW",self.close)
        sg.bind (obj      = self.gui.parent
                ,bindings = ['<Control-q>','<Control-w>']
                ,action   = self.close
                )
        self.gui._a[0].action = self.album_editor
        self.gui._a[1].action = self.prepare
        self.gui._a[2].action = self.collect
        self.gui._a[3].action = self.obfuscate
        self.gui._a[4].action = self.close
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        lg.objs.db().save()
        self.gui.close()



class Objects:
    
    def __init__(self):
        self._editor = self._tracks = None
    
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
    f = 'controller.__main__'
    sg.objs.start()
    Menu().show()
    sg.objs.end()
