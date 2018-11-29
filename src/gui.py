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
        self.frame  = sg.Frame (parent = self.parent
                               ,expand = 0
                               ,fill   = 'x'
                               ,side   = 'bottom'
                               )
        self.framet = sg.Frame (parent = self.frame
                               ,expand = 0
                               ,fill   = 'x'
                               ,side   = 'top'
                               )
        self.frameb = sg.Frame (parent = self.frame
                               ,expand = 0
                               ,fill   = 'x'
                               ,side   = 'bottom'
                               )
        self.frame1 = sg.Frame (parent = self.frameb
                               ,side   = 'left'
                               ,expand = 0
                               ,fill   = 'x'
                               )
        self.frame2 = sg.Frame (parent = self.frameb
                               ,side   = 'right'
                               ,expand = 0
                               ,fill   = 'x'
                               )

    def _buttons(self):
        self.btn_trk = sg.Button (parent   = self.frame1
                                 ,text     = _('Tracks')
                                 ,hint     = _('Edit tracks')
                                 ,side     = 'left'
                                 ,inactive = self._path_trk
                                 ,active   = self._path_trk
                                 )
        self.btn_rec = sg.Button (parent   = self.frame1
                                 ,text     = _('Create')
                                 ,hint     = _('Create a new record')
                                 ,side     = 'left'
                                 ,inactive = self._path_add
                                 ,active   = self._path_add
                                 )
        self.btn_sav = sg.Button (parent   = self.frame1
                                 ,text     = _('Save')
                                 ,hint     = _('Save changes')
                                 ,side     = 'left'
                                 ,inactive = self._path_sav
                                 ,active   = self._path_sav
                                 )
        self.btn_rld = sg.Button (parent   = self.frame2
                                 ,text     = _('Reload')
                                 ,hint     = _('Reload the present record')
                                 ,side     = 'left'
                                 ,inactive = self._path_rld
                                 ,active   = self._path_rld
                                 )
        self.btn_del = sg.Button (parent   = self.frame2
                                 ,text     = _('Delete')
                                 ,hint     = _('Delete the present record')
                                 ,side     = 'left'
                                 ,inactive = self._path_del
                                 ,active   = self._path_del
                                 )

    def _info(self):
        # Bind to 'self.framet' to avoid bulking and free space
        self.label = sg.Label (parent = self.frameb
                              ,text   = ''
                              ,font   = 'Sans 9'
                              )

    def update(self,text):
        self.pool.add(message=text)
        self.label.text(arg=self.pool.get())



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

    def gui(self):
        self._gui_frames()
        self._gui_prev()
        self._gui_meter()
        self._gui_next()
        self._gui_search()
        self.bindings()

    def bindings(self):
        sg.bind (obj      = self
                ,bindings = '<F3>'
                ,action   = self.focus_search
                )
        ''' Binding to '<Button-1>' instead of '<ButtonRelease-1>' will
            not allow to select all contents
        '''
        sg.bind (obj      = self.entry_search
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.focus_search
                )

    def _gui_frames(self):
        self.frame = sg.Frame (parent = self.parent
                              ,side   = 'top'
                              ,expand = 0
                              ,fill   = 'x'
                              )
        self.frame1 = sg.Frame (parent = self.frame
                               ,expand = 1
                               ,side   = 'left'
                               )
        self.frame2 = sg.Frame (parent = self.frame
                               ,expand = 1
                               ,side   = 'left'
                               )
        self.widget = self.parent.widget

    def _gui_prev(self):
        self.btn_prev = sg.Button (parent   = self.frame1
                                  ,hint     = _('Go to the preceding record')
                                  ,inactive = self.prev_inactive
                                  ,active   = self.prev_active
                                  ,text     = '←'
                                  ,hint_dir = 'bottom'
                                  ,side     = 'right'
                                  )

    def _gui_next(self):
        self.btn_next = sg.Button (parent   = self.frame2
                                  ,hint     = _('Go to the following record')
                                  ,inactive = self.next_inactive
                                  ,active   = self.next_active
                                  ,text     = '→'
                                  ,hint_dir = 'bottom'
                                  ,side     = 'left'
                                  )

    # Show the current record #/total records ratio
    def _gui_meter(self):
        self.meter = sg.Label (parent = self.frame2
                              ,text   = '0 / 0'
                              ,expand = 0
                              ,side   = 'left'
                              )

    def _gui_search(self):
        frame_search = sg.Frame (parent = self.frame
                                ,side   = 'left'
                                ,expand = 1
                                ,fill   = 'x'
                                )
        sg.Label (parent = frame_search
                 ,text   = _('Search in albums:')
                 ,side   = 'left'
                 )
        self.btn_search_prev = sg.Button (parent   = frame_search
                                         ,hint     = _('Search older records')
                                         ,inactive = self.prev_inactive
                                         ,active   = self.prev_active
                                         ,text     = '←'
                                         ,hint_dir = 'bottom'
                                         ,side     = 'left'
                                         )
        self.entry_search = sg.Entry (parent    = frame_search
                                     ,Composite = 1
                                     ,side      = 'left'
                                     )
        self.btn_search_next = sg.Button (parent   = frame_search
                                         ,hint     = _('Search newer records')
                                         ,inactive = self.next_inactive
                                         ,active   = self.next_active
                                         ,text     = '→'
                                         ,hint_dir = 'bottom'
                                         ,side     = 'left'
                                         )

    def focus_search(self,event=None):
        self.entry_search.focus()
        self.entry_search.select_all()

    def focus_go(self,event=None):
        self.entry_go.focus()
        self.entry_go.select_all()



class AlbumEditor:

    def __init__(self):
        self.obj    = sg.Top(parent=sg.objs.root())
        self.widget = self.obj.widget
        self.icon()
        self.title()
        ''' For some reason, introducing an additional Frame into Top
            does not allow to expand embedded widgets
        '''
        self.top_area = TopArea(parent=self.obj)
        self._frames()
        self.bottom_area = BottomArea(parent=self.obj)
        self.bindings()
        sg.Geometry(parent=self.obj)

    def _frames(self):
        self.cur = Body(parent=self.obj)

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
        self.w_aid.clear_text()
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
        self.main_frame = sg.Frame (parent = self.parent
                                   ,expand = 1
                                   ,fill   = 'both'
                                   ,side   = 'top'
                                   )
        self.frame_left = sg.Frame (parent = self.main_frame
                                   ,expand = 0
                                   ,side   = 'left'
                                   )
        self.frame_right = sg.Frame (parent = self.main_frame
                                    ,expand = 1
                                    ,fill   = 'x'
                                    ,side   = 'right'
                                    ,ipadx  = 150
                                    )
        self.frame_buttons = sg.Frame (parent = self.parent
                                      ,expand = 0
                                      ,fill   = 'x'
                                      ,side   = 'bottom'
                                      )
        self.frame_buttons_left = sg.Frame (parent = self.frame_buttons
                                           ,expand = 0
                                           ,fill   = 'x'
                                           ,side   = 'left'
                                           )
        self.frame_buttons_right = sg.Frame (parent = self.frame_buttons
                                            ,expand = 0
                                            ,fill   = 'x'
                                            ,side   = 'right'
                                            )

    def entries(self):
        self.w_aid = sg.Entry (parent    = self.frame_right
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_art = sg.Entry (parent    = self.frame_right
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_alb = sg.Entry (parent    = self.frame_right
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_yer = sg.Entry (parent    = self.frame_right
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_cnt = sg.Entry (parent    = self.frame_right
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        self.w_com = sg.Entry (parent    = self.frame_right
                              ,Composite = True
                              ,expand    = 1
                              ,fill      = 'x'
                              ,ipady     = 1
                              )
        
    def labels(self):
        sg.Label (parent = self.frame_left
                 ,text   = _('Album ID:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frame_left
                 ,text   = _('Artist:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frame_left
                 ,text   = _('Album:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frame_left
                 ,text   = _('Year:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frame_left
                 ,text   = _('Country:')
                 ,ipady  = 2
                 )
        sg.Label (parent = self.frame_left
                 ,text   = _('Comment:')
                 ,ipady  = 2
                 )


if __name__ == '__main__':
    sg.objs.start()
    editor = AlbumEditor()
    editor.show()
    sg.objs.end()
