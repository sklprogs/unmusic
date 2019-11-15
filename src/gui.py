#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh

import gettext
import skl_shared.gettext_windows
skl_shared.gettext_windows.setup_env()
gettext.install('unmusic','../resources/locale')

PLAY = (_('Play')
       ,_('All')
       ,_('Good')
       ,_('Best')
       )

ITEMS_YEAR = (_('Not set'),'=','>=','<=')
ICON = sh.objs.pdir().add('..','resources','unmusic.gif')


class Copy:
    
    def __init__(self):
        self._width = 7
        self.parent = sh.Top()
        self.gui()
    
    def limit(self):
        self.lbl_lim = sh.Label (parent = self.frm_lim
                                ,text   = _('Limit:')
                                ,side   = 'left'
                                ,width  = self._width
                                )
        self.ent_lim = sh.Entry (parent = self.frm_lim
                                ,side   = 'left'
                                ,width  = 5
                                )
        self.ent_lim.insert(100)
    
    def reset(self,event=None):
        self.opt_gnr.set(_('All'))
        self.opt_yer.set(_('Not set'))
        self.opt_src.set(_('external collection'))
        self.opt_trg.set(_('mobile collection'))
        self.ent_yer.reset()
        self.ent_lim.reset()
        self.ent_lim.insert(100)
        self.btn_str.focus()
    
    def bindings(self):
        sh.com.bind (obj      = self.parent
                    ,bindings = ('<Escape>','<Control-w>','<Control-q>')
                    ,action   = self.close
                    )
        self.opt_yer.action = self.ent_yer.focus
    
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon(ICON)
    
    def title(self,arg=None):
        if not arg:
            arg = _('Copy music')
        self.parent.title(arg)
    
    def frames(self):
        self.frm_prm = sh.Frame (parent = self.parent
                                ,expand = True
                                ,fill   = 'both'
                                )
        self.frm_gnr = sh.Frame (parent = self.frm_prm
                                ,expand = True
                                ,fill   = 'x'
                                ,side   = 'top'
                                )
        self.frm_yer = sh.Frame (parent = self.frm_prm
                                ,expand = True
                                ,fill   = 'x'
                                ,side   = 'top'
                                )
        self.frm_src = sh.Frame (parent = self.frm_prm
                                ,expand = True
                                ,fill   = 'x'
                                ,side   = 'top'
                                )
        
        self.frm_trg = sh.Frame (parent = self.frm_prm
                                ,expand = True
                                ,fill   = 'x'
                                ,side   = 'top'
                                )
        self.frm_lim = sh.Frame (parent = self.frm_prm
                                ,expand = True
                                ,fill   = 'x'
                                ,side   = 'top'
                                )
        self.frm_btn = sh.Frame (parent = self.frm_prm
                                ,expand = True
                                ,fill   = 'x'
                                ,side   = 'bottom'
                                ,pady   = 7
                                )
        self.frm_btl = sh.Frame (parent = self.frm_btn
                                ,side   = 'left'
                                )
        self.frm_btr = sh.Frame (parent = self.frm_btn
                                ,side   = 'right'
                                )
    
    def buttons(self):
        self.btn_cls = sh.Button (parent = self.frm_btl
                                 ,text   = _('Close')
                                 ,side   = 'left'
                                 ,action = self.close
                                 )
        self.btn_rst = sh.Button (parent = self.frm_btl
                                 ,text   = _('Reset')
                                 ,side   = 'right'
                                 ,action = self.reset
                                 )
        self.btn_str = sh.Button (parent = self.frm_btr
                                 ,text   = _('Start')
                                 ,side   = 'right'
                                 ,Focus  = True
                                 )
    
    def year(self):
        self.lbl_yer = sh.Label (parent = self.frm_yer
                                ,text   = _('Year:')
                                ,side   = 'left'
                                ,fill   = None
                                ,expand = False
                                ,width  = self._width
                                )
        self.opt_yer = sh.OptionMenu (parent  = self.frm_yer
                                     ,items   = ITEMS_YEAR
                                     ,side    = 'left'
                                     ,default = _('Not set')
                                     )
        self.ent_yer = sh.Entry (parent = self.frm_yer
                                ,side   = 'left'
                                ,fill   = None
                                ,expand = None
                                ,width  = 4
                                )
    
    def genre(self):
        self.lbl_gnr = sh.Label (parent = self.frm_gnr
                                ,text   = _('Genres:')
                                ,side   = 'left'
                                ,fill   = None
                                ,expand = False
                                ,width  = self._width
                                )
        self.opt_gnr = sh.OptionMenu (parent  = self.frm_gnr
                                     ,items   = (_('All'),_('Heavy')
                                                ,_('Light')
                                                )
                                     ,side    = 'left'
                                     ,default = _('All')
                                     )
    
    def source(self):
        self.lbl_src = sh.Label (parent = self.frm_src
                                ,text   = _('Read:')
                                ,side   = 'left'
                                ,fill   = None
                                ,expand = False
                                ,width  = self._width
                                )
        self.opt_src = sh.OptionMenu (parent  = self.frm_src
                                     ,items   = (_('external collection')
                                                ,_('local collection')
                                                )
                                     ,side    = 'left'
                                     ,default = _('external collection')
                                     )
    
    def target(self):
        self.lbl_trg = sh.Label (parent = self.frm_trg
                                ,text   = _('Write:')
                                ,side   = 'left'
                                ,fill   = None
                                ,expand = False
                                ,width  = self._width
                                )
        self.opt_trg = sh.OptionMenu (parent  = self.frm_trg
                                     ,items   = (_('mobile collection')
                                                ,_('local collection')
                                                )
                                     ,side    = 'left'
                                     ,default = _('mobile collection')
                                     )
    
    def gui(self):
        self.frames()
        self.genre()
        self.year()
        self.source()
        self.target()
        self.limit()
        self.buttons()
        self.icon()
        self.title()
        self.bindings()
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()



class ImageViewer:
    
    def __init__(self):
        self.gui()
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def bindings(self):
        sh.com.bind (obj      = self.parent
                    ,bindings = ('<Escape>','<Control-w>','<Control-q>'
                                ,'<ButtonRelease-1>'
                                )
                    ,action   = self.close
                    )
    
    def title(self,arg=None):
        if not arg:
            arg = _('Image:')
        self.parent.title(arg)
    
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon(ICON)
    
    def gui(self):
        self.parent = sh.Top()
        self.lbl = sh.Label (parent = self.parent
                            ,text   = _('Image:')
                            ,expand = True
                            ,fill   = 'both'
                            )
        self.title()
        self.icon()
        self.bindings()



class AlbumEditor:

    def __init__(self):
        self.values()
        self.parent = sh.Top (icon  = ICON
                             ,title = _('Album Editor')
                             )
        self.widget = self.parent.widget
        self.pool   = sh.lg.MessagePool(max_size=4)
        self.gui()
    
    def present(self):
        self.cbx_loc = sh.CheckBox (parent = self.frm_prs
                                   ,side   = 'left'
                                   )
        self.lbl_loc = sh.Label (parent = self.frm_prs
                                ,text   = _('local collection')
                                ,side   = 'left'
                                )
        self.cbx_ext = sh.CheckBox (parent = self.frm_prs
                                   ,side   = 'left'
                                   )
        self.lbl_ext = sh.Label (parent = self.frm_prs
                                ,text   = _('external collection')
                                ,side   = 'left'
                                )
        self.cbx_mob = sh.CheckBox (parent = self.frm_prs
                                   ,side   = 'left'
                                   )
        self.lbl_mob = sh.Label (parent = self.frm_prs
                                ,text   = _('mobile collection')
                                ,side   = 'left'
                                )
        ''' We can call 'cbx_loc.widget.config(state="disabled")'
            but this makes the checkbox indistinguishable.
        '''
        self.cbx_loc.reset(action=self.cbx_loc.toggle)
        self.cbx_ext.reset(action=self.cbx_ext.toggle)
        self.cbx_mob.reset(action=self.cbx_mob.toggle)
    
    def clear_ids(self,event=None):
        self.ent_ids.focus()
        self.ent_ids.clear_text()
    
    def clear_album_search(self,event=None):
        self.ent_src.focus()
        self.ent_src.clear_text()
    
    def clear_track_search(self,event=None):
        self.ent_sr2.focus()
        self.ent_sr2.clear_text()
    
    def focus_ids(self,event=None):
        self.ent_ids.focus()
        self.ent_ids.select_all()
    
    def search_ids(self):
        self.ent_ids = sh.Entry (parent = self.frm
                                ,side   = 'left'
                                ,width  = 5
                                )
        sh.ToolTip (obj  = self.ent_ids
                   ,text = _('Search an album by ID')
                   ,hdir = 'bottom'
                   )
    
    def image(self):
        self.lbl_img = sh.Label (parent = self.frm_img
                                ,text   = _('Image:')
                                ,side   = 'right'
                                ,anchor = 'w'
                                ,expand = True
                                ,fill   = 'both'
                                )
    
    def bottom(self):
        self.opt_gnr = sh.OptionMenu (parent = self.frm_rht
                                     ,side   = 'left'
                                     )
        self.btn_rld = sh.Button (parent   = self.frm1
                                 ,text     = _('Reload')
                                 ,hint     = _('Reload the present record')
                                 ,side     = 'left'
                                 ,inactive = self._path_rld
                                 ,active   = self._path_rld
                                 ,bindings = ('<F5>','<Control-r>')
                                 )
        self.btn_rec = sh.Button (parent   = self.frm1
                                 ,text     = _('Create')
                                 ,hint     = _('Create a new record')
                                 ,side     = 'left'
                                 ,inactive = self._path_add
                                 ,active   = self._path_add
                                 ,bindings = '<Control-n>'
                                 )
        self.btn_del = sh.Button (parent   = self.frm1
                                 ,text     = _('Delete')
                                 ,hint     = _('Delete the present record')
                                 ,side     = 'left'
                                 ,inactive = self._path_del
                                 ,active   = self._path_del
                                 )
        self.btn_dez = sh.Button (parent   = self.frm2
                                 ,text     = _('Decypher')
                                 ,hint     = _('Decypher text (Caesar algorithm)')
                                 ,side     = 'left'
                                 ,inactive = self._path_dez
                                 ,active   = self._path_dez
                                 )
        self.btn_cyp = sh.Button (parent   = self.frm2
                                 ,text     = _('Cypher')
                                 ,hint     = _('Cypher text (Caesar algorithm)')
                                 ,side     = 'left'
                                 ,inactive = self._path_cyp
                                 ,active   = self._path_cyp
                                 )
        self.btn_dec = sh.Button (parent   = self.frm2
                                 ,text     = _('Decode')
                                 ,hint     = _('Decode back to cp1251')
                                 ,side     = 'left'
                                 ,inactive = self._path_dec
                                 ,active   = self._path_dec
                                 )
        self.btn_sav = sh.Button (parent   = self.frm2
                                 ,text     = _('Save')
                                 ,hint     = _('Save changes')
                                 ,side     = 'left'
                                 ,inactive = self._path_sav
                                 ,active   = self._path_sav
                                 ,bindings = ('<F2>','<Control-s>')
                                 )
        self.btn_trk = sh.Button (parent   = self.frm2
                                 ,text     = _('Tracks')
                                 ,hint     = _('Edit tracks')
                                 ,side     = 'left'
                                 ,inactive = self._path_trk
                                 ,active   = self._path_trk
                                 ,bindings = ('<F4>','<Control-t>'
                                             ,'<Alt-t>'
                                             )
                                 )

    def update_info(self,text):
        self.pool.add(message=text)
        self.lbl.text(arg=self.pool.get())
    
    def entries(self):
        self.ent_art = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,fill   = 'x'
                                ,ipady  = 1
                                )
        self.ent_alb = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,fill   = 'x'
                                ,ipady  = 1
                                )
        self.ent_yer = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,ipady  = 1
                                ,fill   = 'both'
                                )
        self.ent_cnt = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,ipady  = 1
                                ,fill   = 'both'
                                )
        self.ent_com = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,fill   = 'x'
                                ,ipady  = 1
                                )
        self.ent_bit = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,fill   = 'x'
                                ,ipady  = 1
                              )
        self.ent_len = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,fill   = 'x'
                                ,ipady  = 1
                                )
    
    def labels(self):
        sh.Label (parent = self.frm_lft
                 ,text   = _('Artist:')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Album:')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Year:')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Country (2 letters):')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Comment:')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Mean bitrate:')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Total length:')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Genre:')
                 ,ipady  = 2
                 )
        # Bind to 'self.frmb' to avoid bulking and free space
        self.lbl = sh.Label (parent = self.frmb
                            ,text   = ''
                            ,font   = 'Sans 9'
                            )
    
    def clear_entries(self,event=None):
        self.ent_art.clear_text()
        self.ent_alb.clear_text()
        self.ent_yer.clear_text()
        self.ent_cnt.clear_text()
        self.ent_com.clear_text()
        self.ent_art.focus()
    
    def gui(self):
        self.frames()
        self.search_albums()
        self.search_ids()
        self.meter()
        self.search_tracks()
        self.menus()
        self.labels()
        self.entries()
        self.present()
        self.image()
        self.bottom()
        self.bindings()
        self.ent_art.focus()
        sh.Geometry(self.parent)
    
    def search_albums(self):
        self.btn_spr = sh.Button (parent   = self.frm
                                 ,hint     = _('Search older records')
                                 ,inactive = self.prev_inactive
                                 ,active   = self.prev_active
                                 ,text     = '←'
                                 ,hdir     = 'bottom'
                                 ,side     = 'left'
                                 )
        self.ent_src = sh.Entry (parent = self.frm
                                ,side   = 'left'
                                )
        self.btn_snx = sh.Button (parent   = self.frm
                                 ,hint     = _('Search newer records')
                                 ,inactive = self.next_inactive
                                 ,active   = self.next_active
                                 ,text     = '→'
                                 ,hdir     = 'bottom'
                                 ,side     = 'left'
                                 )
        sh.ToolTip (obj  = self.ent_src
                   ,text = _('Search in albums')
                   ,hdir = 'bottom'
                   )
    
    def search_tracks(self):
        self.ent_sr2 = sh.Entry (parent = self.frm
                                ,side   = 'left'
                                )
        sh.ToolTip (obj  = self.ent_sr2
                   ,text = _('Search in tracks')
                   ,hdir = 'bottom'
                   )
    
    def meter(self):
        self.btn_prv = sh.Button (parent   = self.frm
                                 ,hint     = _('Go to the preceding record')
                                 ,inactive = self.prev_inactive
                                 ,active   = self.prev_active
                                 ,text     = '←'
                                 ,hdir     = 'bottom'
                                 ,side     = 'left'
                                 ,bindings = '<Alt-Left>'
                                 )
        # Show the current record #/total records ratio
        self.lbl_mtr = sh.Label (parent = self.frm
                                ,text   = '0 / 0'
                                ,expand = False
                                ,side   = 'left'
                                )
        sh.ToolTip (obj  = self.lbl_mtr
                   ,text = _('Album ID')
                   ,hdir = 'bottom'
                   )
        self.btn_nxt = sh.Button (parent   = self.frm
                                 ,hint     = _('Go to the following record')
                                 ,inactive = self.next_inactive
                                 ,active   = self.next_active
                                 ,text     = '→'
                                 ,hdir     = 'bottom'
                                 ,side     = 'left'
                                 ,bindings = '<Alt-Right>'
                                 )
    
    def menus(self):
        self.opt_rtg = sh.OptionMenu (parent = self.frm
                                     ,items  = (0,1,2,3,4,5,6,7,8,9,10)
                                     ,side   = 'left'
                                     )
        self.opt_ply = sh.OptionMenu (parent = self.frm
                                     ,items  = PLAY
                                     ,side   = 'left'
                                     )

    def bindings(self):
        ''' #todo: Cannot use Delete + smth bindings, e.g.
            '<Control-Delete>' (TextBox reacts to Delete)
        '''
        sh.com.bind (obj      = self
                    ,bindings = '<Escape>'
                    ,action   = sh.Geometry(self).minimize
                    )
        sh.com.bind (obj      = self
                    ,bindings = '<Control-q>'
                    ,action   = self.close
                    )
        sh.com.bind (obj      = self
                    ,bindings = '<F3>'
                    ,action   = self.focus_album_search
                    )
        sh.com.bind (obj      = self
                    ,bindings = '<F6>'
                    ,action   = self.focus_ids
                    )
        sh.com.bind (obj      = self
                    ,bindings = '<F7>'
                    ,action   = self.focus_track_search
                    )
        ''' Binding to '<Button-1>' instead of '<ButtonRelease-1>' will
            not allow to select all contents
        '''
        sh.com.bind (obj      = self.ent_src
                    ,bindings = '<ButtonRelease-1>'
                    ,action   = self.focus_album_search
                    )
        sh.com.bind (obj      = self.ent_src
                    ,bindings = '<ButtonRelease-3>'
                    ,action   = self.clear_album_search
                    )
        sh.com.bind (obj      = self.ent_sr2
                    ,bindings = '<ButtonRelease-1>'
                    ,action   = self.focus_track_search
                    )
        sh.com.bind (obj      = self.ent_sr2
                    ,bindings = '<ButtonRelease-3>'
                    ,action   = self.clear_track_search
                    )
        sh.com.bind (obj      = self.ent_ids
                    ,bindings = '<ButtonRelease-1>'
                    ,action   = self.focus_ids
                    )
        sh.com.bind (obj      = self.ent_ids
                    ,bindings = '<ButtonRelease-3>'
                    ,action   = self.clear_ids
                    )

    def focus_album_search(self,event=None):
        self.ent_src.focus()
        self.ent_src.select_all()
    
    def focus_track_search(self,event=None):
        self.ent_sr2.focus()
        self.ent_sr2.select_all()
        
    def frames(self):
        self.frm = sh.Frame (parent = self.parent
                            ,side   = 'top'
                            ,expand = False
                            ,fill   = 'x'
                            )
        self.frm_prm = sh.Frame (parent = self.parent
                                ,expand = True
                                ,fill   = 'both'
                                ,side   = 'top'
                                )
        self.frm_lft = sh.Frame (parent = self.frm_prm
                                ,expand = True
                                ,side   = 'left'
                                )
        self.frm_rht = sh.Frame (parent = self.frm_prm
                                ,expand = True
                                ,fill   = 'x'
                                ,side   = 'left'
                                )
        self.frm_prs = sh.Frame (parent = self.frm_rht
                                ,expand = False
                                ,side   = 'bottom'
                                )
        self.frm_img = sh.Frame (parent = self.frm_prm
                                ,expand = True
                                ,fill   = 'both'
                                ,side   = 'right'
                                )
        self.frm_btn = sh.Frame (parent = self.parent
                                ,expand = False
                                ,side   = 'bottom'
                                )
        self.frm_btl = sh.Frame (parent = self.frm_btn
                                ,expand = False
                                ,fill   = 'x'
                                ,side   = 'left'
                                )
        self.frm_btr = sh.Frame (parent = self.frm_btn
                                ,expand = False
                                ,fill   = 'x'
                                ,side   = 'right'
                                )
        self.frm_btm = sh.Frame (parent = self.parent
                                ,expand = False
                                ,fill   = 'x'
                                ,side   = 'bottom'
                                )
        self.frmt = sh.Frame (parent = self.frm_btm
                             ,expand = False
                             ,fill   = 'x'
                             ,side   = 'top'
                             )
        self.frmb = sh.Frame (parent = self.frm_btm
                             ,expand = False
                             ,fill   = 'x'
                             ,side   = 'bottom'
                             )
        self.frm1 = sh.Frame (parent = self.frmb
                             ,side   = 'left'
                             ,expand = False
                             ,fill   = 'x'
                             )
        self.frm2 = sh.Frame (parent = self.frmb
                             ,side   = 'right'
                             ,expand = False
                             ,fill   = 'x'
                             )
    
    def values(self):
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
        self._path_add = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_add.gif'
                                           )
        self._path_cyp = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_cypher.gif'
                                           )
        self._path_dec = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_decode.gif'
                                           )
        self._path_dez = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_decypher.gif'
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
    
    def dump(self,event=None):
        return (self.ent_alb.get(),self.ent_art.get()
               ,self.ent_yer.get(),self.opt_gnr.choice
               ,self.ent_cnt.get(),self.ent_com.get()
               )
    
    def title(self,text=None):
        if not text:
            text = _('Album Editor')
        self.parent.title(text=text)

    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon(ICON)

    def show(self,event=None):
        self.parent.show()
        
    def close(self,event=None):
        self.parent.close()



class Menu:
    
    def __init__(self):
        self._a = []
        self.parent = sh.Top (icon  = ICON
                             ,title = 'unmusic'
                             )
        self.gui()
    
    def bindings(self):
        self.parent.widget.protocol("WM_DELETE_WINDOW",self.close)
        sh.com.bind (obj      = self.parent
                    ,bindings = ('<Control-q>','<Control-w>')
                    ,action   = self.close
                    )
        sh.com.bind (obj      = self.parent
                    ,bindings = '<Escape>'
                    ,action   = sh.Geometry(self.parent).minimize
                    )
        if len(self._a) > 0:
            for i in range(len(self._a)):
                sh.com.bind (obj      = self._a[i]
                            ,bindings = '<Home>'
                            ,action   = self._a[0].focus
                            )
                sh.com.bind (obj      = self._a[i]
                            ,bindings = '<End>'
                            ,action   = self._a[-1].focus
                            )
                if i > 0:
                    sh.com.bind (obj      = self._a[i]
                                ,bindings = '<Up>'
                                ,action   = self._a[i-1].focus
                                )
                else:
                    sh.com.bind (obj      = self._a[i]
                                ,bindings = '<Up>'
                                ,action   = self._a[-1].focus
                                )
                if i < len(self._a) - 1:
                    sh.com.bind (obj      = self._a[i]
                                ,bindings = '<Down>'
                                ,action   = self._a[i+1].focus
                                )
                else:
                    sh.com.bind (obj      = self._a[i]
                                ,bindings = '<Down>'
                                ,action   = self._a[0].focus
                                )
    
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon(ICON)
    
    def title(self,text=''):
        if not text:
            text = 'unmusic'
        self.parent.title(text)
    
    def buttons(self):
        font = 'Serif 11'
        self._a.append (sh.Button (parent = self.parent
                                  ,text   = _('Album Editor')
                                  ,side   = 'top'
                                  ,font   = font
                                  )
                       )
        self._a.append (sh.Button (parent = self.parent
                                  ,text   = _('Prepare files')
                                  ,hint   = _('Move sub-folders to a root folder, split large lossless files, etc.')
                                  ,side   = 'top'
                                  ,font   = font
                                  )
                       )
        self._a.append (sh.Button (parent = self.parent
                                  ,text   = _('Collect tags & Obfuscate')
                                  ,side   = 'top'
                                  ,font   = font
                                  )
                       )
        self._a.append (sh.Button (parent = self.parent
                                  ,text   = _('Copy music')
                                  ,side   = 'top'
                                  ,font   = font
                                  )
                       )
        self._a.append (sh.Button (parent = self.parent
                                  ,text   = _('Quit')
                                  ,side   = 'top'
                                  ,font   = font
                                  ,action = self.close
                                  )
                       )
    
    def gui(self):
        self.buttons()
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
        self.pool    = sh.lg.MessagePool(max_size=3)
        self.parent  = sh.Top()
        self.widget  = self.parent.widget
        self._width  = width
        self._height = height
        self.gui()
        
    def clear_rating(self,event=None):
        for track in self._tracks:
            track.opt_rtg.set(0)
    
    def _info(self):
        self.lbl = sh.Label (parent = self.frm_btn
                            ,text   = ''
                            ,font   = 'Sans 9'
                            )

    def update_info(self,text):
        self.pool.add(message=text)
        self.lbl.text(arg=self.pool.get())
    
    def dump(self):
        new = []
        for track in self._tracks:
            new.append(track.dump())
        return new
    
    def values(self):
        self._tracks   = []
        self._path_cyp = sh.objs.pdir().add ('..','resources','buttons'
                                            ,'icon_36x36_cypher.gif'
                                            )
        self._path_dec = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_decode.gif'
                                           )
        self._path_dez = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_decypher.gif'
                                           )
        self._path_rat = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_clear_rating.gif'
                                           )
        self._path_rld = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_reload.gif'
                                           )
        self._path_sav = sh.objs._pdir.add ('..','resources','buttons'
                                           ,'icon_36x36_save.gif'
                                           )
    
    def buttons(self):
        self.btn_rld = sh.Button (parent   = self.frm_btn
                                 ,text     = _('Reload')
                                 ,hint     = _('Reload the present record')
                                 ,side     = 'left'
                                 ,inactive = self._path_rld
                                 ,active   = self._path_rld
                                 ,bindings = ('<F5>','<Control-r>')
                                 )
        self.btn_rat = sh.Button (parent   = self.frm_btn
                                 ,text     = _('Clear rating')
                                 ,hint     = _('Clear rating of all tracks')
                                 ,side     = 'left'
                                 ,inactive = self._path_rat
                                 ,active   = self._path_rat
                                 ,action   = self.clear_rating
                                 )
        self.btn_dez = sh.Button (parent   = self.frm_btn
                                 ,text     = _('Decypher')
                                 ,hint     = _('Decypher text (Caesar algorithm)')
                                 ,side     = 'left'
                                 ,inactive = self._path_dez
                                 ,active   = self._path_dez
                                 )
        self.btn_cyp = sh.Button (parent   = self.frm_btn
                                 ,text     = _('Cypher')
                                 ,hint     = _('Cypher text (Caesar algorithm)')
                                 ,side     = 'left'
                                 ,inactive = self._path_cyp
                                 ,active   = self._path_cyp
                                 )
        self.btn_dec = sh.Button (parent   = self.frm_btn
                                 ,text     = _('Decode')
                                 ,hint     = _('Decode back to cp1251')
                                 ,side     = 'left'
                                 ,inactive = self._path_dec
                                 ,active   = self._path_dec
                                 )
        self.btn_sav = sh.Button (parent   = self.frm_btn
                                 ,text     = _('Save')
                                 ,hint     = _('Save changes')
                                 ,side     = 'right'
                                 ,inactive = self._path_sav
                                 ,active   = self._path_sav
                                 ,bindings = ('<F2>','<Control-s>')
                                 )
    
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon(ICON)
    
    def reset(self):
        for track in self._tracks:
            track.frm_prm.widget.destroy()
        self._tracks = []
    
    def after_add(self):
        sh.objs.root().idle()
        max_x = self.label.reqwidth()
        max_y = self.label.reqheight()
        self.canvas.region (x        = max_x
                           ,y        = max_y
                           ,x_border = 10
                           ,y_border = 20
                           )
        if not self._width:
            self._width = max_x + 40
        sh.Geometry(self.parent).set ('%dx%d' % (self._width
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
        self.frm_prm = sh.Frame (parent = self.parent)
        self.frm_hor = sh.Frame (parent = self.frm_prm
                                ,expand = False
                                ,fill   = 'x'
                                ,side   = 'bottom'
                                )
        self.frm_ver = sh.Frame (parent = self.frm_prm
                                ,expand = False
                                ,fill   = 'y'
                                ,side   = 'right'
                                )
        # This frame must be created after the bottom frame
        self.frm_sec = sh.Frame (parent = self.frm_prm)
        self.frm_btn = sh.Frame (parent = self.frm_prm
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
        self.bindings()
    
    def bindings(self):
        ''' We need a special action for '<Home>' and '<End>' (they are
            useful to navigate within entries), so we use a modified
            version of 'Canvas.top_bindings' here.
        '''
        sh.com.bind (obj      = self.parent
                    ,bindings = '<Down>'
                    ,action   = self.canvas.move_down
                    )
        sh.com.bind (obj      = self.parent
                    ,bindings = '<Up>'
                    ,action   = self.canvas.move_up
                    )
        sh.com.bind (obj      = self.parent
                    ,bindings = '<Left>'
                    ,action   = self.canvas.move_left
                    )
        sh.com.bind (obj      = self.parent
                    ,bindings = '<Right>'
                    ,action   = self.canvas.move_right
                    )
        sh.com.bind (obj      = self.parent
                    ,bindings = '<Next>'
                    ,action   = self.canvas.move_page_down
                    )
        sh.com.bind (obj      = self.parent
                    ,bindings = '<Prior>'
                    ,action   = self.canvas.move_page_up
                    )
        sh.com.bind (obj      = self.parent
                    ,bindings = '<Control-End>'
                    ,action   = self.canvas.move_bottom
                    )
        sh.com.bind (obj      = self.parent
                    ,bindings = '<Control-Home>'
                    ,action   = self.canvas.move_top
                    )
        sh.com.bind (obj      = self.parent
                    ,bindings = ('<MouseWheel>'
                                ,'<Button 4>'
                                ,'<Button 5>'
                                )
                    ,action   = self.canvas.mouse_wheel
                    )
    
    def widgets(self):
        self.canvas = sh.Canvas(parent = self.frm_sec)
        self.label  = sh.Label (parent = self.frm_sec
                               ,text   = _('Tracks:')
                               ,expand = True
                               ,fill   = 'both'
                               )
        self.canvas.embed(self.label)
        self.yscroll = sh.Scrollbar (parent = self.frm_ver
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
        return (self.ent_tit.get(),self.ent_lyr.get(),self.ent_com.get()
               ,int(self.opt_rtg.choice)
               )
    
    # Useful for debug purposes only
    def show(self,event=None):
        self.parent.show()
    
    def frames(self):
        self.frm_prm = sh.Frame (parent = self.parent
                                ,expand = False
                                ,fill   = 'x'
                                )
        self.frm_lft = sh.Frame (parent = self.frm_prm
                                ,side   = 'left'
                                )
        self.frm_rht = sh.Frame (parent = self.frm_prm
                                ,side   = 'left'
                                )
    
    def labels(self):
        if self.Extended:
            sh.Label (parent = self.frm_lft
                     ,text   = _('Album ID:')
                     ,ipady  = 2
                     )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Track #:')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Title:')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Lyrics:')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Comment:')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Bitrate:')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Length:')
                 ,ipady  = 2
                 )
        sh.Label (parent = self.frm_lft
                 ,text   = _('Rating:')
                 ,ipady  = 2
                 )
    
    def entries(self):
        if self.Extended:
            self.ent_aid = sh.Entry (parent = self.frm_rht
                                    ,expand = True
                                    ,fill   = 'x'
                                    ,ipady  = 1
                                    )
        self.ent_tno = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,fill   = 'x'
                                ,ipady  = 1
                                )
        self.ent_tit = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,fill   = 'x'
                                ,ipady  = 1
                                )
        self.ent_lyr = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,fill   = 'x'
                                ,ipady  = 1
                                )
        self.ent_com = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,fill   = 'x'
                                ,ipady  = 1
                                )
        self.ent_bit = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,fill   = 'x'
                                ,ipady  = 1
                                )
        self.ent_len = sh.Entry (parent = self.frm_rht
                                ,expand = True
                                ,fill   = 'x'
                                ,ipady  = 1
                                )
    
    def menus(self):
        self.opt_rtg = sh.OptionMenu (parent = self.frm_rht
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
        self._tracks = self._wait = self._progress = None
    
    def progress(self):
        if self._progress is None:
            self._progress = sh.ProgressBar (height  = 100
                                            ,YScroll = False
                                            )
            self._progress.title(_('Copy progress'))
            self._progress.icon(ICON)
            # Widget is not created yet, do not 'center' it here!
        return self._progress
    
    def tracks(self):
        if self._tracks is None:
            self._tracks = Tracks()
        return self._tracks
    
    def wait(self):
        if self._wait is None:
            self._wait = sh.WaitBox(icon=ICON)
        return self._wait



objs = Objects()



if __name__ == '__main__':
    sh.com.start()
    AlbumEditor().show()
    #Copy().show()
    #Tracks().show()
    sh.com.end()
