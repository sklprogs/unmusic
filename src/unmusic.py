#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import time

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh
#import skl_shared.image.controller as im

import logic as lg
import gui.albums as ga
import gui.tracks as gt


class AlbumEditor:
    
    def __init__(self):
        self.Success = True
        self.gui = ga.AlbumEditor()
        self.set_bindings()
    
    def reset(self):
        self.Success = self.logic.Success = lg.objs.get_db().Success
        self.fill()
    
    def update_album_search(self):
        f = '[unmusic] unmusic.AlbumEditor.update_album_search'
        if not self.Success:
            sh.com.cancel(f)
            return
        pattern = self.gui.ent_src.get()
        self.gui.btn_spr.inactivate()
        self.gui.btn_snx.inactivate()
        if not pattern:
            return
        albumid = lg.objs.db.get_next_album(pattern)
        if albumid:
            self.gui.btn_snx.activate()
        albumid = lg.objs.db.get_prev_album(pattern)
        if albumid:
            self.gui.btn_spr.activate()
    
    def update_meter(self):
        f = '[unmusic] unmusic.AlbumEditor.update_meter'
        if not self.Success:
            sh.com.cancel(f)
            return
        max_ = self.logic.get_max()
        self.gui.lbl_mtr.set_text(f'{self.logic.check_no()} / {max_}')
        if lg.objs.get_db().albumid < max_:
            self.gui.btn_nxt.activate()
        else:
            self.gui.btn_nxt.inactivate()
        if lg.objs.db.albumid == self.logic.get_min():
            self.gui.btn_prv.inactivate()
        else:
            self.gui.btn_prv.activate()
    
    def update(self):
        f = '[unmusic] unmusic.AlbumEditor.update'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.update_meter()
        self.update_album_search()
        self.update_presence()
        self.set_ui_rating()
    
    def fill(self):
        f = '[unmusic] unmusic.AlbumEditor.fill'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.logic.check_no()
        data = lg.objs.get_db().get_album()
        if not data:
            sh.com.rep_empty(f)
            return
        #NOTE: Change this value upon a change in the number of ALBUMS fields
        if len(data) != 7:
            mes = _('Wrong input data: "{}"!').format(data)
            sh.objs.get_mes(f, mes).show_error()
            return
        mes = _('Load #{}.').format(lg.objs.db.albumid)
        self.gui.update_info(mes)
        self.gui.clear_entries()
        self.gui.ent_alb.insert(data[0])
        self.gui.ent_art.insert(data[1])
        self.gui.ent_yer.insert(data[2])
        genre = data[3]
        self.set_genre(genre)
        self.gui.ent_cnt.insert(data[4])
        self.gui.ent_com.insert(data[5])
        self.set_ui_rating()
        self.get_bitrate()
        self.get_length()
        self.set_image()
        self.update()
        if objs.get_tracks().Active:
            objs.tracks.reload()
    
    def delete_tracks(self):
        f = '[unmusic] unmusic.AlbumEditor.delete_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        print(f)
    
    def go_prev_unrated(self):
        f = '[unmusic] unmusic.AlbumEditor.go_prev_unrated'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.save()
        self.logic.set_prev_unrated()
        self.fill()
    
    def go_next_unrated(self):
        f = '[unmusic] unmusic.AlbumEditor.go_next_unrated'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.save()
        self.logic.set_next_unrated()
        self.fill()
    
    def update_presence(self):
        f = '[unmusic] unmusic.AlbumEditor.update_presence'
        if not self.Success:
            sh.com.cancel(f)
            return
        if lg.objs.get_collection().has_local_album():
            self.gui.cbx_loc.enable()
            self.gui.lbl_loc.enable()
        else:
            self.gui.cbx_loc.disable()
            self.gui.lbl_loc.disable()
        if lg.objs.collection.has_ext_album():
            self.gui.cbx_ext.enable()
            self.gui.lbl_ext.enable()
        else:
            self.gui.cbx_ext.disable()
            self.gui.lbl_ext.disable()
        if lg.objs.collection.has_mob_album():
            self.gui.cbx_mob.enable()
            self.gui.lbl_mob.enable()
        else:
            self.gui.cbx_mob.disable()
            self.gui.lbl_mob.disable()
    
    def set_genre(self, genre):
        f = '[unmusic] unmusic.AlbumEditor.set_genre'
        if not self.Success:
            sh.com.cancel(f)
            return
        genre = str(genre)
        if not genre:
            # Do not localize (being stored in DB)
            genre = '?'
        items = list(lg.GENRES)
        if not genre in items:
            items.append(genre)
        self.gui.opt_gnr.reset (items = items
                               ,default = genre
                               )
    
    def go_end(self):
        f = '[unmusic] unmusic.AlbumEditor.go_end'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' #NOTE: If we change 'albumid' BEFORE saving, then a wrong DB record
            will be overwritten!
        '''
        self.save()
        albumid = lg.objs.get_db().get_max_id()
        if not albumid:
            sh.com.rep_empty(f)
            return
        lg.objs.db.albumid = albumid
        self.fill()
    
    def go_start(self):
        f = '[unmusic] unmusic.AlbumEditor.go_start'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' #NOTE: If we change 'albumid' BEFORE saving, then a wrong DB record
            will be overwritten!
        '''
        self.save()
        albumid = lg.objs.get_db().get_min_id()
        if not albumid:
            sh.com.rep_empty(f)
            return
        lg.objs.db.albumid = albumid
        self.fill()
    
    def search_id(self):
        f = '[unmusic] unmusic.AlbumEditor.search_id'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' #NOTE: If we change 'albumid' BEFORE saving, then a wrong DB record
            will be overwritten!
        '''
        self.save()
        albumid = self.gui.ent_ids.get()
        if not albumid:
            sh.com.rep_lazy(f)
            return
        if not str(albumid).isdigit():
            mes = _('Wrong input data: "{}"!')
            mes = mes.format(albumid)
            sh.objs.get_mes(f, mes).show_warning()
            return
        albumid = int(albumid)
        if albumid <= 0:
            mes = _('Wrong input data: "{}"!')
            mes = mes.format(albumid)
            sh.objs.get_mes(f, mes).show_warning()
            return
        data = lg.objs.get_db().has_id(albumid)
        if not data:
            mes = _('No matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        lg.objs.db.albumid = albumid
        self.fill()
    
    def decode(self):
        f = '[unmusic] unmusic.AlbumEditor.decode'
        if not self.Success:
            sh.com.cancel(f)
            return
        artist = self.gui.ent_art.get()
        album = self.gui.ent_alb.get()
        comment = self.gui.ent_com.get()
        artist = lg.com.decode_back(artist)
        album = lg.com.decode_back(album)
        comment = lg.com.decode_back(comment)
        self.gui.ent_art.clear_text()
        self.gui.ent_art.insert(artist)
        self.gui.ent_alb.clear_text()
        self.gui.ent_alb.insert(album)
        self.gui.ent_com.clear_text()
        self.gui.ent_com.insert(comment)
        
    def zoom_image(self):
        f = '[unmusic] unmusic.AlbumEditor.zoom_image'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.image:
            # This should not happen
            sh.com.rep_empty(f)
            return
        viewer = gi.ImageViewer()
        viewer.lbl.widget.config(image=self.image)
        viewer.lbl.widget.image = self.image
        viewer.show()
    
    def set_image(self):
        f = '[unmusic] unmusic.AlbumEditor.set_image'
        if not self.Success:
            sh.com.cancel(f)
            return
        path = objs.get_image().run()
        if not path:
            sh.com.rep_empty(f)
            return
        try:
            iimage = im.Image()
            iimage.open(path)
            # Get a large image
            self.image = iimage.get_image()
            ''' These are dimensions of 'self.gui.frm_img' when
                the default image is loaded.
            '''
            iimage.get_thumbnail(130,212)
            thumb = iimage.get_image()
        except Exception as e:
            ''' Do not fail 'Success' here - it can just be
                an incorrectly ripped image.
            '''
            thumb = None
            mes = _('Third-party module has failed!\n\nDetails: {}')
            mes = mes.format(e)
            sh.objs.get_mes(f, mes).show_warning()
        if not thumb:
            sh.com.rep_empty(f)
            return
        self.gui.lbl_img.widget.config(image=thumb)
        # Prevent the garbage collector from deleting the image
        self.gui.lbl_img.widget.image = thumb
    
    def play(self):
        f = '[unmusic] unmusic.AlbumEditor.play'
        if not self.Success:
            sh.com.cancel(f)
            return
        choice = self.gui.opt_ply.choice
        default = _('Play')
        if choice == default:
            sh.com.rep_lazy(f)
        elif choice == _('All'):
            self.gui.opt_ply.set(default)
            lg.Play().play_all_tracks()
        elif choice == _('Good'):
            self.gui.opt_ply.set(default)
            lg.Play().play_good_tracks()
        elif choice == _('Best'):
            self.gui.opt_ply.set(default)
            lg.Play().play_good_tracks(9)
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(choice,';'.join(gi.PLAY))
            sh.objs.get_mes(f, mes).show_error()
    
    def get_length(self):
        f = '[unmusic] unmusic.AlbumEditor.get_length'
        if not self.Success:
            sh.com.cancel(f)
            return
        total = lg.objs.get_db().get_length()
        if total:
            mes = _('{} ({} tracks)')
            mes = mes.format(sh.lg.com.get_human_time(sum(total)), len(total))
        else:
            mes = '?'
        self.gui.ent_len.enable()
        self.gui.ent_len.clear_text()
        self.gui.ent_len.insert(mes)
        self.gui.ent_len.disable()
    
    def get_bitrate(self):
        f = '[unmusic] unmusic.AlbumEditor.get_bitrate'
        if not self.Success:
            sh.com.cancel(f)
            return
        mean = self.logic.get_mean_bitrate()
        if mean:
            mes = '%dk' % (mean // 1000)
        else:
            mes = '?'
        self.gui.ent_bit.enable()
        self.gui.ent_bit.clear_text()
        self.gui.ent_bit.insert(mes)
        self.gui.ent_bit.disable()
    
    def set_ui_rating(self):
        f = '[unmusic] unmusic.AlbumEditor.set_ui_rating'
        if not self.Success:
            sh.com.cancel(f)
            return
        rating = lg.objs.get_db().get_rating()
        if rating is None:
            sh.com.rep_empty(f)
            return
        if int(rating) == rating:
            ''' Make GUI look better (without ',0' at the end). SQLite
                automatically converts 'int' to 'float'.
            '''
            rating = int(rating)
        ''' We call GUI directly here since shared checks for fixed values, and
            we want float here.
        '''
        self.gui.opt_rtg.gui.set(rating)
        ''' This is because we override the shared method. An actual value of
            the widget is not changed without this.
        ''' 
        self.gui.opt_rtg.choice = rating
    
    def update_rating(self):
        f = '[unmusic] unmusic.AlbumEditor.update_rating'
        if not self.Success:
            sh.com.cancel(f)
            return
        old = lg.objs.get_db().get_rating()
        new = self.logic.get_mean_rating()
        if old is None or new is None:
            sh.com.rep_empty(f)
            return
        if old == new:
            sh.com.rep_lazy(f)
            return
        lg.objs.db.set_album_rating(new)
        self.set_ui_rating()
    
    def set_rating(self):
        f = '[unmusic] unmusic.AlbumEditor.set_rating'
        if not self.Success:
            sh.com.cancel(f)
            return
        rating = self.logic.get_mean_rating()
        if rating is None:
            sh.com.rep_empty(f)
            return
        if not isinstance(rating, float):
            mes = _('Wrong input data: "{}"!').format(rating)
            sh.objs.get_mes(f, mes).show_error()
            return
        mes = _('Tracks are of a mixed rating. Do you want to assign the same rating to all of them?')
        ui_value = float(self.gui.opt_rtg.choice)
        if rating == ui_value:
            ''' Album rating is set to 0 in UI if any track rating is 0 (not
                rated); thus, we should keep track ratings if 0 is selected in
                UI as an album rating.
            '''
            sh.com.rep_lazy(f)
            return
        if rating == int(rating) or sh.objs.get_mes(f, mes).show_question():
            lg.objs.get_db().set_rating(ui_value)
        else:
            self.set_ui_rating()
    
    def dump(self):
        f = '[unmusic] unmusic.AlbumEditor.dump'
        if not self.Success:
            sh.com.cancel(f)
            return
        old = lg.objs.get_db().get_album()
        if not old:
            sh.com.rep_empty(f)
            return
        new = self.gui.dump()
        if len(old) != len(new):
            sub = f'{len(old)} == {len(new)}'
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f, mes).show_error()
            return
        old = list(old)
        new = list(new)
        if not [item for item in new if item]:
            sh.com.rep_empty(f)
            return
        if not new[0]:
            mes = _('An album title should be indicated.')
            sh.objs.get_mes(f, mes).show_warning()
            if old[0]:
                new[0] = old[0]
            else:
                # Do not localize (being stored in DB)
                new[0] = '?'
        if not new[1]:
            mes = _('An artist should be indicated.')
            sh.objs.get_mes(f, mes).show_warning()
            if old[1]:
                new[1] = old[1]
            else:
                # Do not localize (being stored in DB)
                new[1] = '?'
        # Do not warn if a year is not set
        if new[2]:
            new[2] = sh.lg.Input(f, new[2]).get_integer()
        else:
            # We need to return integer anyway
            new[2] = old[2]
        if old == new:
            mes = _('No changes!')
            sh.objs.get_mes(f, mes, True).show_info()
            return
        mes = _('Some fields have been updated.')
        sh.objs.get_mes(f, mes, True).show_info()
        query = self.logic._compare_albums(old, new)
        lg.objs.db.updateDB(query)
        return query
    
    def search_track(self):
        f = '[unmusic] unmusic.AlbumEditor.search_track'
        if not self.Success:
            sh.com.cancel(f)
            return
        pattern = self.gui.ent_sr2.get()
        if not pattern:
            sh.com.rep_lazy(f)
            return
        data = lg.objs.get_db().search_track(pattern)
        if not data:
            mes = _('No matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        objs.get_tracks().fill_search(data=data)
        objs.tracks.show()
    
    def search_album(self):
        f = '[unmusic] unmusic.AlbumEditor.search_album'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.save()
        old = lg.objs.get_db().albumid
        # Not 1, because we use '<' and '>' in search
        lg.objs.db.albumid = 0
        self.search_next_album(Save=False)
        if lg.objs.db.albumid == 0:
            lg.objs.db.albumid = old
    
    def search_next_album(self, Save=True):
        f = '[unmusic] unmusic.AlbumEditor.search_next_album'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' #NOTE: If we change 'albumid' BEFORE saving, then a wrong DB record
            will be overwritten! Since 'self.search_album' is generally
            a wrapper over this procedure and changes 'albumid', we should be
            careful about this.
        '''
        if Save:
            self.save()
        pattern = self.gui.ent_src.get()
        if not pattern:
            self.gui.btn_spr.inactivate()
            self.gui.btn_snx.inactivate()
            sh.com.rep_lazy(f)
            return
        old = lg.objs.get_db().albumid
        albumid = lg.objs.db.get_next_album(pattern)
        if not albumid:
            lg.objs.db.albumid = old
            mes = _('No matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        lg.objs.db.albumid = albumid
        self.fill()
    
    def search_prev_album(self):
        f = '[unmusic] unmusic.AlbumEditor.search_prev_album'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' #NOTE: Make sure that actual 'albumid' is not changed prior to
            'self.search_prev_album'.
        '''
        self.save()
        pattern = self.gui.ent_src.get()
        if not pattern:
            self.gui.btn_spr.inactivate()
            self.gui.btn_snx.inactivate()
            sh.com.rep_lazy(f)
            return
        old = lg.objs.get_db().albumid
        albumid = lg.objs.db.get_prev_album(pattern)
        if not albumid:
            lg.objs.db.albumid = old
            mes = _('No matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        lg.objs.db.albumid = albumid
        self.fill()
    
    def go_prev(self):
        f = '[unmusic] unmusic.AlbumEditor.go_prev'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.save()
        self.logic.dec()
        self.fill()
    
    def go_next(self):
        f = '[unmusic] unmusic.AlbumEditor.go_next'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.save()
        self.logic.inc()
        self.fill()
    
    def show_tracks(self):
        f = '[unmusic] unmusic.AlbumEditor.show_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        objs.get_tracks().fill()
        if objs.tracks.gui.tracks:
            objs.tracks.show()
    
    def delete(self):
        f = '[unmusic] unmusic.AlbumEditor.delete'
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = _('Are you sure you want to permanently delete record #{}?')
        mes = mes.format(lg.objs.get_db().albumid)
        if not sh.objs.get_mes(f, mes).show_question():
            return
        mes = _('Delete #{}.').format(lg.objs.db.albumid)
        self.gui.update_info(text=mes)
        lg.objs.db.delete()
        lg.objs.db.albumid = self.logic.get_max()
        self.fill()
    
    def save(self):
        ''' #NOTE: this should be done before 'albumid' is changed, otherwise,
            a wrong DB record will be overwritten!
        '''
        f = '[unmusic] unmusic.AlbumEditor.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.dump():
            self.gui.update_info(_('Save DB.'))
            lg.objs.get_db().save()
    
    def set_bindings(self):
        self.gui.bind(('Ctrl+Q',), self.close)
        self.gui.bind(('Esc',), self.minimize)
        #self.gui.widget.protocol('WM_DELETE_WINDOW', self.close)
        self.gui.top.btn_nxt.set_action(self.go_next)
        self.gui.top.btn_prv.set_action(self.go_prev)
        self.gui.top.btn_snr.set_action(self.search_next_album)
        self.gui.top.btn_spr.set_action(self.search_prev_album)
        self.gui.top.opt_rtg.set_action(self.set_rating)
        self.gui.top.opt_ply.action.set_action(self.play)
        self.gui.bottom.btn_dec.set_action(self.decode)
        self.gui.bottom.btn_del.set_action(self.delete)
        self.gui.bottom.btn_trs.set_action(self.delete_tracks)
        self.gui.bottom.btn_rld.set_action(self.fill)
        self.gui.bottom.btn_sav.action.set_action(self.save)
        self.gui.bottom.btn_trk.set_action(self.show_tracks)
    
    def show(self):
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.gui.close()



class Tracks:
    
    def __init__(self):
        self.gui = gt.Tracks()
        self.tracks = []
        self.set_bindings()
    
    def decode(self):
        f = '[unmusic] unmusic.Tracks.decode'
        if not self.Success:
            sh.com.cancel(f)
            return
        for track in self.get_gui().tracks:
            title = track.ent_tit.get()
            title = lg.com.decode_back(title)
            track.ent_tit.clear_text()
            track.ent_tit.insert(title)
    
    def _dump_search(self, old, new):
        f = '[unmusic] unmusic.Tracks._dump_search'
        mes = _('Not implemented yet!')
        sh.objs.get_mes(f, mes).show_info()
        return False
    
    def _dump(self, old, new):
        f = '[unmusic] unmusic.Tracks._dump'
        if not old or not new:
            sh.com.rep_empty(f)
            return
        if len(old) != len(new):
            sub = f'{len(old)} = {len(new)}'
            mes = _('Condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f, mes).show_error()
            return
        Dump = False
        for i in range(len(old)):
            if len(old[i]) != 7 or len(new[i]) != 4:
                self.Success = False
                mes = _('Wrong input data!')
                sh.objs.get_mes(f, mes).show_error()
                # We're in loop - do not use 'return'
                continue
            old_record = [old[i][0], old[i][2], old[i][3], old[i][6]]
            new_record = [new[i][0], new[i][1], new[i][2], new[i][3]]
            if old_record != new_record:
                if not new[i][0]:
                    mes = _('A track title should be indicated.')
                    sh.objs.get_mes(f, mes).show_warning()
                    # We're in loop - do not use 'return'
                    continue
                mes = _('Edit #{}.').format(i+1)
                self.get_gui().update_info(mes)
                lg.objs.get_db().update_track (no = i + 1
                                              ,data = new_record
                                              )
                Dump = True
        return Dump
    
    def dump(self):
        f = '[unmusic] unmusic.Tracks.dump'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not lg.objs.get_db().check_nos():
            mes = _('Track numbers should be sequential!')
            sh.objs.get_mes(f, mes).show_warning()
            return
        Extended = False
        if self.get_gui().tracks:
            Extended = self.gui.tracks[0].Extended
        old = lg.objs.db.get_tracks()
        new = self.gui.dump()
        if Extended:
            return self._dump_search(old, new)
        else:
            return self._dump(old, new)
    
    def save(self):
        ''' #NOTE: this should be done before 'albumid' is changed, otherwise,
            a wrong DB record will be overwritten!
        '''
        f = '[unmusic] unmusic.Tracks.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.dump():
            objs.get_editor().update_rating()
            self.get_gui().update_info(_('Save DB.'))
            lg.objs.get_db().save()
    
    def set_bindings(self):
        self.gui.bind(('Ctrl+Q',), self.close)
        self.gui.bind(('Esc',), self.close)
    
    def add(self):
        track = gt.Track()
        self.gui.add(track)
        self.tracks.append(track)
    
    def show(self):
        self.Active = True
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.Active = False
        self.save()
        self.gui.close()
    
    def fill_search(self, data):
        f = '[unmusic] unmusic.Tracks.fill_search'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.get_gui().reset()
        if not data:
            sh.com.rep_empty(f)
            return
        for i in range(len(data)):
            self.gui.add(Extended=True)
            record = data[i]
            track = self.gui.tracks[i]
            if len(record) == 8:
                track.ent_aid.enable()
                track.ent_aid.clear_text()
                track.ent_aid.insert(record[0])
                track.ent_aid.disable()
                track.ent_tno.enable()
                track.ent_tno.clear_text()
                track.ent_tno.insert(str(record[2]))
                track.ent_tno.disable()
                track.ent_tit.clear_text()
                track.ent_tit.insert(record[1])
                track.ent_lyr.clear_text()
                track.ent_lyr.insert(record[3])
                track.ent_com.clear_text()
                track.ent_com.insert(record[4])
                track.ent_bit.enable()
                track.ent_bit.clear_text()
                track.ent_bit.insert(str(record[5] // 1000) + 'k')
                track.ent_bit.disable()
                track.ent_len.enable()
                track.ent_len.clear_text()
                track.ent_len.insert(sh.lg.com.get_human_time(float(record[6])))
                track.ent_len.disable()
                track.opt_rtg.set(record[7])
            else:
                self.Success = False
                mes = _('Wrong input data: "{}"!').format(data)
                sh.objs.get_mes(f, mes).show_error()
        self.gui.adjust_by_content()
    
    def reload(self):
        self.fill()
        self.show()
    
    def fill(self):
        f = '[unmusic] unmusic.Tracks.fill'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.get_gui().reset()
        data = lg.objs.get_db().get_tracks()
        if not data:
            mes = _('No tracks are associated with this album.')
            sh.objs.get_mes(f, mes).show_info()
            return
        for i in range(len(data)):
            self.gui.add()
            mes = _('Load #{}.').format(i+1)
            self.gui.update_info(mes)
            record = data[i]
            track = self.gui.tracks[i]
            if len(record) == 7:
                track.ent_tno.enable()
                track.ent_tno.clear_text()
                track.ent_tno.insert(str(record[1]))
                track.ent_tno.disable()
                track.ent_tit.clear_text()
                track.ent_tit.insert(record[0])
                track.ent_lyr.clear_text()
                track.ent_lyr.insert(record[2])
                track.ent_com.clear_text()
                track.ent_com.insert(record[3])
                track.ent_bit.enable()
                track.ent_bit.clear_text()
                track.ent_bit.insert(str(record[4] // 1000) + 'k')
                track.ent_bit.disable()
                track.ent_len.enable()
                track.ent_len.clear_text()
                track.ent_len.insert(sh.lg.com.get_human_time(float(record[5])))
                track.ent_len.disable()
                track.opt_rtg.set(record[6])
            else:
                self.Success = False
                mes = _('Wrong input data: "{}"!').format(data)
                sh.objs.get_mes(f, mes).show_error()
        self.gui.adjust_by_content()



class Copy:
    
    def __init__(self):
        self.set_values()
        self.gui = gi.Copy()
        self.set_bindings()
    
    def wait_carrier(self,carrier):
        f = '[unmusic] unmusic.Copy.wait_carrier'
        if not self.Success:
            sh.com.cancel()
            return
        if not carrier:
            sh.com.rep_empty(f)
            return
        carrier = os.path.realpath(carrier)
        carrier_sh = sh.lg.Text(carrier).shorten (max_len = 25
                                                 ,encloser = '"'
                                                 ,FromEnd = True
                                                 )
        mes = _('Waiting for {}').format(carrier_sh)
        objs.get_waitbox().reset (func = f
                                 ,message = mes
                                 )
        objs.waitbox.show()
        while not os.path.isdir(carrier):
            time.sleep(1)
        objs.waitbox.close()
    
    def get_settings(self):
        f = '[unmusic] unmusic.Copy.get_settings'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.genre = self.gui.opt_gnr.choice
        if self.gui.opt_yer.choice == _('Not set'):
            pass
        elif self.gui.opt_yer.choice == '=':
            self.year = sh.lg.Input (title = f
                                    ,value = self.gui.ent_yer.get()
                                    ).get_integer()
        elif self.gui.opt_yer.choice == '>=':
            self.syear = sh.lg.Input (title = f
                                      ,value = self.gui.ent_yer.get()
                                      ).get_integer()
        elif self.gui.opt_yer.choice == '<=':
            self.eyear = sh.lg.Input (title = f
                                      ,value = self.gui.ent_yer.get()
                                      ).get_integer()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format (self.gui.opt_yer.choice
                             ,'; '.join(gi.ITEMS_YEAR)
                             )
            sh.objs.get_mes(f, mes).show_error()
        self.source = lg.objs.get_default().ihome.add_share(self.gui.opt_src.choice)
        self.target = lg.objs.default.ihome.add_share(self.gui.opt_trg.choice)
        self.limit = sh.lg.Input (title = f
                                 ,value = self.gui.ent_lim.get()
                                 ).get_integer()
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()
    
    def set_bindings(self):
        self.gui.btn_str.action = self.start
    
    def set_values(self):
        self.ids = []
        self.sizes = []
        self.dirs = []
        self.query = ''
        self.source = ''
        self.target = ''
        self.genre = _('All')
        self.limit = 100
        self.year = 0
        self.syear = 0
        self.eyear = 0
        # At least 30 MiB should remain free on the target device
        self.minfr = 31457280
        self.Success = lg.objs.get_db().Success
    
    def confirm(self):
        f = '[unmusic] unmusic.Copy.copy'
        if not self.Success:
            sh.com.cancel(f)
            return
        total = sum(self.sizes)
        free = sh.lg.Path(self.target).get_free_space()
        cond = total and free and total + self.minfr < free
        if cond:
            free = sh.lg.com.get_human_size (bsize = free
                                            ,LargeOnly = True
                                            )
            total = sh.lg.com.get_human_size(total,LargeOnly=1)
            message = _('Selected albums: {}').format(len(self.ids))
            message += '\n'
            message += _('Total size: {}').format(total)
            message += '\n'
            message += _('Free space: {}').format(free)
            message += '\n\n'
            message += _('Continue?')
            return sh.objs.get_mes(f,message).show_question()
        elif not total:
            # Do not fail here since we may change settings after
            sh.com.rep_lazy(f)
        else:
            free = sh.lg.com.get_human_size (bsize = free
                                            ,LargeOnly = True
                                            )
            bsize = total + self.minfr
            required = sh.lg.com.get_human_size (bsize = bsize
                                                ,LargeOnly = True
                                                )
            message = _('Not enough free space on "{}"!')
            message = message.format(self.target)
            message += '\n'
            message += _('Free space: {}').format(free)
            message += '\n'
            message += _('Required: {}').format(required)
            sh.objs.get_mes(f,message).show_warning()
    
    def copy(self):
        f = '[unmusic] unmusic.Copy.copy'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.confirm():
            mes = _('Operation has been canceled by the user.')
            sh.objs.get_mes(f, mes, True).show_info()
            return
        gi.objs.progress.show()
        for i in range(len(self.ids)):
            myid = str(self.ids[i])
            source = os.path.join(self.source,myid)
            target = os.path.join(self.target,myid)
            source_sh = sh.lg.Text(source).shorten (max_len = 30
                                                   ,FromEnd = True
                                                   )
            target_sh = sh.lg.Text(target).shorten (max_len = 30
                                                   ,FromEnd = True
                                                   )
            message = '({}/{}) {} -> {}'.format (i + 1
                                                ,len(self.ids)
                                                ,source_sh
                                                ,target_sh
                                                )
            gi.objs.progress.set_text(message)
            gi.objs.progress.update(i,len(self.ids))
            idir = sh.lg.Directory (path = source
                                   ,dest = target
                                   )
            idir.copy()
            if not idir.Success:
                self.Success = False
                break
        gi.objs.progress.close()
    
    def get_sizes(self):
        f = '[unmusic] unmusic.Copy.get_sizes'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.sizes = []
        if not self.ids:
            sh.com.rep_lazy(f)
            return
        gi.objs.get_progress().set_text(_('Calculate required space'))
        gi.objs.progress.show()
        for i in range(len(self.ids)):
            gi.objs.progress.update(i,len(self.ids))
            mydir = os.path.join(self.source,str(self.ids[i]))
            idir = sh.lg.Directory(mydir)
            self.Success = idir.Success
            if self.Success:
                self.sizes.append(idir.get_size())
            else:
                sh.com.cancel(f)
                break
        gi.objs.progress.close()
    
    def select_albums(self):
        f = '[unmusic] unmusic.Copy.select_albums'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.ids:
            sh.com.rep_empty(f)
            return
        text = lg.objs.get_db().get_brief(self.ids)
        if not text:
            sh.com.rep_empty(f)
            return
        lst = text.splitlines()
        ibox = sh.MultCBoxesC (text = text
                              ,MarkAll = True
                              ,width = 1024
                              ,height = 768
                              ,icon = gi.ICON
                              )
        ibox.show()
        # Always a list
        selected = ibox.get_selected()
        poses = []
        for item in selected:
            try:
                poses.append(lst.index(item))
            except ValueError:
                self.Success = False
                mes = _('Wrong input data!')
                sh.objs.get_mes(f, mes).show_error()
        ids = []
        for pos in poses:
            try:
                ids.append(self.ids[pos])
            except IndexError:
                mes = _('Wrong input data!')
                sh.objs.get_mes(f, mes).show_error()
        # Allow an empty list here to cancel copying if no albums are selected
        self.ids = ids
    
    def fetch(self):
        f = '[unmusic] unmusic.Copy.fetch'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            if self.genre == _('Light'):
                lst = list(self.ids) + list(lg.LIGHT)
            elif self.genre == _('Heavy'):
                lst = list(self.ids) + list(lg.HEAVY)
            else:
                lst = list(self.ids)
            lg.objs.get_db().dbc.execute(self.query,lst)
            result = lg.objs.db.dbc.fetchall()
            if result:
                self.ids = [item[0] for item in result]
            else:
                sh.com.rep_empty(f)
                self.Success = False
        except Exception as e:
            self.Success = False
            mes = _('Operation has failed!\n\nDetails: {}')
            mes = mes.format(e)
            sh.objs.get_mes(f, mes).show_error()
    
    def set_query(self):
        f = '[unmusic] unmusic.Copy.set_query'
        if not self.Success:
            sh.com.cancel(f)
            return
        ids = lg.objs.get_db().get_rated()
        if not ids:
            sh.com.rep_empty(f)
            return
        self.ids = ids
        # We assume that 'self.ids' are already distinct
        self.query = 'select ALBUMID from ALBUMS where ALBUMID in (%s)' \
                      % ','.join('?'*len(self.ids))
        if self.genre in (_('All'),_('Any')):
            pass
        elif self.genre == _('Light'):
            self.query += ' and GENRE in (%s)' % ','.join('?' * len(lg.LIGHT))
        elif self.genre == _('Heavy'):
            self.query += ' and GENRE in (%s)' % ','.join('?' * len(lg.HEAVY))
        else:
            self.Success = False
            genres = (_('All'), _('Any'), _('Light'), _('Heavy'))
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(self.genre, '; '.join(genres))
            sh.objs.get_mes(f, mes).show_error()
        ''' If an exact year is set then only this year should be used;
            otherwise, a starting-ending years range should be used.
        '''
        if self.year:
            self.query += ' and YEAR = %d' % self.year
        else:
            if self.syear:
                self.query += ' and YEAR >= %d' % self.syear
            if self.eyear:
                self.query += ' and YEAR <= %d' % self.eyear
        self.query += ' order by ALBUMID'
        if self.limit:
            self.query += ' limit %d' % self.limit
    
    def debug(self):
        f = '[unmusic] unmusic.Copy.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.ids:
            sh.com.rep_empty(f)
            return
        '''
        mes = '; '.join([str(albumid) for albumid in self.ids])
        sh.objs.get_mes(f, mes, True).show_debug()
        '''
        ids = lg.objs.get_db().get_brief(self.ids)
        ids = ids.splitlines()
        ids.sort()
        sh.fast_txt('\n'.join(ids))
    
    def start(self):
        # Do not reset GUI here
        self.set_values()
        self.get_settings()
        self.wait_carrier(self.source)
        self.wait_carrier(self.target)
        self.set_query()
        self.fetch()
        self.select_albums()
        self.get_sizes()
        self.copy()



class Menu:
    
    def __init__(self):
        self.gui = gi.Menu()
        self.set_bindings()
    
    def delete_bad(self):
        f = '[unmusic] unmusic.Menu.delete_bad'
        ibad = lg.BadMusic()
        objs.get_waitbox().reset (func = f
                                 ,message = _('Calculate ratings')
                                 )
        objs.waitbox.show()
        data = ibad.get_rates()
        objs.waitbox.close()
        if not data:
            mes = _('Nothing to do!')
            sh.objs.get_mes(f, mes).show_info()
            return
        mes = _('Insert all required media to calculate space to be freed.\n\nContinue?')
        ques = sh.objs.get_mes(f, mes).show_question()
        if not ques:
            mes = _('Operation has been canceled by the user.')
            sh.objs.get_mes(f, mes, True).show_info()
            return
        objs.waitbox.reset (func = f
                           ,message = _('Calculate sizes')
                           )
        objs.waitbox.show()
        ibad.get_sizes()
        objs.waitbox.close()
        ibad.report()
        if not ibad.sizes:
            sh.com.rep_empty(f)
            return
        sizes = [item for item in ibad.sizes if item]
        total_size = 0
        for item in sizes:
            total_size += item
        total_size = sh.com.get_human_size (bsize = total_size
                                           ,LargeOnly = True
                                           )
        affected = ibad.get_affected_carriers()
        if affected:
            affected = ', '.join(affected)
        else:
            affected = _('N/A')
        mes = _('Affected carriers: {}.\nSpace to be freed: {}.\nNumber of albums to delete: {}.\nThe list of directories to be deleted is below. Continue?\n\n{}')
        mes = mes.format (affected, total_size, len(ibad.dellst)
                         ,'\n'.join(ibad.dellst)
                         )
        ques = sh.objs.get_mes(f, mes).show_question()
        if not ques:
            mes = _('Operation has been canceled by the user.')
            sh.objs.get_mes(f, mes, True).show_info()
            return
        objs.waitbox.reset (func = f
                           ,message = _('Delete albums')
                           )
        objs.waitbox.show()
        ibad.delete()
        objs.waitbox.close()
        
    def copy(self):
        objs.get_copy().show()
    
    def album_editor(self):
        objs.get_editor().reset()
        objs.editor.show()
    
    def collect(self):
        ''' If an artist and/or album title were changed and originally
            were not empty, there is no easy way to tell if we are
            dealing with the same album or not. So, it's best to add
            tags to DB only once.
        '''
        f = '[unmusic] unmusic.Menu.collect'
        folder = sh.lg.Home(app_name='unmusic').add_share(_('not processed'))
        if not sh.lg.Path(folder).create():
            sh.com.cancel(f)
            return
        iwalk = lg.Walker(folder)
        dirs = iwalk.get_dirs()
        if not dirs:
            sh.com.rep_empty(f)
            iwalk.delete_empty()
            lg.objs.get_db().save()
            return
        count = 0
        timer = sh.lg.Timer(f)
        timer.start()
        for folder in dirs:
            if not lg.objs.get_db().Success:
                sh.com.cancel(f)
                continue
            count += 1
            basename = sh.lg.Path(folder).get_basename()
            itext = sh.lg.Text(basename)
            itext.delete_unsupported()
            itext.shorten(max_len=15)
            mes = _('Process "{}" ({}/{})')
            mes = mes.format(itext.text, count, len(dirs))
            gi.objs.get_wait().reset (func = f
                                     ,message = mes
                                     )
            gi.objs.wait.show()
            lg.Directory(folder).run()
            ''' In case something went wrong, we should loose only 1 album
                record, not the entire sequence.
            '''
            lg.objs.get_db().save()
        gi.objs.get_wait().close()
        delta = timer.end()
        mes = _('Operation has taken {}')
        mes = mes.format(sh.lg.com.get_human_time(delta))
        sh.objs.get_mes(f, mes).show_info()
        objs.get_editor().reset()
        objs.editor.show()
        iwalk.delete_empty()
        lg.objs.get_db().save()
    
    def prepare(self):
        f = '[unmusic] unmusic.Menu.prepare'
        mes = _('Not implemented yet!')
        sh.objs.get_mes(f, mes).show_info()
    
    def set_bindings(self):
        self.gui.a[0].action = self.album_editor
        self.gui.a[1].action = self.prepare
        self.gui.a[2].action = self.collect
        self.gui.a[3].action = self.copy
        self.gui.a[4].action = self.delete_bad
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()



class Objects(lg.Objects):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editor = self.tracks = self.copy_ = self.waitbox = None
    
    def get_waitbox(self):
        if self.waitbox is None:
            self.waitbox = sh.WaitBox(gi.ICON)
        return self.waitbox
    
    def get_copy(self):
        if self.copy_ is None:
            self.copy_ = Copy()
        return self.copy_
    
    def get_editor(self):
        if self.editor is None:
            self.editor = AlbumEditor()
        return self.editor
    
    def get_tracks(self):
        if self.tracks is None:
            self.tracks = Tracks()
        return self.tracks


objs = Objects()


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    editor = AlbumEditor()
    editor.show()
    sh.com.end()
