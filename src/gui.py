#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg

PRODUCT = 'unmusic'
# Do not localize (being stored in DB)
GENRES = ('?','Ambient','Black Metal','Blues','Brutal Death/Grindcore'
         ,'Brutal Death Metal','Classical','Death Metal','Death/Black'
         ,'Death/Thrash','Electronic','Ethnic','Heavy Metal','Game'
         ,'Grindcore','Goregrind','Metal','Pop','Rap','Relaxation'
         ,'Soundtrack','Thrash Metal','Vocal'
         )

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install(PRODUCT,'../resources/locale')



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
        # Bind to 'self.frmb' to avoid bulking and free space
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
                                 ,bindings = '<Alt-Left>'
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
                                 ,bindings = '<Alt-Right>'
                                 )
    
    def gui(self):
        self.frames()
        self.search_albums()
        self.meter()
        self.search_tracks()
        self.rating()
        self.bindings()
        
    def rating(self):
        sg.Label (parent = self.frm
                 ,text   = _('Rating:')
                 ,ipady  = 2
                 )
        self.w_rtg = sg.OptionMenu (parent = self.frm
                                   ,items  = (0,1,2,3,4,5,6,7,8,9,10)
                                   ,side   = 'left'
                                   )

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
        self.parent = sg.Top(parent=sg.objs.root())
        self.widget = self.parent.widget
        self.icon()
        self.title()
        ''' For some reason, introducing an additional Frame into Top
            does not allow to expand embedded widgets
        '''
        self.top_area    = TopArea(parent=self.parent)
        self.body        = Body(parent=self.parent)
        self.bottom_area = BottomArea(parent=self.parent)
        self.bindings()
        sg.Geometry(parent=self.parent)

    def dump(self,event=None):
        return (self.body.w_alb.get(),self.body.w_art.get()
               ,self.body.w_yer.get(),self.body.w_gnr.choice
               ,self.body.w_cnt.get(),self.body.w_com.get()
               )
    
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
        self.parent.title(text=text)

    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon (sh.objs.pdir().add ('..','resources'
                                                 ,PRODUCT + '.gif'
                                                 )
                             )

    def show(self,event=None):
        self.parent.show()
        
    def close(self,event=None):
        self.parent.close()



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
        self.labels()
        self.entries()
        self.menus()
        self.w_art.focus()

    def frames(self):
        self.frm_prm = sg.Frame (parent = self.parent
                                ,expand = 1
                                ,fill   = 'both'
                                ,side   = 'top'
                                )
        self.frm_lft = sg.Frame (parent = self.frm_prm
                                ,expand = 1
                                ,side   = 'left'
                                )
        self.frm_rht = sg.Frame (parent = self.frm_prm
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

    def menus(self):
        self.w_gnr = sg.OptionMenu (parent = self.frm_rht
                                   ,items  = GENRES
                                   ,side   = 'left'
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
        self.w_bit = sg.Entry (parent    = self.frm_rht
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_len = sg.Entry (parent    = self.frm_rht
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
        sg.Label (parent = self.frm_lft
                 ,text   = _('Mean bitrate:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Total length:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Genre:')
                 ,ipady  = 2
                 )



class Menu:
    
    def __init__(self):
        self._a = []
        self.parent = sg.Top(sg.objs.root())
        self.gui()
    
    def bindings(self):
        sg.bind (obj      = self.parent
                ,bindings = '<Escape>'
                ,action   = sg.Geometry(parent=self.parent).minimize
                )
        if len(self._a) > 0:
            for i in range(len(self._a)):
                sg.bind (obj      = self._a[i]
                        ,bindings = '<Home>'
                        ,action   = self._a[0].focus
                        )
                sg.bind (obj      = self._a[i]
                        ,bindings = '<End>'
                        ,action   = self._a[-1].focus
                        )
                if i > 0:
                    sg.bind (obj      = self._a[i]
                            ,bindings = '<Up>'
                            ,action   = self._a[i-1].focus
                            )
                else:
                    sg.bind (obj      = self._a[i]
                            ,bindings = '<Up>'
                            ,action   = self._a[-1].focus
                            )
                if i < len(self._a) - 1:
                    sg.bind (obj      = self._a[i]
                            ,bindings = '<Down>'
                            ,action   = self._a[i+1].focus
                            )
                else:
                    sg.bind (obj      = self._a[i]
                            ,bindings = '<Down>'
                            ,action   = self._a[0].focus
                            )
    
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon (sh.objs.pdir().add ('..','resources'
                                                 ,PRODUCT + '.gif'
                                                 )
                             )
    
    def title(self,text=''):
        if not text:
            text = PRODUCT
        self.parent.title(text)
    
    def buttons(self):
        self._a.append (sg.Button (parent = self.parent
                                  ,text   = _('Album Editor')
                                  ,side   = 'top'
                                  )
                       )
        self._a.append (sg.Button (parent     = self.parent
                                  ,text       = _('Prepare files')
                                  ,hint       = _('Move sub-folders to a root folder, split large lossless files, etc.')
                                  ,hint_width = 600
                                  ,side       = 'top'
                                  )
                       )
        self._a.append (sg.Button (parent = self.parent
                                  ,text   = _('Collect tags')
                                  ,side   = 'top'
                                  )
                       )
        self._a.append (sg.Button (parent     = self.parent
                                  ,text       = _('Obfuscate')
                                  ,hint       = _('Clear tags, name folders by ALBUMID, etc.')
                                  ,hint_width = 600
                                  ,side       = 'top'
                                  )
                       )
        self._a.append (sg.Button (parent = self.parent
                                  ,text   = _('Quit')
                                  ,side   = 'top'
                                  )
                       )
    
    def gui(self):
        self.buttons()
        self.icon()
        self.title()
        self.bindings()
        if len(self._a) > 0:
            self._a[0].focus()
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()



class Tracks:
    
    def __init__(self,width=0,height=768):
        self.values()
        self.pool    = sh.MessagePool(max_size=3)
        self.parent  = sg.Top(sg.objs.root())
        self.widget  = self.parent.widget
        self._width  = width
        self._height = height
        self.gui()
    
    def _info(self):
        self.lbl = sg.Label (parent = self.frm_btn
                            ,text   = ''
                            ,font   = 'Sans 9'
                            )

    def update(self,text):
        self.pool.add(message=text)
        self.lbl.text(arg=self.pool.get())
    
    def dump(self):
        new = []
        for track in self._tracks:
            new.append(track.dump())
        return new
    
    def values(self):
        self._tracks   = []
        self._path_rld = sh.objs.pdir().add ('..','resources','buttons'
                                            ,'icon_36x36_reload.gif'
                                            )
        self._path_sav = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_save.gif'
                                           )
    
    def buttons(self):
        self.btn_rld = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Reload')
                                 ,hint     = _('Reload the present record')
                                 ,side     = 'left'
                                 ,inactive = self._path_rld
                                 ,active   = self._path_rld
                                 ,bindings = ['<F5>','<Control-r>']
                                 )
        self.btn_sav = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Save')
                                 ,hint     = _('Save changes')
                                 ,side     = 'right'
                                 ,inactive = self._path_sav
                                 ,active   = self._path_sav
                                 ,bindings = ['<F2>','<Control-s>']
                                 )
    
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon (sh.objs.pdir().add ('..','resources'
                                                 ,PRODUCT + '.gif'
                                                 )
                             )
    
    def reset(self):
        for track in self._tracks:
            track.frm_prm.widget.destroy()
        self._tracks = []
    
    def after_add(self):
        sg.objs.root().widget.update_idletasks()
        max_x = self.label.widget.winfo_reqwidth()
        max_y = self.label.widget.winfo_reqheight()
        self.canvas.region (x        = max_x
                           ,y        = max_y
                           ,x_border = 10
                           ,y_border = 20
                           )
        if not self._width:
            self._width = max_x + 40
        sg.Geometry(parent=self.parent).set ('%dx%d' % (self._width
                                                       ,self._height
                                                       )
                                            )
        self.canvas.move_top()
        self.canvas.widget.xview_moveto(0)
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def title(self,text=None):
        if not text:
            text = _('Tracks:')
        self.parent.title(text=text)
    
    def frames(self):
        self.frm_prm = sg.Frame (parent = self.parent)
        self.frm_hor = sg.Frame (parent = self.frm_prm
                                ,expand = False
                                ,fill   = 'x'
                                ,side   = 'bottom'
                                )
        self.frm_ver = sg.Frame (parent = self.frm_prm
                                ,expand = False
                                ,fill   = 'y'
                                ,side   = 'right'
                                )
        # This frame must be created after the bottom frame
        self.frm_sec = sg.Frame (parent = self.frm_prm)
        self.frm_btn = sg.Frame (parent = self.frm_prm
                                ,expand = False
                                ,fill   = 'x'
                                ,side   = 'bottom'
                                )
    
    def gui(self):
        self.frames()
        self.widgets()
        self._info()
        self.buttons()
        self.icon()
        self.title()
        self.canvas.top_bindings(self.parent)
    
    def widgets(self):
        self.canvas = sg.Canvas(parent = self.frm_sec)
        self.label  = sg.Label (parent = self.frm_sec
                               ,text   = _('Tracks:')
                               ,expand = True
                               ,fill   = 'both'
                               )
        self.canvas.embed(self.label)
        self.yscroll = sg.Scrollbar (parent = self.frm_ver
                                    ,scroll = self.canvas
                                    )
        self.canvas.focus()
        
    def add(self,event=None,Extended=False):
        self._tracks.append(Track(self.label,Extended))
        return self._tracks[-1]



class Track:
    
    def __init__(self,parent,Extended=False):
        self.parent   = parent
        self.Extended = Extended
        self.gui()
    
    def dump(self,event=None):
        return (self.w_tit.get(),self.w_lyr.get(),self.w_com.get()
               ,int(self.w_rtg.choice)
               )
    
    # Useful for debug purposes only
    def show(self,event=None):
        self.parent.show()
    
    def frames(self):
        self.frm_prm = sg.Frame (parent = self.parent
                                ,expand = False
                                ,fill   = 'x'
                                )
        self.frm_lft = sg.Frame (parent = self.frm_prm
                                ,side   = 'left'
                                )
        self.frm_rht = sg.Frame (parent = self.frm_prm
                                ,side   = 'left'
                                )
    
    def labels(self):
        if self.Extended:
            sg.Label (parent = self.frm_lft
                     ,text   = _('Album ID:')
                     ,ipady  = 2
                     )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Track #:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Title:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Lyrics:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Comment:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Bitrate:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Length:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frm_lft
                 ,text   = _('Rating:')
                 ,ipady  = 2
                 )
    
    def entries(self):
        if self.Extended:
            self.w_aid = sg.Entry (parent    = self.frm_rht
                                  ,Composite = True
                                  ,expand    = 1
                                  ,fill      = 'x'
                                  ,ipady     = 1
                                  )
        self.w_tno = sg.Entry (parent    = self.frm_rht
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_tit = sg.Entry (parent    = self.frm_rht
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_lyr = sg.Entry (parent    = self.frm_rht
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_com = sg.Entry (parent    = self.frm_rht
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_bit = sg.Entry (parent    = self.frm_rht
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_len = sg.Entry (parent    = self.frm_rht
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
    
    def menus(self):
        self.w_rtg = sg.OptionMenu (parent = self.frm_rht
                                   ,items  = (0,1,2,3,4,5,6,7,8,9,10)
                                   ,side   = 'left'
                                   )
    
    def gui(self):
        self.frames()
        self.labels()
        self.entries()
        self.menus()



class Objects:
    
    def __init__(self):
        self._tracks = None
    
    def tracks(self):
        if self._tracks is None:
            self._tracks = Tracks()
        return self._tracks



objs = Objects()



if __name__ == '__main__':
    sg.objs.start()
    Menu().show()
    sg.objs.end()
