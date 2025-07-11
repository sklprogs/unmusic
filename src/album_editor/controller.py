#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import html

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.logic import com as shcom, Input

from config import PATHS, CONFIG
from logic import com, DB, GENRES
from image_viewer.controller import IMAGE_VIEWER, IMAGE
from tracks.controller import TRACKS
from search_tracks.controller import SEARCH_TRACKS
from album_editor import logic
from album_editor import gui


class AlbumEditor:
    
    def __init__(self):
        self.Success = True
        self.image = None
        self.pool = logic.MessagePool(4)
        self.logic = logic.AlbumEditor()
        self.gui = gui.AlbumEditor()
        self.set_bindings()
    
    def focus_id_search(self, event=None):
        if self.gui.top.ent_ids.get() == _('ID'):
            self.gui.top.ent_ids.clear()
        else:
            self.gui.top.ent_ids.select_all()
        self.gui.top.ent_ids.select_all()
        self.gui.top.ent_ids.focus()
        self.gui.top.undecorate_ids()
    
    def focus_album_search(self, event=None):
        if self.gui.top.ent_src.get() == _('Search in albums'):
            self.gui.top.ent_src.clear()
        else:
            self.gui.top.ent_src.select_all()
        self.gui.top.ent_src.focus()
        self.gui.top.undecorate_src()
    
    def focus_track_search(self, event=None):
        if self.gui.top.ent_sr2.get() == _('Search in tracks'):
            self.gui.top.ent_sr2.clear()
        else:
            self.gui.top.ent_sr2.select_all()
        self.gui.top.ent_sr2.focus()
        self.gui.top.undecorate_sr2()
    
    def quit(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.quit'
        self.save()
        com.export_config()
        CONFIG.quit()
        ''' For this code to be executed last, it's not enough to put it in 
            '__main__' right before 'Root.end'.
        '''
        mes = _('Goodbye!')
        Message(f, mes).show_debug()
    
    def update_info(self, text):
        self.pool.add(text)
        self.gui.bottom.lbl_inf.set_text(self.pool.get())
    
    def minimize(self):
        self.gui.minimize()
    
    def reset(self):
        self.Success = self.logic.Success = DB.Success
        self.fill()
    
    def update_album_search(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.update_album_search'
        if not self.Success:
            rep.cancel(f)
            return
        pattern = self.gui.top.ent_src.get()
        self.gui.top.btn_spr.inactivate()
        self.gui.top.btn_snr.inactivate()
        if not pattern:
            return
        albumid = DB.get_next_album(pattern)
        if albumid:
            self.gui.top.btn_snr.activate()
        albumid = DB.get_prev_album(pattern)
        if albumid:
            self.gui.top.btn_spr.activate()
    
    def update_meter(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.update_meter'
        if not self.Success:
            rep.cancel(f)
            return
        max_ = self.logic.get_max()
        self.gui.top.lbl_mtr.set_text(f'{self.logic.check_no()} / {max_}')
        if DB.albumid < max_:
            self.gui.top.btn_nxt.activate()
        else:
            self.gui.top.btn_nxt.inactivate()
        if DB.albumid == self.logic.get_min():
            self.gui.top.btn_prv.inactivate()
        else:
            self.gui.top.btn_prv.activate()
    
    def update(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.update'
        if not self.Success:
            rep.cancel(f)
            return
        self.update_meter()
        self.update_album_search()
        self.update_presence()
        self.set_ui_rating()
    
    def fill(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.fill'
        if not self.Success:
            rep.cancel(f)
            return
        self.logic.check_no()
        data = DB.get_album()
        if not data:
            rep.empty(f)
            return
        #NOTE: Change this value upon a change in the number of ALBUMS fields
        if len(data) != 6:
            mes = _('Wrong input data: "{}"!').format(data)
            Message(f, mes, True).show_error()
            return
        mes = _('Load #{}.').format(DB.albumid)
        self.update_info(mes)
        self.gui.clear_entries()
        self.gui.center.ent_alb.insert(data[0])
        self.gui.center.ent_art.insert(data[1])
        self.gui.center.ent_yer.insert(data[2])
        genre = data[3]
        self.set_genre(genre)
        self.gui.center.ent_cnt.insert(data[4])
        self.gui.center.ent_com.insert(data[5])
        self.set_ui_rating()
        self.get_bitrate()
        self.get_length()
        self.set_image()
        self.update()
        # Refill tracks if the widget is shown
        if TRACKS.Active:
            TRACKS.show()
        if SEARCH_TRACKS.Active:
            SEARCH_TRACKS.show()
    
    def delete_tracks(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.delete_tracks'
        if not self.Success:
            rep.cancel(f)
            return
        logic.DeleteTracks().run()
    
    def go_prev_unrated(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.go_prev_unrated'
        if not self.Success:
            rep.cancel(f)
            return
        self.save()
        self.logic.set_prev_unrated()
        self.fill()
    
    def go_next_unrated(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.go_next_unrated'
        if not self.Success:
            rep.cancel(f)
            return
        self.save()
        self.logic.set_next_unrated()
        self.fill()
    
    def update_presence(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.update_presence'
        if not self.Success:
            rep.cancel(f)
            return
        if logic.COLLECTION.has_local_album():
            self.gui.center.cbx_loc.enable()
        else:
            self.gui.center.cbx_loc.disable()
        if logic.COLLECTION.has_ext_album():
            self.gui.center.cbx_ext.enable()
        else:
            self.gui.center.cbx_ext.disable()
        if logic.COLLECTION.has_mob_album():
            self.gui.center.cbx_mob.enable()
        else:
            self.gui.center.cbx_mob.disable()
    
    def set_genre(self, genre):
        f = '[unmusic] album_editor.controller.AlbumEditor.set_genre'
        if not self.Success:
            rep.cancel(f)
            return
        genre = str(genre)
        if not genre:
            # Do not localize (being stored in DB)
            genre = '?'
        items = list(GENRES)
        if not genre in items:
            items.append(genre)
        self.gui.center.opt_gnr.reset(items, genre)
    
    def go_end(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.go_end'
        if not self.Success:
            rep.cancel(f)
            return
        ''' #NOTE: If we change 'albumid' BEFORE saving, then a wrong DB record
            will be overwritten!
        '''
        self.save()
        albumid = DB.get_max_id()
        if not albumid:
            rep.empty(f)
            return
        DB.albumid = albumid
        self.fill()
    
    def go_start(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.go_start'
        if not self.Success:
            rep.cancel(f)
            return
        ''' #NOTE: If we change 'albumid' BEFORE saving, then a wrong DB record
            will be overwritten!
        '''
        self.save()
        albumid = DB.get_min_id()
        if not albumid:
            rep.empty(f)
            return
        DB.albumid = albumid
        self.fill()
    
    def search_id(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.search_id'
        if not self.Success:
            rep.cancel(f)
            return
        ''' #NOTE: If we change 'albumid' BEFORE saving, then a wrong DB record
            will be overwritten!
        '''
        self.save()
        albumid = self.gui.top.ent_ids.get()
        if not albumid:
            rep.lazy(f)
            return
        if not str(albumid).isdigit():
            mes = _('Wrong input data: "{}"!').format(albumid)
            Message(f, mes, True).show_warning()
            return
        albumid = int(albumid)
        if albumid <= 0:
            mes = _('Wrong input data: "{}"!').format(albumid)
            Message(f, mes, True).show_warning()
            return
        data = DB.has_id(albumid)
        if not data:
            mes = _('No matches!')
            Message(f, mes, True).show_info()
            return
        DB.albumid = albumid
        self.fill()
    
    def decode(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.decode'
        if not self.Success:
            rep.cancel(f)
            return
        artist = self.gui.center.ent_art.get()
        album = self.gui.center.ent_alb.get()
        comment = self.gui.center.ent_com.get()
        artist = com.decode_back(artist)
        album = com.decode_back(album)
        comment = com.decode_back(comment)
        self.gui.center.ent_art.clear_text()
        self.gui.center.ent_art.insert(artist)
        self.gui.center.ent_alb.clear_text()
        self.gui.center.ent_alb.insert(album)
        self.gui.center.ent_com.clear_text()
        self.gui.center.ent_com.insert(comment)
        
    def zoom_image(self, event=None):
        f = '[unmusic] album_editor.controller.AlbumEditor.zoom_image'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.image:
            # This should not happen
            rep.empty(f)
            return
        IMAGE_VIEWER.set_image()
        IMAGE_VIEWER.show()
    
    def set_image(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.set_image'
        if not self.Success:
            rep.cancel(f)
            return
        path = IMAGE.run()
        if not path:
            rep.empty(f)
            return
        try:
            self.image = self.gui.center.set_image(path)
        except Exception as e:
            ''' Do not fail 'Success' here - it can be just an incorrectly
                ripped image.
            '''
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            Message(f, mes, True).show_warning()
    
    def play(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.play'
        if not self.Success:
            rep.cancel(f)
            return
        choice = self.gui.top.opt_ply.get()
        default = _('Play')
        if choice == default:
            rep.lazy(f)
        elif choice == _('All'):
            self.gui.top.opt_ply.set(default)
            logic.Play().run()
        elif choice == _('Good'):
            self.gui.top.opt_ply.set(default)
            logic.Play(8).run()
        elif choice == _('Best'):
            self.gui.top.opt_ply.set(default)
            logic.Play(9).run()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(choice, ';'.join(gi.PLAY))
            Message(f, mes, True).show_error()
    
    def get_length(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.get_length'
        if not self.Success:
            rep.cancel(f)
            return
        total = DB.get_length()
        if total:
            mes = _('{} ({} tracks)')
            mes = mes.format(shcom.get_human_time(sum(total)), len(total))
        else:
            mes = '?'
        self.gui.center.ent_len.enable()
        self.gui.center.ent_len.clear()
        self.gui.center.ent_len.insert(mes)
        self.gui.center.ent_len.disable()
    
    def get_bitrate(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.get_bitrate'
        if not self.Success:
            rep.cancel(f)
            return
        mean = self.logic.get_mean_bitrate()
        if mean:
            mes = '%dk' % (mean // 1000)
        else:
            mes = '?'
        self.gui.center.ent_bit.enable()
        self.gui.center.ent_bit.clear()
        self.gui.center.ent_bit.insert(mes)
        self.gui.center.ent_bit.disable()
    
    def set_ui_rating(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.set_ui_rating'
        if not self.Success:
            rep.cancel(f)
            return
        rates = DB.get_rates()
        if not rates:
            rep.empty(f)
            return
        rating = round(sum(rates) / len(rates), 2)
        if int(rating) == rating:
            ''' Make GUI look better (without ',0' at the end). SQLite
                automatically converts 'int' to 'float'.
            '''
            rating = int(rating)
        ''' We call GUI directly here since shared checks for fixed values, and
            we want float here.
        '''
        ratings = list(gui.RATINGS)
        if rating in ratings:
            self.gui.top.opt_rtg.set(rating)
        else:
            ratings.append(rating)
            ratings.sort()
            self.gui.top.opt_rtg.reset(ratings, rating)
    
    def set_rating(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.set_rating'
        if not self.Success:
            rep.cancel(f)
            return
        rating = self.logic.get_mean_rating()
        if rating is None:
            rep.empty(f)
            return
        if not isinstance(rating, float):
            mes = _('Wrong input data: "{}"!').format(rating)
            Message(f, mes, True).show_error()
            return
        mes = _('Tracks are of a mixed rating. Do you want to assign the same rating to all of them?')
        ui_value = float(self.gui.top.opt_rtg.get())
        if rating == ui_value:
            ''' Album rating is set to 0 in UI if any track rating is 0 (not
                rated); thus, we should keep track ratings if 0 is selected in
                UI as an album rating.
            '''
            rep.lazy(f)
            return
        if rating == int(rating) or Message(f, mes, True).show_question():
            DB.set_rating(ui_value)
            ''' To speed up, data on tracks is not saved unless they are shown,
                so we need to save manually here. High-level 'save' commands
                are not suitable here, since they check for modifications,
                and TRACKS.tracks might even be unfilled for now.
            '''
            self.update_info(_('Save DB.'))
            DB.save()
        else:
            self.set_ui_rating()
    
    def dump(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.dump'
        if not self.Success:
            rep.cancel(f)
            return
        old = DB.get_album()
        if not old:
            rep.empty(f)
            return
        new = self.gui.dump()
        if len(old) != len(new):
            sub = f'{len(old)} == {len(new)}'
            mes = _('The condition "{}" is not observed!').format(sub)
            Message(f, mes, True).show_error()
            return
        old = list(old)
        new = list(new)
        if not [item for item in new if item]:
            rep.empty(f)
            return
        if not new[0]:
            mes = _('An album title should be indicated.')
            Message(f, mes, True).show_warning()
            if old[0]:
                new[0] = old[0]
            else:
                # Do not localize (being stored in DB)
                new[0] = '?'
        if not new[1]:
            mes = _('An artist should be indicated.')
            Message(f, mes, True).show_warning()
            if old[1]:
                new[1] = old[1]
            else:
                # Do not localize (being stored in DB)
                new[1] = '?'
        # Do not warn if a year is not set
        if new[2]:
            new[2] = Input(f, new[2]).get_integer()
        else:
            # We need to return integer anyway
            new[2] = old[2]
        if old == new:
            mes = _('No changes!')
            Message(f, mes).show_info()
            return
        mes = _('Some fields have been updated.')
        Message(f, mes).show_info()
        query = self.logic._compare_albums(old, new)
        DB.updateDB(query)
        return query
    
    def search_track(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.search_track'
        if not self.Success:
            rep.cancel(f)
            return
        pattern = self.gui.top.ent_sr2.get()
        if not pattern:
            rep.lazy(f)
            return
        SEARCH_TRACKS.reload(pattern)
    
    def search_album(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.search_album'
        if not self.Success:
            rep.cancel(f)
            return
        self.save()
        old = DB.albumid
        # Not 1, because we use '<' and '>' in search
        DB.albumid = 0
        self.search_next_album(Save=False)
        if DB.albumid == 0:
            DB.albumid = old
    
    def search_next_album(self, Save=True):
        f = '[unmusic] album_editor.controller.AlbumEditor.search_next_album'
        if not self.Success:
            rep.cancel(f)
            return
        ''' #NOTE: If we change 'albumid' BEFORE saving, then a wrong DB record
            will be overwritten! Since 'self.search_album' is generally
            a wrapper over this procedure and changes 'albumid', we should be
            careful about this.
        '''
        if Save:
            self.save()
        pattern = self.gui.top.ent_src.get()
        if not pattern:
            self.gui.top.btn_spr.inactivate()
            self.gui.top.btn_snx.inactivate()
            rep.lazy(f)
            return
        old = DB.albumid
        albumid = DB.get_next_album(pattern)
        if not albumid:
            DB.albumid = old
            mes = _('No matches!')
            Message(f, mes, True).show_info()
            return
        DB.albumid = albumid
        self.fill()
    
    def search_prev_album(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.search_prev_album'
        if not self.Success:
            rep.cancel(f)
            return
        ''' #NOTE: Make sure that actual 'albumid' is not changed prior to
            'self.search_prev_album'.
        '''
        self.save()
        pattern = self.gui.top.ent_src.get()
        if not pattern:
            self.gui.top.btn_spr.inactivate()
            self.gui.top.btn_snx.inactivate()
            rep.lazy(f)
            return
        old = DB.albumid
        albumid = DB.get_prev_album(pattern)
        if not albumid:
            DB.albumid = old
            mes = _('No matches!')
            Message(f, mes, True).show_info()
            return
        DB.albumid = albumid
        self.fill()
    
    def go_prev(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.go_prev'
        if not self.Success:
            rep.cancel(f)
            return
        self.save()
        self.logic.dec()
        self.fill()
    
    def go_next(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.go_next'
        if not self.Success:
            rep.cancel(f)
            return
        self.save()
        self.logic.inc()
        self.fill()
    
    def show_tracks(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.show_tracks'
        if not self.Success:
            rep.cancel(f)
            return
        TRACKS.show()
    
    def delete(self):
        f = '[unmusic] album_editor.controller.AlbumEditor.delete'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Are you sure you want to permanently delete record #{}?')
        mes = mes.format(DB.albumid)
        if not Message(f, mes, True).show_question():
            return
        mes = _('Delete #{}.').format(DB.albumid)
        self.update_info(mes)
        DB.delete()
        DB.albumid = self.logic.get_max()
        self.fill()
    
    def save(self):
        ''' #NOTE: this should be done before 'albumid' is changed, otherwise,
            a wrong DB record will be overwritten!
        '''
        f = '[unmusic] album_editor.controller.AlbumEditor.save'
        if not self.Success:
            rep.cancel(f)
            return
        if self.dump():
            self.update_info(_('Save DB.'))
            DB.save()
        if TRACKS.Active:
            TRACKS.save()
        if SEARCH_TRACKS.Active:
            SEARCH_TRACKS.save()
    
    def _bind_key(self, key, action):
        f = '[unmusic] album_editor.controller.AlbumEditor._bind_key'
        if not key or not action:
            rep.empty(f)
            return
        try:
            self.gui.bind(CONFIG.new['actions'][key]['hotkeys'], action)
            return True
        except KeyError:
            mes = _('Wrong input data: "{}"!').format(key)
            # Failed config fails all keys, so this should be silent
            Message(f, mes).show_warning()
    
    def _bind_hint(self, key, widget):
        f = '[unmusic] album_editor.controller.AlbumEditor._bind_hint'
        if not key or not widget:
            rep.empty(f)
            return
        if not hasattr(widget, 'hint'):
            # Set a hint on a supported widget only such as a button
            return
        hotkeys = hint = None
        try:
            hotkeys = CONFIG.new['actions'][key]['hotkeys']
            hint = CONFIG.new['actions'][key]['hint']
        except KeyError:
            mes = _('Wrong input data: "{}"!').format(key)
            Message(f, mes, True).show_warning()
            return
        if not hotkeys or not hint:
            rep.empty(f)
            return
        hotkeys = ', '.join(hotkeys)
        widget.hint = f'{html.escape(_(hint))}<i><center>{hotkeys}</center></i>'
        widget.set_hint()
    
    def bind_top(self, key, action, widget=None):
        # Bind hotkeys to the window and set up a button with the same action
        f = '[unmusic] album_editor.controller.AlbumEditor.bind_top'
        if not self._bind_key(key, action):
            return
        if not widget:
            return
        widget.set_action(action)
        self._bind_hint(key, widget)
    
    def set_bindings(self):
        # Connect to signals
        self.gui.sig_close.connect(self.close)
        self.gui.sig_close.connect(self.quit)
        self.gui.top.ent_src.widget.sig_focus_out.connect(self.gui.top.decorate_src)
        self.gui.top.ent_ids.widget.sig_focus_out.connect(self.gui.top.decorate_id)
        self.gui.top.ent_sr2.widget.sig_focus_out.connect(self.gui.top.decorate_sr2)
        # Bind widgets
        self.bind_top('go_next', self.go_next, self.gui.top.btn_nxt)
        self.bind_top('go_prev', self.go_prev, self.gui.top.btn_prv)
        self.bind_top('go_next_unrated', self.go_next_unrated)
        self.bind_top('go_prev_unrated', self.go_prev_unrated)
        self.bind_top('go_start', self.go_start)
        self.bind_top('go_end', self.go_end)
        self.bind_top('reload', self.fill, self.gui.bottom.btn_rld)
        self.bind_top('show_tracks', self.show_tracks, self.gui.bottom.btn_trk)
        self.bind_top('focus_album_search', self.focus_album_search)
        self.bind_top('focus_id_search', self.focus_id_search)
        self.bind_top('focus_track_search', self.focus_track_search)
        self.bind_top('delete_tracks', self.delete_tracks, self.gui.bottom.btn_trs)
        self.bind_top('minimize', self.minimize)
        self.gui.top.btn_snr.set_action(self.search_next_album)
        self.gui.top.btn_spr.set_action(self.search_prev_album)
        self.gui.top.opt_rtg.set_action(self.set_rating)
        self.gui.top.opt_ply.set_action(self.play)
        self.gui.bottom.btn_dec.set_action(self.decode)
        self.gui.bottom.btn_del.set_action(self.delete)
        # Hardcode hotkeys
        self.gui.bind(('Ctrl+Q',), self.close)
        # Bind entries
        self.gui.top.ent_ids.widget.mousePressEvent = self.focus_id_search
        self.gui.top.ent_src.widget.mousePressEvent = self.focus_album_search
        self.gui.top.ent_sr2.widget.mousePressEvent = self.focus_track_search
        self.gui.top.ent_ids.widget.returnPressed.connect(self.search_id)
        self.gui.top.ent_src.widget.returnPressed.connect(self.search_album)
        self.gui.top.ent_sr2.widget.returnPressed.connect(self.search_track)
        TRACKS.gui.signal.sig_rating.connect(self.set_ui_rating)
        TRACKS.gui.signal.sig_info.connect(self.update_info)
        # Bind labels
        self.gui.center.lbl_img.set_action(self.zoom_image)
    
    def show(self):
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.gui.close()


ALBUM_EDITOR = AlbumEditor()
