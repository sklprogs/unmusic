#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg
import logic     as lg
import gui       as gi

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install(lg.PRODUCT,'../resources/locale')



class AlbumEditor:
    
    def __init__(self):
        self.gui = gi.AlbumEditor()
        self.bindings()
        self.reset()
        
    def search_track(self,event=None):
        f = 'controller.AlbumEditor.search_track'
        if self.Success:
            search = self.gui.top_area.ent_sr2.get()
            if search:
                data = lg.objs.db().search_track(search)
                if data:
                    mes = ''
                    for track in data:
                        #todo: get album info
                        '''
                        mes =  _('Artist:')  + ' %s\n' % self._artist
                        mes += _('Album:')   + ' %s\n' % self._album
                        mes += _('Year:')    + ' %d\n' % self._year
                        '''
                        if track[0]:
                            mes +=  _('Album ID:') + ' %d\n' % track[0]
                        if track[1]:
                            mes += _('Title:') + ' %s\n' % track[1]
                        mes += _('Track #:') + ' %d\n' % track[2]
                        if track[3]:
                            mes += _('Lyrics:')   + ' %s\n' % track[3]
                        if track[4]:
                            mes += _('Comment:')  + ' %s\n' % track[4]
                        if track[5]:
                            mes += _('Bitrate:')  + ' %dk\n' \
                                   % (track[5] // 1000)
                        # Length
                        if track[6]:
                            minutes = track[6] // 60
                            seconds = track[6] - minutes * 60
                            mes += _('Length:') + ' %d ' % minutes \
                                   + _('min')   + ' %d ' % seconds \
                                   + _('sec')   + '\n'
                        # Rating
                        if track[7]:
                            mes += _('Rating:')  + ' %d\n' % track[7]
                        mes += '\n\n'
                    
                    gi.objs.tracks().reset()
                    gi.objs._tracks.insert(text=mes)
                    gi.objs._tracks.show()
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
            old = lg.objs.db().albumid
            # Not 1, because we use '<' and '>' in search
            lg.objs._db.albumid = 0
            self.search_next_album()
            if lg.objs._db.albumid == 0:
                lg.objs._db.albumid = old
        else:
            sh.com.cancel(f)
    
    def search_next_album(self,event=None):
        f = 'controller.AlbumEditor.search_next_album'
        if self.Success:
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
    
    def inc(self):
        f = 'controller.AlbumEditor.inc'
        if self.Success:
            if self.get_no() == self.get_max():
                lg.objs.db().albumid = self.get_min()
            else:
                lg.objs.db().albumid = lg.objs.db().next_id()
                self.get_no()
        else:
            sh.com.cancel(f)
    
    def dec(self):
        f = 'controller.AlbumEditor.dec'
        if self.Success:
            if self.get_no() == self.get_min():
                lg.objs.db().albumid = self.get_max()
            else:
                lg.objs.db().albumid = lg.objs.db().prev_id()
                self.get_no()
        else:
            sh.com.cancel(f)
    
    def prev(self,event=None):
        f = 'controller.AlbumEditor.prev'
        if self.Success:
            self.dec()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def next(self,event=None):
        f = 'controller.AlbumEditor.next'
        if self.Success:
            self.inc()
            self.fill()
        else:
            sh.com.cancel(f)
    
    def tracks(self,event=None):
        f = 'controller.AlbumEditor.tracks'
        data = lg.objs.db().tracks()
        if data:
            mes = ''
            for track in data:
                mes += _('Track #:') + ' %d\n' % track[1]
                if track[0]:
                    mes += _('Title:')   + ' %s\n' % track[0]
                if track[4]:
                    mes += _('Bitrate:') + ' %dk\n' % (track[4] // 1000)
                # Length
                if track[5]:
                    minutes = track[5] // 60
                    seconds = track[5] - minutes * 60
                    mes += _('Length:') + ' %d ' % minutes \
                           + _('min')   + ' %d ' % seconds \
                           + _('sec')   + '\n'
                # Rating
                if track[6]:
                    mes += _('Rating:')  + ' %d\n' % track[6]
                    mes += '\n\n'
                    
            gi.objs.tracks().reset()
            gi.objs._tracks.insert(text=mes)
            gi.objs._tracks.show()
        else:
            sh.com.cancel(f)
    
    def delete(self,event=None):
        f = 'controller.AlbumEditor.delete'
        sh.objs.mes (f,_('INFO')
                    ,_('Not implemented yet!')
                    )
    
    def save(self,event=None):
        f = 'controller.AlbumEditor.save'
        sh.objs.mes (f,_('INFO')
                    ,_('Not implemented yet!')
                    )
    
    def create(self,event=None):
        f = 'controller.AlbumEditor.create'
        sh.objs.mes (f,_('INFO')
                    ,_('Not implemented yet!')
                    )
    
    def bindings(self):
        self.gui.widget.protocol("WM_DELETE_WINDOW",self.close)
        self.gui.top_area.btn_nxt.action    = self.next
        self.gui.top_area.btn_prv.action    = self.prev
        self.gui.top_area.btn_spr.action    = self.search_prev_album
        self.gui.top_area.btn_snx.action    = self.search_next_album
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
                ,bindings = '<F4>'
                ,action   = self.tracks
                )
    
    def get_no(self):
        f = 'controller.AlbumEditor.get_no'
        if self.Success:
            lg.objs.db().albumid = sh.Input (title = f
                                            ,value = lg.objs.db().albumid
                                            ).integer()
        else:
            sh.com.cancel(f)
        return lg.objs.db().albumid
    
    def get_min(self):
        f = 'controller.AlbumEditor.get_min'
        if self.Success:
            return sh.Input (title = f
                            ,value = lg.objs.db().min_id()
                            ).integer()
        else:
            sh.com.cancel(f)
            return 0
    
    def get_max(self):
        f = 'controller.AlbumEditor.get_max'
        if self.Success:
            return sh.Input (title = f
                            ,value = lg.objs.db().max_id()
                            ).integer()
        else:
            sh.com.cancel(f)
            return 0
    
    def reset(self):
        f = 'controller.AlbumEditor.reset'
        self.Success = lg.objs.db().Success
        lg.objs._db.albumid = self.get_max()
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
            _max = self.get_max()
            self.gui.top_area.lbl_mtr.text ('%d / %d' % (self.get_no()
                                                        ,_max
                                                        )
                                           )
            if lg.objs.db().albumid < _max:
                self.gui.top_area.btn_nxt.active()
            else:
                self.gui.top_area.btn_nxt.inactive()
            if lg.objs._db.albumid == self.get_min():
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
            self.get_no()
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
                    # insert genre
                    self.gui.body.w_cnt.insert(data[4])
                    self.gui.body.w_com.insert(data[5])
                    self.update()
                else:
                    sh.objs.mes (f,_('ERROR')
                                ,_('Wrong input data: "%s"!') % str(data)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        lg.objs.db().save()
        self.gui.close()



class Objects:
    
    def __init__(self):
        self._editor = None
    
    def editor(self):
        if not self._editor:
            self._editor = AlbumEditor()
        return self._editor


objs = Objects()



if __name__ == '__main__':
    f = 'controller.__main__'
    sg.objs.start()
    objs.editor().show()
    sg.objs.end()
