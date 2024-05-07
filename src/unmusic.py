#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

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
    
    def set_bindings(self):
        self.gui.bind(('Ctrl+Q',), self.close)
        self.gui.bind(('Esc',), self.close)
    
    def add(self):
        track = gt.Track()
        self.gui.add(track)
        self.tracks.append(track)
    
    def show(self):
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.gui.close()


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    editor = AlbumEditor()
    editor.show()
    sh.com.end()
