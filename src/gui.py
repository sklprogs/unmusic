#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6
import PyQt6.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


#NOTE: Do not localize (being stored in DB)
GENRES = ('?', 'Alternative Rock', 'Ambient', 'Black Metal', 'Blues'
         ,'Brutal Death Metal', 'Chanson', 'Classical', 'Death Metal'
         ,'Death Metal/Grindcore', 'Death/Black Metal'
         ,'Death/Thrash Metal', 'Deathcore', 'Electronic', 'Ethnic', 'Game'
         ,'Goregrind', 'Grindcore', 'Heavy Metal', 'Industrial Metal'
         ,'Melodic Death Metal', 'Metal', 'Pop', 'Power Metal', 'Rap'
         ,'Relaxation', 'Rock', 'Soundtrack', 'Technical Brutal Death Metal'
         ,'Technical Death Metal', 'Thrash Metal', 'Vocal'
         )


class AlbumEditor(PyQt6.QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_values()
        self.set_gui()
    
    def set_values(self):
        self.icn_rld = sh.objs.get_pdir().add ('..', 'resources', 'buttons'
                                              ,'reload.png'
                                              )
        self.icn_del = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'delete_record.png'
                                        )
        self.icn_trs = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'delete_tracks.png'
                                        )
        self.icn_dec = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'decode.png'
                                        )
        self.icn_sav = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'save.png'
                                        )
        self.icn_trk = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'tracks.png'
                                        )

    def set_label_font_size(self):
        self.lbl_art.change_font_size(2)
        self.lbl_alb.change_font_size(2)
        self.lbl_yer.change_font_size(2)
        self.lbl_cnt.change_font_size(2)
        self.lbl_com.change_font_size(2)
        self.lbl_bit.change_font_size(2)
        self.lbl_len.change_font_size(2)
        self.lbl_gnr.change_font_size(2)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def set_layout(self):
        self.parent = PyQt6.QtWidgets.QWidget()
        self.layout_ = PyQt6.QtWidgets.QGridLayout()
        #self.layout_.setContentsMargins(0, 0, 0, 0)
    
    def set_labels(self):
        self.lbl_art = sh.Label(_('Artist:'))
        self.lbl_alb = sh.Label(_('Album:'))
        self.lbl_yer = sh.Label(_('Year:'))
        self.lbl_cnt = sh.Label(_('Country:'))
        self.lbl_com = sh.Label(_('Comment:'))
        self.lbl_bit = sh.Label(_('Average bitrate:'))
        self.lbl_len = sh.Label(_('Total length:'))
        self.lbl_gnr = sh.Label(_('Genre:'))
    
    def set_entries(self):
        self.ent_art = PyQt6.QtWidgets.QLineEdit()
        self.ent_alb = PyQt6.QtWidgets.QLineEdit()
        self.ent_yer = PyQt6.QtWidgets.QLineEdit()
        self.ent_cnt = PyQt6.QtWidgets.QLineEdit()
        self.ent_com = PyQt6.QtWidgets.QLineEdit()
        self.ent_bit = PyQt6.QtWidgets.QLineEdit()
        self.ent_len = PyQt6.QtWidgets.QLineEdit()
    
    def set_options(self):
        self.opt_gnr = sh.OptionMenu(GENRES)
    
    def set_widgets(self):
        self.set_labels()
        self.set_entries()
        self.set_options()
        self.set_collections()
        self.set_bottom()
    
    def configure(self):
        self.set_label_font_size()
    
    def set_gui(self):
        self.set_layout()
        self.set_widgets()
        self.add_widgets()
        self.setCentralWidget(self.parent)
        self.configure()
    
    def add_options(self):
        self.layout_.addWidget(self.opt_gnr.widget, 7, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
    
    def add_labels(self):
        self.layout_.addWidget(self.lbl_art.widget, 0, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_alb.widget, 1, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_yer.widget, 2, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_cnt.widget, 3, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_com.widget, 4, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_bit.widget, 5, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_len.widget, 6, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.lbl_gnr.widget, 7, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
    
    def add_entries(self):
        self.layout_.addWidget(self.ent_art, 0, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_alb, 1, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_yer, 2, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_cnt, 3, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_com, 4, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_bit, 5, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.ent_len, 6, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
    
    def add_panels(self):
        self.layout_.addWidget(self.pnl_col, 8, 1, 1, 2, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.pnl_btm, 9, 0, 1, 20)
    
    def add_collections(self):
        self.lay_col.addWidget(self.cbx_loc.widget)
        self.lay_col.addWidget(self.lbl_loc.widget)
        self.lay_col.addWidget(self.cbx_ext.widget)
        self.lay_col.addWidget(self.lbl_ext.widget)
        self.lay_col.addWidget(self.cbx_mob.widget)
        self.lay_col.addWidget(self.lbl_mob.widget)
    
    def set_bottom(self):
        self.pnl_btm = PyQt6.QtWidgets.QWidget()
        self.lay_btm = PyQt6.QtWidgets.QGridLayout()
        self.btn_rld = sh.Button (hint = _('Reload the present record')
                                 ,inactive = self.icn_rld
                                 ,active = self.icn_rld
                                 )
        self.btn_del = sh.Button (hint = _('Delete the present record')
                                 ,inactive = self.icn_del
                                 ,active = self.icn_del
                                 )
        self.btn_trs = sh.Button (hint = _('Delete tracks with rating < 8')
                                 ,inactive = self.icn_trs
                                 ,active = self.icn_trs
                                 )
        self.lbl_inf = sh.Label(_('Current messages are shown here.'))
        self.btn_dec = sh.Button (hint = _('Decode back to cp1251')
                                 ,inactive = self.icn_dec
                                 ,active = self.icn_dec
                                 )
        self.btn_sav = sh.Button (hint = _('Save changes')
                                 ,inactive = self.icn_sav
                                 ,active = self.icn_sav
                                 )
        self.btn_trk = sh.Button (hint = _('Edit tracks')
                                 ,inactive = self.icn_trk
                                 ,active = self.icn_trk
                                 )
        self.pnl_btm.setLayout(self.lay_btm)
    
    def add_bottom(self):
        self.lay_btm.addWidget(self.btn_rld.widget, 0, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.lay_btm.addWidget(self.btn_del.widget, 0, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.lay_btm.addWidget(self.btn_trs.widget, 0, 2, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.lay_btm.addWidget(self.lbl_inf.widget, 0, 3, 1, 5)
        self.lay_btm.addWidget(self.btn_dec.widget, 0, 4, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignRight)
        self.lay_btm.addWidget(self.btn_sav.widget, 0, 5, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignRight)
        self.lay_btm.addWidget(self.btn_trk.widget, 0, 6, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignRight)
    
    def set_collections(self):
        self.pnl_col = PyQt6.QtWidgets.QWidget()
        self.lay_col = PyQt6.QtWidgets.QHBoxLayout()
        self.cbx_loc = sh.CheckBox()
        self.cbx_ext = sh.CheckBox()
        self.cbx_mob = sh.CheckBox()
        self.lbl_loc = sh.Label(_('local collection'))
        self.lbl_ext = sh.Label(_('external collection'))
        self.lbl_mob = sh.Label(_('mobile collection'))
        self.pnl_col.setLayout(self.lay_col)
    
    def add_widgets(self):
        self.add_labels()
        self.add_entries()
        self.add_options()
        self.add_collections()
        self.add_panels()
        self.add_bottom()
        self.parent.setLayout(self.layout_)


if __name__ == '__main__':
    f = '__main__'
    import sys
    exe = PyQt6.QtWidgets.QApplication(sys.argv)
    app = AlbumEditor()
    app.show()
    sys.exit(exe.exec())
