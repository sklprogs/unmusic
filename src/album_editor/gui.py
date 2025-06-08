#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QGridLayout, QLineEdit
from PyQt6.QtGui import QShortcut, QKeySequence, QFont, QPalette, QColor, QPixmap
from PyQt6.QtCore import pyqtSignal, Qt, QSize

from skl_shared.localize import _
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.icon.controller import ICON
from skl_shared.graphics.button.controller import Button
from skl_shared.graphics.entry.controller import Entry
from skl_shared.graphics.label.controller import Label
from skl_shared.graphics.option_menu.controller import OptionMenu
from skl_shared.graphics.checkbox.controller import CheckBox
from skl_shared.paths import PDIR


RATINGS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
PLAY = (_('Play'), _('All'), _('Good'), _('Best'))
#NOTE: Do not localize (being stored in DB)
GENRES = ('?', 'Alternative Rock', 'Ambient', 'Black Metal', 'Blues'
         ,'Brutal Death Metal', 'Chanson', 'Classical', 'Death Metal'
         ,'Death Metal/Grindcore', 'Death/Black Metal'
         ,'Death/Thrash Metal', 'Deathcore', 'Electronic', 'Ethnic', 'Game'
         ,'Goregrind', 'Grindcore', 'Heavy Metal', 'Industrial Metal'
         ,'Melodic Death Metal', 'Metal', 'Pop', 'Power Metal', 'Rap'
         ,'Relaxation', 'Rock', 'Slamming Brutal Death Metal', 'Soundtrack'
         ,'Technical Brutal Death Metal', 'Technical Death Metal'
         ,'Thrash Metal', 'Vocal')


ICON.set(PDIR.add('..', 'resources', 'unmusic.png'))


class SearchField(QLineEdit):
    sig_focus_out = pyqtSignal()
    
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.sig_focus_out.emit()



class Top:
    
    def __init__(self):
        self.set_values()
        self.set_gui()
    
    def set_values(self):
        self.prev_inactive = PDIR.add('..', 'resources', 'buttons'
                                     ,'go_back_off.png')
        self.prev_active = PDIR.add('..', 'resources', 'buttons', 'go_back.png')
        self.next_inactive = PDIR.add('..', 'resources', 'buttons'
                                     ,'go_next_off.png')
        self.next_active = PDIR.add('..', 'resources', 'buttons', 'go_next.png')
        self.font = None
        self.mono = QFont('Mono')
        self.mono.setItalic(True)
        self.gray_palette = QPalette()
        self.gray_palette.setColor(QPalette.ColorRole.Text, QColor('gray'))
        self.black_palette = QPalette()
        self.black_palette.setColor(QPalette.ColorRole.Text, QColor('black'))
    
    def set_layout(self):
        self.pnl_top = QWidget()
        self.lay_top = QHBoxLayout()
        self.lay_top.setContentsMargins(0, 0, 0, 0)
        self.pnl_top.setLayout(self.lay_top)
    
    def set_gui(self):
        self.set_layout()
        self.set_widgets()
        # Overload entries as early as possible
        self.overload_entries()
        self.add_widgets()
        self.configure()
    
    def decorate_src(self):
        # Do not overwrite existing text
        if self.ent_src.get():
            return
        self.ent_src.set_text(_('Search in albums'))
        self.ent_src.widget.setFont(self.mono)
        self.ent_src.widget.setPalette(self.gray_palette)
    
    def decorate_id(self):
        # Do not overwrite existing text
        if self.ent_ids.get():
            return
        self.ent_ids.set_text(_('ID'))
        self.ent_ids.widget.setFont(self.mono)
        self.ent_ids.widget.setPalette(self.gray_palette)
    
    def decorate_sr2(self):
        # Do not overwrite existing text
        if self.ent_sr2.get():
            return
        self.ent_sr2.set_text(_('Search in tracks'))
        self.ent_sr2.widget.setFont(self.mono)
        self.ent_sr2.widget.setPalette(self.gray_palette)
    
    def undecorate_src(self):
        if not self.font:
            return
        self.ent_src.widget.setFont(self.font)
        self.ent_src.widget.setPalette(self.black_palette)
    
    def undecorate_sr2(self):
        if not self.font:
            return
        self.ent_sr2.widget.setFont(self.font)
        self.ent_sr2.widget.setPalette(self.black_palette)
    
    def undecorate_ids(self):
        if not self.font:
            return
        self.ent_ids.widget.setFont(self.font)
        self.ent_ids.widget.setPalette(self.black_palette)
    
    def overload_entries(self):
        self.ent_src.widget = self.ent_src.gui.widget = SearchField()
        self.ent_ids.widget = self.ent_ids.gui.widget = SearchField()
        self.ent_sr2.widget = self.ent_sr2.gui.widget = SearchField()
    
    def configure(self):
        self.font = self.ent_src.widget.font()
        # Set max width
        self.ent_ids.widget.setMaximumWidth(40)
        self.decorate_src()
        self.decorate_id()
        self.decorate_sr2()
    
    def set_widgets(self):
        self.btn_spr = Button(hint = _('Search older records')
                             ,inactive = self.prev_inactive
                             ,active = self.prev_active)
        self.ent_src = Entry()
        self.btn_snr = Button(hint = _('Search newer records')
                             ,inactive = self.next_inactive
                             ,active = self.next_active)
        self.ent_ids = Entry()
        self.btn_prv = Button(hint = _('Go to the preceding record')
                             ,inactive = self.prev_inactive
                             ,active = self.prev_active)
        # Show the current record #/total records ratio
        self.lbl_mtr = Label('0 / 0')
        self.btn_nxt = Button(hint = _('Go to the following record')
                             ,inactive = self.next_inactive
                             ,active = self.next_active)
        self.ent_sr2 = Entry()
        self.opt_rtg = OptionMenu(RATINGS)
        self.opt_ply = OptionMenu(PLAY)
    
    def add_widgets(self):
        self.lay_top.addWidget(self.btn_spr.widget)
        self.lay_top.addWidget(self.ent_src.widget)
        self.lay_top.addWidget(self.btn_snr.widget)
        self.lay_top.addWidget(self.ent_ids.widget)
        self.lay_top.addWidget(self.btn_prv.widget)
        self.lay_top.addWidget(self.lbl_mtr.widget)
        self.lay_top.addWidget(self.btn_nxt.widget)
        self.lay_top.addWidget(self.ent_sr2.widget)
        self.lay_top.addWidget(self.opt_rtg.widget)
        self.lay_top.addWidget(self.opt_ply.widget)



class Center:
    
    def __init__(self):
        self.set_gui()
    
    def set_font_size(self):
        # Labels
        self.lbl_art.change_font_size(2)
        self.lbl_alb.change_font_size(2)
        self.lbl_yer.change_font_size(2)
        self.lbl_cnt.change_font_size(2)
        self.lbl_com.change_font_size(2)
        self.lbl_bit.change_font_size(2)
        self.lbl_len.change_font_size(2)
        self.lbl_gnr.change_font_size(2)
        self.lbl_loc.change_font_size(1)
        self.lbl_ext.change_font_size(1)
        self.lbl_mob.change_font_size(1)
        # Entries
        self.ent_art.change_font_size(2)
        self.ent_alb.change_font_size(2)
        self.ent_yer.change_font_size(2)
        self.ent_cnt.change_font_size(2)
        self.ent_com.change_font_size(2)
        self.ent_bit.change_font_size(2)
        self.ent_len.change_font_size(2)
        # Option menus
        self.opt_gnr.change_font_size(1)
    
    def add_widgets(self):
        self.add_labels()
        self.add_entries()
        self.add_options()
        self.add_collections()
    
    def set_collections(self):
        self.pnl_col = QWidget()
        self.lay_col = QHBoxLayout()
        self.cbx_loc = CheckBox()
        self.cbx_ext = CheckBox()
        self.cbx_mob = CheckBox()
        self.cbx_loc.widget.setEnabled(False)
        self.cbx_ext.widget.setEnabled(False)
        self.cbx_mob.widget.setEnabled(False)
        self.lbl_loc = Label(_('local collection'))
        self.lbl_ext = Label(_('external collection'))
        self.lbl_mob = Label(_('mobile collection'))
        self.lay_col.setContentsMargins(0, 0, 0, 0)
        self.pnl_col.setLayout(self.lay_col)
    
    def add_collections(self):
        self.lay_col.addWidget(self.cbx_loc.widget)
        self.lay_col.addWidget(self.lbl_loc.widget)
        self.lay_col.addWidget(self.cbx_ext.widget)
        self.lay_col.addWidget(self.lbl_ext.widget)
        self.lay_col.addWidget(self.cbx_mob.widget)
        self.lay_col.addWidget(self.lbl_mob.widget)
    
    def add_options(self):
        self.lay_grd.addWidget(self.opt_gnr.widget, 7, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
    
    def add_labels(self):
        self.lay_grd.addWidget(self.lbl_art.widget, 0, 0, 1, 1)
        self.lay_grd.addWidget(self.lbl_alb.widget, 1, 0, 1, 1)
        self.lay_grd.addWidget(self.lbl_yer.widget, 2, 0, 1, 1)
        self.lay_grd.addWidget(self.lbl_cnt.widget, 3, 0, 1, 1)
        self.lay_grd.addWidget(self.lbl_com.widget, 4, 0, 1, 1)
        self.lay_grd.addWidget(self.lbl_bit.widget, 5, 0, 1, 1)
        self.lay_grd.addWidget(self.lbl_len.widget, 6, 0, 1, 1)
        self.lay_grd.addWidget(self.lbl_gnr.widget, 7, 0, 1, 1)
        self.lay_grd.addWidget(self.pnl_col, 8, 1, 1, 1)
        self.lay_img.addWidget(self.lbl_img.widget, Qt.AlignmentFlag.AlignRight)
    
    def add_entries(self):
        self.lay_grd.addWidget(self.ent_art.widget, 0, 1, 1, 1)
        self.lay_grd.addWidget(self.ent_alb.widget, 1, 1, 1, 1)
        self.lay_grd.addWidget(self.ent_yer.widget, 2, 1, 1, 1)
        self.lay_grd.addWidget(self.ent_cnt.widget, 3, 1, 1, 1)
        self.lay_grd.addWidget(self.ent_com.widget, 4, 1, 1, 1)
        self.lay_grd.addWidget(self.ent_bit.widget, 5, 1, 1, 1)
        self.lay_grd.addWidget(self.ent_len.widget, 6, 1, 1, 1)

    def set_layout(self):
        self.pnl_ctr = QWidget()
        self.lay_ctr = QHBoxLayout()
        self.pnl_grd = QWidget()
        self.pnl_img = QWidget()
        self.lay_grd = QGridLayout()
        self.lay_img = QHBoxLayout()
        self.lay_ctr.addWidget(self.pnl_grd)
        self.lay_ctr.addWidget(self.pnl_img)
        self.lay_ctr.setContentsMargins(0, 0, 0, 0)
        self.lay_grd.setContentsMargins(0, 0, 0, 0)
        self.pnl_ctr.setLayout(self.lay_ctr)
        self.pnl_grd.setLayout(self.lay_grd)
        self.pnl_img.setLayout(self.lay_img)
    
    def set_labels(self):
        self.lbl_art = Label(_('Artist:'))
        self.lbl_alb = Label(_('Album:'))
        self.lbl_yer = Label(_('Year:'))
        self.lbl_cnt = Label(_('Country:'))
        self.lbl_com = Label(_('Comment:'))
        self.lbl_bit = Label(_('Average bitrate:'))
        self.lbl_len = Label(_('Total length:'))
        self.lbl_gnr = Label(_('Genre:'))
        self.lbl_img = Label()
    
    def set_entries(self):
        self.ent_art = Entry()
        self.ent_alb = Entry()
        self.ent_yer = Entry()
        self.ent_cnt = Entry()
        self.ent_com = Entry()
        self.ent_bit = Entry()
        self.ent_len = Entry()
    
    def set_options(self):
        self.opt_gnr = OptionMenu(GENRES)
    
    def set_widgets(self):
        self.set_labels()
        self.set_entries()
        self.set_options()
        self.set_collections()
    
    def set_image(self, path):
        image = QPixmap(path)
        image = image.scaled(QSize(150, 150))
        self.lbl_img.widget.setPixmap(image)
        return image
    
    def set_gui(self):
        self.set_layout()
        self.set_widgets()
        self.set_font_size()
        self.add_widgets()



class Bottom(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_values()
        self.set_gui()
    
    def set_values(self):
        self.icn_rld = PDIR.add('..', 'resources', 'buttons', 'reload.png')
        self.icn_del = PDIR.add('..', 'resources', 'buttons'
                               ,'delete_record.png')
        self.icn_trs = PDIR.add('..', 'resources', 'buttons'
                               ,'delete_tracks.png')
        self.icn_dec = PDIR.add('..', 'resources', 'buttons', 'decode.png')
        self.icn_trk = PDIR.add('..', 'resources', 'buttons', 'tracks.png')

    def set_layout(self):
        self.pnl_btm = QWidget()
        self.lay_btm = QHBoxLayout()
        self.lay_btm.setContentsMargins(0, 0, 0, 0)
        self.pnl_btm.setLayout(self.lay_btm)
    
    def set_gui(self):
        self.set_layout()
        self.set_widgets()
        self.add_widgets()
        self.setCentralWidget(self.pnl_btm)
    
    def set_widgets(self):
        self.btn_rld = Button(hint = _('Reload the present record')
                             ,inactive = self.icn_rld
                             ,active = self.icn_rld)
        self.btn_del = Button(hint = _('Delete the present record')
                             ,inactive = self.icn_del
                             ,active = self.icn_del)
        self.btn_trs = Button(hint = _('Delete tracks with rating < 8')
                             ,inactive = self.icn_trs
                             ,active = self.icn_trs)
        self.lbl_inf = Label(_('Current messages are shown here.'))
        self.btn_dec = Button(hint = _('Decode back to cp1251')
                             ,inactive = self.icn_dec
                             ,active = self.icn_dec)
        self.btn_trk = Button(hint = _('Edit tracks')
                             ,inactive = self.icn_trk
                             ,active = self.icn_trk)
        self.pnl_btm.setLayout(self.lay_btm)
    
    def add_widgets(self):
        self.lay_btm.addWidget(self.btn_rld.widget, Qt.AlignmentFlag.AlignLeft)
        self.lay_btm.addWidget(self.btn_del.widget, Qt.AlignmentFlag.AlignLeft)
        self.lay_btm.addWidget(self.btn_trs.widget, Qt.AlignmentFlag.AlignLeft)
        self.lay_btm.addWidget(self.lbl_inf.widget, Qt.AlignmentFlag.AlignCenter)
        self.lay_btm.addWidget(self.btn_dec.widget, Qt.AlignmentFlag.AlignRight)
        self.lay_btm.addWidget(self.btn_trk.widget, Qt.AlignmentFlag.AlignRight)



class AlbumEditor(QMainWindow):

    sig_close = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()

    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)

    def dump(self):
        return (self.center.ent_alb.get(), self.center.ent_art.get()
               ,self.center.ent_yer.get(), self.center.opt_gnr.get()
               ,self.center.ent_cnt.get(), self.center.ent_com.get()
               ,float(self.top.opt_rtg.get()))
    
    def clear_entries(self):
        self.center.ent_art.clear()
        self.center.ent_alb.clear()
        self.center.ent_yer.clear()
        self.center.ent_cnt.clear()
        self.center.ent_com.clear()
        self.center.ent_art.focus()
    
    def minimize(self):
        self.showMinimized()
    
    def centralize(self):
        ''' Do this only after showing the widget; otherwise, it will have
            bogus dimensions of 640×480.
        '''
        self.move(ROOT.get_root().primaryScreen().geometry().center() - self.rect().center())
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
    
    def set_layout(self):
        self.pnl_edt = QWidget()
        self.lay_edt = QVBoxLayout()
        self.lay_edt.setContentsMargins(13, 7, 13, 7)
        self.lay_edt.addWidget(self.top.pnl_top)
        self.lay_edt.addWidget(self.center.pnl_ctr)
        self.lay_edt.addWidget(self.bottom.pnl_btm)
        self.pnl_edt.setLayout(self.lay_edt)
    
    def set_icon(self):
        # Does not accept None
        self.setWindowIcon(ICON.get())
    
    def set_title(self):
        self.setWindowTitle(_('Album Editor'))
    
    def set_gui(self):
        self.top = Top()
        self.center = Center()
        self.bottom = Bottom()
        self.set_layout()
        self.setCentralWidget(self.pnl_edt)
        self.set_icon()
        self.set_title()
