#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('unmusic','../resources/locale')



class BottomArea:

    def __init__(self,parent):
        self._path_add = sh.objs.pdir().add ('..','resources','buttons'
                                            ,'icon_36x36_add.gif'
                                            )
        self._path_del = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_delete_record.gif'
                                           )
        self._path_rld = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_reload.gif'
                                           )
        self._path_sav = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_save.gif'
                                           )
        self._path_trk = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_tracks.gif'
                                           )
        
        self.pool   = sh.MessagePool(max_size=4)
        self.parent = parent
        self._frames()
        self._buttons()
        self._info()

    def _frames(self):
        self.frm  = sg.Frame (parent = self.parent
                             ,expand = 0
                             ,fill   = 'x'
                             ,side   = 'bottom'
                             )
        self.frmt = sg.Frame (parent = self.frm
                             ,expand = 0
                             ,fill   = 'x'
                             ,side   = 'top'
                             )
        self.frmb = sg.Frame (parent = self.frm
                             ,expand = 0
                             ,fill   = 'x'
                             ,side   = 'bottom'
                             )
        self.frm1 = sg.Frame (parent = self.frmb
                             ,side   = 'left'
                             ,expand = 0
                             ,fill   = 'x'
                             )
        self.frm2 = sg.Frame (parent = self.frmb
                             ,side   = 'right'
                             ,expand = 0
                             ,fill   = 'x'
                             )

    def _buttons(self):
        self.btn_trk = sg.Button (parent   = self.frm1
                                 ,text     = _('Tracks')
                                 ,hint     = _('Edit tracks')
                                 ,side     = 'left'
                                 ,inactive = self._path_trk
                                 ,active   = self._path_trk
                                 ,bindings = ['<F4>','<Control-t>'
                                             ,'<Alt-t>'
                                             ]
                                 )
        self.btn_rec = sg.Button (parent   = self.frm1
                                 ,text     = _('Create')
                                 ,hint     = _('Create a new record')
                                 ,side     = 'left'
                                 ,inactive = self._path_add
                                 ,active   = self._path_add
                                 ,bindings = '<Control-n>'
                                 )
        self.btn_sav = sg.Button (parent   = self.frm1
                                 ,text     = _('Save')
                                 ,hint     = _('Save changes')
                                 ,side     = 'left'
                                 ,inactive = self._path_sav
                                 ,active   = self._path_sav
                                 ,bindings = ['<F2>','<Control-s>']
                                 )
        self.btn_rld = sg.Button (parent   = self.frm2
                                 ,text     = _('Reload')
                                 ,hint     = _('Reload the present record')
                                 ,side     = 'left'
                                 ,inactive = self._path_rld
                                 ,active   = self._path_rld
                                 ,bindings = ['<F5>','<Control-r>']
                                 )
        self.btn_del = sg.Button (parent   = self.frm2
                                 ,text     = _('Delete')
                                 ,hint     = _('Delete the present record')
                                 ,side     = 'left'
                                 ,inactive = self._path_del
                                 ,active   = self._path_del
                                 )

    def _info(self):
        # Bind to 'self.frmt' to avoid bulking and free space
        self.lbl = sg.Label (parent = self.frmb
                            ,text   = ''
                            ,font   = 'Sans 9'
                            )

    def update(self,text):
        self.pool.add(message=text)
        self.lbl.text(arg=self.pool.get())



class TopArea:

    def __init__(self,parent):
        self._values()
        self.parent = parent
        self.gui()

    def _values(self):
        self.prev_inactive = sh.objs.pdir().add ('..','resources'
                                                ,'buttons'
                                                ,'icon_36x36_go_back_off.gif'
                                                )
        self.prev_active   = sh.objs._pdir.add ('..','resources'
                                               ,'buttons'
                                               ,'icon_36x36_go_back.gif'
                                               )
        self.next_inactive = sh.objs._pdir.add ('..','resources'
                                               ,'buttons'
                                               ,'icon_36x36_go_forward_off.gif'
                                               )
        self.next_active   = sh.objs._pdir.add ('..','resources'
                                               ,'buttons'
                                               ,'icon_36x36_go_forward.gif'
                                               )

    def frames(self):
        self.frm = sg.Frame (parent = self.parent
                            ,side   = 'top'
                            ,expand = 0
                            ,fill   = 'x'
                            )
        self.widget = self.parent.widget
    
    def search_albums(self):
        self.btn_spr = sg.Button (parent   = self.frm
                                 ,hint     = _('Search older records')
                                 ,inactive = self.prev_inactive
                                 ,active   = self.prev_active
                                 ,text     = '←'
                                 ,hint_dir = 'bottom'
                                 ,side     = 'left'
                                 )
        self.ent_src = sg.Entry (parent    = self.frm
                                ,Composite = 1
                                ,side      = 'left'
                                )
        self.btn_snx = sg.Button (parent   = self.frm
                                 ,hint     = _('Search newer records')
                                 ,inactive = self.next_inactive
                                 ,active   = self.next_active
                                 ,text     = '→'
                                 ,hint_dir = 'bottom'
                                 ,side     = 'left'
                                 )
        sg.ToolTip (obj        = self.ent_src
                   ,text       = _('Search in albums')
                   ,hint_width = 170
                   ,hint_dir   = 'bottom'
                   )
    
    def search_tracks(self):
        self.ent_sr2 = sg.Entry (parent    = self.frm
                                ,Composite = 1
                                ,side      = 'left'
                                )
        sg.ToolTip (obj        = self.ent_sr2
                   ,text       = _('Search in tracks')
                   ,hint_width = 170
                   ,hint_dir   = 'bottom'
                   )
    
    def meter(self):
        self.btn_prv = sg.Button (parent   = self.frm
                                 ,hint     = _('Go to the preceding record')
                                 ,inactive = self.prev_inactive
                                 ,active   = self.prev_active
                                 ,text     = '←'
                                 ,hint_dir = 'bottom'
                                 ,side     = 'left'
                                 )
        # Show the current record #/total records ratio
        self.lbl_mtr = sg.Label (parent = self.frm
                                ,text   = '0 / 0'
                                ,expand = 0
                                ,side   = 'left'
                                )
        sg.ToolTip (obj        = self.lbl_mtr
                   ,text       = _('Album ID')
                   ,hint_width = 150
                   ,hint_dir   = 'bottom'
                   )
        self.btn_nxt = sg.Button (parent   = self.frm
                                 ,hint     = _('Go to the following record')
                                 ,inactive = self.next_inactive
                                 ,active   = self.next_active
                                 ,text     = '→'
                                 ,hint_dir = 'bottom'
                                 ,side     = 'left'
                                 )
    
    def gui(self):
        self.frames()
        self.search_albums()
        self.meter()
        self.search_tracks()
        self.bindings()

    def bindings(self):
        sg.bind (obj      = self
                ,bindings = '<F3>'
                ,action   = self.focus_album_search
                )
        sg.bind (obj      = self
                ,bindings = '<F6>'
                ,action   = self.focus_track_search
                )
        ''' Binding to '<Button-1>' instead of '<ButtonRelease-1>' will
            not allow to select all contents
        '''
        sg.bind (obj      = self.ent_src
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.focus_album_search
                )
        sg.bind (obj      = self.ent_sr2
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.focus_track_search
                )

    def focus_album_search(self,event=None):
        self.ent_src.focus()
        self.ent_src.select_all()
    
    def focus_track_search(self,event=None):
        self.ent_sr2.focus()
        self.ent_sr2.select_all()



class AlbumEditor:

    def __init__(self):
        self.obj    = sg.Top(parent=sg.objs.root())
        self.widget = self.obj.widget
        self.icon()
        self.title()
        ''' For some reason, introducing an additional Frame into Top
            does not allow to expand embedded widgets
        '''
        self.top_area    = TopArea(parent=self.obj)
        self.body        = Body(parent=self.obj)
        self.bottom_area = BottomArea(parent=self.obj)
        self.bindings()
        sg.Geometry(parent=self.obj)

    def bindings(self):
        ''' #todo: Cannot use Delete + smth bindings, e.g.
            '<Control-Delete>' (TextBox reacts to Delete)
        '''
        sg.bind (obj      = self
                ,bindings = '<Escape>'
                ,action   = sg.Geometry(parent=self).minimize
                )
        sg.bind (obj      = self
                ,bindings = '<Control-q>'
                ,action   = self.close
                )

    def title(self,text=None):
        if not text:
            text = _('Album Editor')
        self.obj.title(text=text)

    def icon(self,path=None):
        if path:
            self.obj.icon(path)
        else:
            self.obj.icon (sh.objs.pdir().add ('..','resources'
                                              ,'unmusic.gif'
                                              )
                          )

    def show(self,event=None):
        self.obj.show()
        
    def close(self,event=None):
        self.obj.close()



class Body:

    def __init__(self,parent):
        self.parent = parent
        self.gui()

    def reset(self,event=None):
        self.w_art.clear_text()
        self.w_alb.clear_text()
        self.w_yer.clear_text()
        self.w_cnt.clear_text()
        self.w_com.clear_text()
        self.w_art.focus()

    def gui(self):
        self.widget = self.parent.widget
        self.frames()
        self.entries()
        self.labels()
        self.w_art.focus()

    def frames(self):
        self.frm_man = sg.Frame (parent = self.parent
                                ,expand = 1
                                ,fill   = 'both'
                                ,side   = 'top'
                                )
        self.frm_lft = sg.Frame (parent = self.frm_man
                                ,expand = 0
                                ,side   = 'left'
                                )
        self.frm_rht = sg.Frame (parent = self.frm_man
                                ,expand = 1
                                ,fill   = 'x'
                                ,side   = 'left'
                                ,ipadx  = 150
                                )
        self.frm_btn = sg.Frame (parent = self.parent
                                ,expand = 0
                                ,side   = 'bottom'
                                )
        self.frm_btl = sg.Frame (parent = self.frm_btn
                                ,expand = 0
                                ,fill   = 'x'
                                ,side   = 'left'
                                )
        self.frm_btr = sg.Frame (parent = self.frm_btn
                                ,expand = 0
                                ,fill   = 'x'
                                ,side   = 'right'
                                )

    def entries(self):
        self.w_art = sg.Entry (parent    = self.frm_rht
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_alb = sg.Entry (parent    = self.frm_rht
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_yer = sg.Entry (parent    = self.frm_rht
                              ,Composite = True
                              ,expand    = 1
                              ,ipady     = 1
                              ,fill      = 'both'
                              )
        self.w_cnt = sg.Entry (parent    = self.frm_rht
                              ,Composite = True
                              ,expand    = 1
                              ,ipady     = 1
                              ,fill      = 'both'
                              )
        self.w_com = sg.Entry (parent    = self.frm_rht
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
    
    def labels(self):
        sg.Label (parent = self.frm_lft
                 ,text   = _('Artist:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Album:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Year:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Country (2 letters):')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Comment:')
                 ,ipady  = 2
                 )



class Objects:
    
    def __init__(self):
        self._tracks = None
    
    def tracks(self):
        if self._tracks is None:
            self._tracks = sg.TextBox(parent=sg.Top(parent=sg.objs.root()))
            self._tracks.title(_('Tracks:'))
            sg.Geometry(parent=self._tracks.parent).set('1024x768')
        return self._tracks



objs = Objects()



if __name__ == '__main__':
    sg.objs.start()
    editor = AlbumEditor()
    editor.show()
    sg.objs.end()
