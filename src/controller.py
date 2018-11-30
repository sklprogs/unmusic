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
        self.gui.bottom_area.btn_trk.action = self.tracks
        self.gui.bottom_area.btn_rec.action = self.create
        self.gui.bottom_area.btn_sav.action = self.save
        self.gui.bottom_area.btn_rld.action = self.fill
        self.gui.bottom_area.btn_del.action = self.delete
        sg.bind (obj      = self.gui
                ,bindings = ['<F5>','<Control-r>']
                ,action   = self.fill
                )
    
    def reset(self):
        f = 'controller.AlbumEditor.reset'
        self.Success = lg.objs.db().Success
        self._no     = lg.objs._db.max_id()
        if str(self._no).isdigit() and self._no > 0:
            pass
        else:
            self._no = 1
            sh.objs.mes (f,_('WARNING')
                        ,_('Wrong input data: "%s"!') % str(self._no)
                        )
        self.fill()
    
    def update(self):
        f = 'controller.AlbumEditor.update'
        if self.Success:
            self._no = sh.Input (title = f
                                ,value = self._no
                                ).integer()
            max_id = lg.objs.db().max_id()
            max_id = sh.Input (title = f
                              ,value = max_id
                              ).integer()
            self.gui.top_area.lbl_mtr.text ('%d / %d' % (self._no
                                                        ,max_id
                                                        )
                                           )
            if self._no < max_id:
                self.gui.top_area.btn_nxt.active()
            else:
                self.gui.top_area.btn_nxt.inactive()
            if self._no == 1:
                self.gui.top_area.btn_prv.inactive()
            else:
                self.gui.top_area.btn_prv.active()
        else:
            sh.com.cancel(f)
    
    def fill(self,event=None):
        f = 'controller.AlbumEditor.fill'
        if self.Success:
            self._no = sh.Input (title = f
                                ,value = self._no
                                ).integer()
            data = lg.objs.db().get_album(self._no)
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
