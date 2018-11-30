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
            sh.objs.mes (f,_('INFO')
                        ,_('Not implemented yet!')
                        )
        else:
            sh.com.cancel(f)
    
    def search_album(self,event=None):
        f = 'controller.AlbumEditor.search_album'
        if self.Success:
            sh.objs.mes (f,_('INFO')
                        ,_('Not implemented yet!')
                        )
        else:
            sh.com.cancel(f)
    
    def search_next_track(self,event=None):
        f = 'controller.AlbumEditor.search_next_track'
        if self.Success:
            sh.objs.mes (f,_('INFO')
                        ,_('Not implemented yet!')
                        )
        else:
            sh.com.cancel(f)
    
    def search_prev_track(self,event=None):
        f = 'controller.AlbumEditor.search_prev_track'
        if self.Success:
            sh.objs.mes (f,_('INFO')
                        ,_('Not implemented yet!')
                        )
        else:
            sh.com.cancel(f)
    
    def search_next_album(self,event=None):
        f = 'controller.AlbumEditor.search_next_album'
        if self.Success:
            sh.objs.mes (f,_('INFO')
                        ,_('Not implemented yet!')
                        )
        else:
            sh.com.cancel(f)
    
    def search_prev_album(self,event=None):
        f = 'controller.AlbumEditor.search_prev_album'
        if self.Success:
            sh.objs.mes (f,_('INFO')
                        ,_('Not implemented yet!')
                        )
        else:
            sh.com.cancel(f)
    
    def inc(self):
        f = 'controller.AlbumEditor.inc'
        if self.Success:
            if self.get_no() == self.get_max():
                self._no = self.get_min()
            else:
                self._no = lg.objs.db().next_id(self._no)
                self.get_no()
        else:
            sh.com.cancel(f)
    
    def dec(self):
        f = 'controller.AlbumEditor.dec'
        if self.Success:
            if self.get_no() == self.get_min():
                self._no = self.get_max()
            else:
                self._no = lg.objs.db().prev_id(self._no)
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
        sh.objs.mes (f,_('INFO')
                    ,_('Not implemented yet!')
                    )
    
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
        self.gui.top_area.btn_sp2.action    = self.search_prev_track
        self.gui.top_area.btn_snx.action    = self.search_next_album
        self.gui.top_area.btn_sn2.action    = self.search_next_track
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
    
    def get_no(self):
        f = 'controller.AlbumEditor.get_no'
        if self.Success:
            self._no = sh.Input (title = f
                                ,value = self._no
                                ).integer()
        else:
            sh.com.cancel(f)
        return self._no
    
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
    
    def values(self):
        self.Success = True
        self._no     = 1
    
    def reset(self):
        f = 'controller.AlbumEditor.reset'
        self.values()
        self.Success = lg.objs.db().Success
        self._no     = self.get_max()
        self.fill()
    
    def update(self):
        f = 'controller.AlbumEditor.update'
        if self.Success:
            _max = self.get_max()
            self.gui.top_area.lbl_mtr.text ('%d / %d' % (self.get_no()
                                                        ,_max
                                                        )
                                           )
            if self._no < _max:
                self.gui.top_area.btn_nxt.active()
            else:
                self.gui.top_area.btn_nxt.inactive()
            if self._no == self.get_min():
                self.gui.top_area.btn_prv.inactive()
            else:
                self.gui.top_area.btn_prv.active()
        else:
            sh.com.cancel(f)
    
    def fill(self,event=None):
        f = 'controller.AlbumEditor.fill'
        if self.Success:
            data = lg.objs.db().get_album(self.get_no())
            if data:
                if len(data) == 6:
                    self.gui.bottom_area.update (_('Load #%d.') \
                                                 % self._no
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
