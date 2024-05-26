#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import phrydy

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from config import PATHS
import logic as lg


class Commands:
    
    def decode(self, text):
        try:
            byted = bytes(text, 'iso-8859-1')
            return byted.decode('cp1251')
        except:
            return text
    
    def delete_album_trash(self, album):
        album = album.replace(' (@FLAC)', '').replace(' (@VBR)', '')
        album = album.replace(' (@vbr)', '').replace(', @FLAC', '')
        album = album.replace(',@FLAC', '').replace(', @VBR', '')
        album = album.replace(',@VBR', '').replace(', @vbr', '')
        album = album.replace(',@vbr', '')
        album = re.sub(' \(@\d+\)', '', album)
        album = re.sub(',[\s]{0,1}@\d+\)', '', album)
        return album
    
    def sanitize(self, field):
        field = sh.lg.Text(field).delete_duplicate_spaces()
        field = field.strip()
        field = self.decode(field)
        if not field:
            field = '?'
        return field



class Track:
    
    def __init__(self, file):
        self.set_values()
        self.file = file
        self.Success = sh.lg.File(self.file).Success
        self.load()
        self.set_info()
        self.decode()
    
    def purge(self):
        f = '[unmusic] album_editor.logic.Track.purge'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.audio:
            sh.com.rep_empty(f)
            return
        try:
            self.audio.delete()
            self.audio.images = {}
        except Exception as e:
            self.Success = False
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes).show_warning()
    
    def save(self):
        ''' This is only needed if the file was changed by means of 'phrydy',
            see, for example, 'self.purge'.
        '''
        f = '[unmusic] album_editor.logic.Track.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.audio:
            sh.com.rep_empty(f)
            return
        try:
            self.audio.save()
        except Exception as e:
            self.Success = False
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes).show_warning()
    
    def decode(self):
        # Fix Cyrillic tags
        f = '[unmusic] album_editor.logic.Track.decode'
        if not self.Success:
            sh.com.cancel(f)
            return
        # Other fields should be decoded before writing to DB
        self.title = com.decode(self.title)
        self.lyrics = com.decode(self.lyrics)
    
    def get_track_meta(self):
        f = '[unmusic] album_editor.logic.Track.get_track_meta'
        if not self.Success:
            sh.com.cancel(f)
            return
        search = [self.title,self.lyrics]
        search = ' '.join(search)
        search = sh.lg.Text(search).delete_duplicate_spaces()
        search = search.strip().lower()
        return (self.title, self.no, self.lyrics, search, self.bitrate
               ,self.length
               )
    
    def set_values(self):
        self.Success = True
        self.audio = None
        self.image = None
        self.artist = ''
        self.album = ''
        self.title = ''
        self.lyrics = ''
        self.genre = ''
        self.year = 0
        self.bitrate = 0
        self.length = 0
        self.no = 1
    
    def show_summary(self):
        f = '[unmusic] album_editor.logic.Track.show_summary'
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = _('Artist: {}').format(self.artist)
        mes += '\n'
        mes += _('Album: {}').format(self.album)
        mes += '\n'
        mes += _('Genre: {}').format(self.genre)
        mes += '\n'
        mes += _('Year: {}').format(self.year)
        mes += '\n'
        mes += _('Track #: {}').format(self.no)
        mes += '\n'
        mes += _('Title: {}').format(self.title)
        mes += '\n'
        mes += _('Lyrics: {}').format(self.lyrics)
        if self.length:
            minutes = self.length // 60
            seconds = self.length - minutes * 60
        else:
            minutes = seconds = 0
        mes += _('Length: {} {} {} {}').format (minutes, _('min'), seconds
                                               ,_('sec')
                                               )
        mes +=  '\n'
        sh.objs.get_mes(f, mes).show_info()
    
    def extract_title(self):
        f = '[unmusic] album_editor.logic.Track.extract_title'
        if not self.Success:
            sh.com.cancel(f)
            return
        title = sh.lg.Path(self.file).get_filename()
        if not title:
            return
        result = re.sub('^\d+[\.]{0,1}[\s]{0,1}','',title)
        if not result:
            # If a title is just a digit + an extension.
            return title
        return result
    
    def _set_info(self):
        f = '[unmusic] album_editor.logic.Track._set_info'
        artist = [self.audio.artist, self.audio.albumartist
                 ,self.audio.composer
                 ]
        artist = [item for item in artist if item]
        if artist:
            self.artist = artist[0]
        ''' - Prevents from type mismatch (e.g., 'phrydy' returns 'None'
              in case a year is not set).
            - If an input value is empty then we do not overwrite a default
              value which should be of a correct type. This does not work
              as a separate procedure.
        '''
        if self.audio.album:
            self.album = str(self.audio.album)
        else:
            dirname = sh.lg.Path(self.file).get_dirname()
            dirname = sh.lg.Path(dirname).get_basename()
            self.album = '[[' + dirname + ']]'
        if self.audio.genre:
            self.genre = str(self.audio.genre)
        if self.audio.year:
            self.year = sh.lg.Input (title = f
                                    ,value = self.audio.year
                                    ).get_integer()
        if self.audio.title:
            self.title = str(self.audio.title)
        else:
            extracted = self.extract_title()
            if extracted:
                self.title = extracted
        if self.audio.bitrate:
            self.bitrate = self.audio.bitrate
        if self.audio.length:
            self.length = self.audio.length
        if str(self.audio.track).isdigit():
            self.no = self.audio.track
        if self.audio.lyrics:
            self.lyrics = str(self.audio.lyrics)
        if self.audio.images:
            self.image = self.audio.images[0].data
    
    def set_info(self):
        f = '[unmusic] album_editor.logic.Track.set_info'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.audio:
            sh.com.rep_empty(f)
            return
        try:
            self._set_info()
        except Exception as e:
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes).show_warning()
    
    def load(self):
        f = '[unmusic] album_editor.logic.Track.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.audio:
            return self.audio
        try:
            self.audio = phrydy.MediaFile(self.file)
        except Exception as e:
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes).show_warning()
        return self.audio



class Directory:
    
    def __init__(self, path):
        self.set_values()
        if path:
            self.reset(path)
    
    def _set_no(self, i, max_len):
        no = str(i + 1)
        while len(no) < max_len:
            no = '0' + no
        return no
    
    def move_tracks(self):
        f = '[unmusic] album_editor.logic.Directory.move_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        success = []
        ''' The current algorithm of tracks renumbering guarantees that
            the file list (*unless changed*) will have a consecutive numbering
            of tracks.
        '''
        max_len = len(self.audio)
        max_len = len(str(max_len))
        for i in range(len(self.audio)):
            file = self.audio[i]
            no = self._set_no(i, max_len)
            basename = no + sh.lg.Path(file).get_ext().lower()
            dest = os.path.join(self.target, basename)
            success.append(sh.lg.File(file=file, dest=dest).move())
        self.Success = not (False in success or None in success)
    
    def purge(self):
        f = '[unmusic] album_editor.logic.Directory.purge'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.tracks:
            sh.com.rep_empty(f)
            return
        mes = _('Purge tracks')
        sh.objs.get_mes(f, mes, True).show_info()
        for track in self.tracks:
            track.purge()
            track.save()
            if not track.Success:
                self.Success = False
                return
    
    def create_target(self):
        f = '[unmusic] album_editor.logic.Directory.create_target'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not objs.get_db().albumid:
            self.Success = False
            sh.com.rep_empty(f)
            return
        self.target = objs.get_default().ihome.add_share (_('processed')
                                                         ,str(objs.db.albumid)
                                                         )
        self.Success = sh.lg.Path(self.target).create()
    
    def reset(self, path):
        self.set_values()
        self.path = path
        self.idir = sh.lg.Directory(self.path)
        self.Success = self.idir.Success
        
    def get_rating(self):
        f = '[unmusic] album_editor.logic.Directory.get_rating'
        if not self.Success:
            sh.com.cancel(f)
            return
        match = re.search(r'\(rating (\d+)\)', self.path)
        if match:
            try:
                rating = match.group(1)
                if rating.isdigit():
                    self.rating = int(rating)
            except IndexError:
                pass
    
    def run(self):
        self.get_rating()
        self.create_list()
        self.get_tracks()
        if self.tracks:
            self.renumber_tracks()
            self.save_meta()
            ''' The following actions should be carried out
                only if we want to obfuscate tracks.
            '''
            self.create_target()
            self.purge()
            self.move_tracks()
            self.save_image()
        return self.Success
    
    def add_album_meta(self):
        f = '[unmusic] album_editor.logic.Directory.add_album_meta'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.tracks:
            sh.com.rep_empty(f)
            return
        ''' If a track could not be processed, empty tags will be returned,
            which, when written to DB, can cause confusion. Here we check that
            the track was processed successfully.
        '''
        if not self.tracks[0].audio:
            sh.com.rep_empty(f)
            return
        album = self.tracks[0].album
        artist = self.tracks[0].artist
        year = self.tracks[0].year
        genre = self.tracks[0].genre
        album = com.sanitize(album)
        album = com.delete_album_trash(album)
        artist = com.sanitize(artist)
        if str(year).isdigit():
            year = int(year)
        else:
            # Prevent from storing an incorrect value
            year = 0
        genre = com.sanitize(genre)
        
        search = [album,artist,str(year),genre]
        search = ' '.join(search)
        search = search.lower()
        
        objs.get_db().add_album([album, artist, year, genre, '', '', search, 0])
    
    def _add_tracks_meta(self, albumid):
        f = '[unmusic] album_editor.logic.Directory._add_tracks_meta'
        for track in self.tracks:
            data = track.get_track_meta()
            ''' If a track could not be processed, empty tags will be returned,
                which, when written to DB, can cause confusion. Here we check
                that the track was processed successfully.
            '''
            if not track.audio or not data:
                sh.com.rep_empty(f)
                return
            objs.get_db().albumid = albumid
            objs.db.add_track ([albumid, data[0], data[1], data[2], '', data[3]
                               ,data[4], data[5], self.rating
                               ]
                              )
    
    def save_meta(self):
        f = '[unmusic] album_editor.logic.Directory.save_meta'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.tracks:
            sh.com.rep_empty(f)
            return
        ''' It seems better to create new ALBUMID without checking if it
            already exists. Reasons:
            1) CD1, CD2, etc. may share same tags.
            2) Albums of different bitrate may share same tags, however, they
               are actually different albums.
            3) Since extracting metadata and obfucating are united by default,
               the program may try to overwrite already existing files in case
               there is an ALBUMID conflict (which does not and should not fail
               'Success').
            4) If tags have been edited after extraction, there is no easy way
               to establish if DB already has a corresponding ALBUMID.
        '''
        self.add_album_meta()
        albumid = objs.db.get_max_id()
        if not albumid:
            sh.com.rep_empty(f)
            return
        self._add_tracks_meta(albumid)
        mes = _('Album {}: {} tracks.')
        mes = mes.format(albumid, len(self.tracks))
        sh.objs.get_mes(f, mes, True).show_info()
    
    def set_values(self):
        self.Success = True
        self.idir = None
        self.path = ''
        self.target = ''
        self.rating = 0
        self.files = []
        self.audio = []
        self.tracks = []
    
    def create_list(self):
        f = '[unmusic] album_editor.logic.Directory.create_list'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.files:
            return self.files
        if not self.idir:
            sh.com.rep_empty(f)
            return self.files
        self.files = self.idir.get_files()
        for file in self.files:
            if sh.lg.Path(file).get_ext().lower() in TYPES:
                self.audio.append(file)
        return self.files
    
    def renumber_tracks(self):
        ''' We use track NO field instead of an autoincrement, so we must keep
            these fields unique within the same album.
        '''
        f = '[unmusic] album_editor.logic.Directory.renumber_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        nos = [i + 1 for i in range(len(self.tracks))]
        count = 0
        for i in range(len(self.tracks)):
            if self.tracks[i].no != nos[i]:
                count += 1
                self.tracks[i].no = nos[i]
        if count:
            mes = _('{}/{} tracks have been renumbered.')
            mes = mes.format(count, len(self.tracks))
            sh.objs.get_mes(f, mes, True).show_warning()
    
    def get_tracks(self):
        f = '[unmusic] album_editor.logic.Directory.get_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.tracks:
            return self.tracks
        if not self.audio:
            mes = _('Folder "{}" has no audio files.').format(self.path)
            sh.objs.get_mes(f, mes, True).show_info()
            return self.tracks
        for file in self.audio:
            self.tracks.append(Track(file=file))
        return self.tracks



class Play:
    
    def __init__(self):
        self.set_values()
        self.Success = lg.objs.get_db().Success
    
    def call_player(self):
        f = '[unmusic] album_editor.logic.Play.call_player'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.get_playlist():
            sh.com.rep_empty(f)
            return
        sh.lg.Launch(self.playlist).launch_default()
    
    def set_values(self):
        self.Success = True
        self.album = ''
        self.playlist = ''
        self.audio = []
        self.nos = []
        self.titles = []
        self.len_ = []
    
    def get_album(self):
        f = '[unmusic] album_editor.logic.Play.get_album'
        if not self.Success:
            sh.com.cancel(f)
            return self.album
        if not self.album:
            local_album = PATHS.get_local_album(lg.objs.get_db().albumid)
            exter_album = PATHS.get_external_album(lg.objs.db.albumid)
            if os.path.exists(local_album):
                self.album = local_album
            elif os.path.exists(exter_album):
                self.album = exter_album
        return self.album
    
    def get_audio(self):
        f = '[unmusic] album_editor.logic.Play.get_audio'
        if not self.Success:
            sh.com.cancel(f)
            return self.audio
        if not self.audio:
            idir = Directory(self.get_album())
            idir.create_list()
            self.Success = idir.Success
            if idir.audio:
                self.audio = idir.audio
        return self.audio
    
    def get_available(self):
        f = '[unmusic] album_editor.logic.Play.get_available'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.get_audio()
        if not (self.audio and self.nos and self.titles and self.len_):
            self.Success = False
            sh.com.rep_empty(f)
            return
        result = []
        errors = []
        for no in self.nos:
            try:
                result.append(self.audio[no])
            except IndexError:
                errors.append(no)
        ''' This may happen when some tracks have been deleted from
            a collection after filling DB or when there is a mismatch of
            ALBUMID stored in DB and the folder named after ALBUMID in the
            collection. In any case, this should not normally happen.
        '''
        if errors:
            for no in errors:
                try:
                    del self.titles[no]
                    del self.nos[no]
                    del self.len_[no]
                except IndexError:
                    pass
            errors = [str(error) for error in errors]
            mes = _('Tracks {} have not been found in "{}"!')
            mes = mes.format(errors, self.get_album())
            sh.objs.get_mes(f, mes).show_warning()
        if len(self.nos) == len(self.titles) == len(self.len_):
            pass
        else:
            self.Success = False
            sub = f'{len(self.nos)} = {len(self.titles)} = {len(self.len_)}'
            mes = _('Condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f, mes).show_error()
        return result
    
    def get_playlist(self):
        f = '[unmusic] album_editor.logic.Play.get_playlist'
        if not self.Success:
            sh.com.cancel(f)
            return self.playlist
        if not self.playlist:
            self.playlist = PATHS.get_playlist()
        return self.playlist
    
    def gen_list(self):
        f = '[unmusic] album_editor.logic.Play.gen_list'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.nos:
            sh.com.rep_empty(f)
            return
        out = []
        result = lg.objs.get_db().get_album()
        ''' Adding #EXTINF will allow to use tags in those players that support
            it (e.g., clementine, deadbeef). This entry should have the
            following format: '#EXTINF:191,Artist Name - Track Title' (multiple
            hyphens may not be supported).
        '''
        if result:
            ''' The hyphen here is actually useless, but 'deadbeef' will not
                separate an album and a title correctly otherwise.
            '''
            header = f'{result[1]}: {result[0]} - '
        else:
            header = ''
        files = self.get_available()
        if files and self.nos:
            out.write('#EXTM3U\n')
            for i in range(len(files)):
                out.append('#EXTINF:')
                out.append(str(int(self.len_[i])))
                out.append(',')
                out.append(header)
                out.append(str(self.nos[i] + 1))
                out.append('. ')
                ''' Replacing a hyphen will allow 'deadbeef' to correctly
                    distinguish between an album and a title.
                '''
                out.append(self.titles[i].replace(' - ',': ').replace(' ~ ',': '))
                out.append('\n')
                out.append(files[i])
                out.append('\n')
        else:
            sh.com.rep_empty(f)
        text = ''.join(out)
        if not text:
            sh.com.rep_empty(f)
            return
        sh.lg.WriteTextFile (file = self.get_playlist()
                            ,Rewrite = True
                            ).write(text)
    
    def play_all_tracks(self):
        f = '[unmusic] album_editor.logic.Play.play_all_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        tracks = lg.objs.get_db().get_tracks()
        if not tracks:
            sh.com.rep_empty(f)
            return
        self.titles = [track[0] for track in tracks]
        self.len_ = [track[5] for track in tracks]
        # '-1' since count starts with 1 in DB and we need 0
        self.nos = [track[1] - 1 for track in tracks]
        self.gen_list()
        self.call_player()
    
    def play_good_tracks(self, rating=8):
        f = '[unmusic] album_editor.logic.Play.play_good_tracks'
        if not self.Success:
            sh.com.cancel(f)
            return
        tracks = lg.objs.get_db().get_good_tracks(rating)
        if not tracks:
            sh.com.rep_empty(f)
            return
        self.titles = [track[0] for track in tracks]
        self.len_ = [track[5] for track in tracks]
        # '-1' since count starts with 1 in DB and we need 0
        self.nos = [track[1] - 1 for track in tracks]
        self.gen_list()
        self.call_player()



class MessagePool:

    def __init__(self, max_size=5):
        self.max_size = max_size
        self.pool = []

    def free(self):
        if len(self.pool) == self.max_size:
            self.delete_first()

    def add(self, message):
        f = '[unmusic] album_editor.logic.MessagePool.add'
        if not message:
            sh.com.rep_empty(f)
            return
        self.free()
        self.pool.append(message)

    def delete_first(self):
        f = '[unmusic] album_editor.logic.MessagePool.delete_first'
        if not self.pool:
            mes = _('The pool is empty!')
            sh.objs.get_mes(f, mes, True).show_warning()
            return
        del self.pool[0]

    def delete_last(self):
        f = '[unmusic] album_editor.logic.MessagePool.delete_last'
        if not self.pool:
            mes = _('The pool is empty!')
            sh.objs.get_mes(f, mes, True).show_warning()
            return
        del self.pool[-1]

    def clear(self):
        self.pool = []

    def get(self):
        return sh.List(lst1=self.pool).space_items()



class Collection:
    
    def __init__(self):
        self.set_paths()
    
    def set_paths(self):
        self.local = PATHS.get_local_collection()
        self.external = PATHS.get_external_collection()
        self.mobile = PATHS.get_mobile_collection()
    
    def get_local_album(self, albumid=None):
        if albumid is None:
            return os.path.join(self.local, str(lg.objs.get_db().albumid))
        else:
            return os.path.join(self.local, str(albumid))
    
    def get_ext_album(self, albumid=None):
        if albumid is None:
            return os.path.join(self.external, str(lg.objs.get_db().albumid))
        else:
            return os.path.join(self.external, str(albumid))
    
    def get_mob_album(self, albumid=None):
        if albumid is None:
            return os.path.join(self.mobile, str(lg.objs.get_db().albumid))
        else:
            return os.path.join(self.mobile, str(albumid))
    
    def has_any_album(self, albumid=None):
        return self.has_local_album(albumid) or self.has_ext_album(albumid) \
                                             or self.has_mob_album(albumid)
    
    def has_local_album(self, albumid=None):
        return os.path.exists(self.get_local_album(albumid))
    
    def has_ext_album(self, albumid=None):
        return os.path.exists(self.get_ext_album(albumid))
    
    def has_mob_album(self, albumid=None):
        return os.path.exists(self.get_mob_album(albumid))



class AlbumEditor:
    
    def __init__(self):
        self.Success = True
    
    def _has_any_album(self, albumids):
        for albumid in albumids:
            if COLLECTION.has_any_album(albumid):
                return albumid
    
    def set_prev_unrated(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.set_prev_unrated'
        if not self.Success:
            sh.com.cancel(f)
            return
        albumids = lg.objs.get_db().get_prev_unrated(lg.objs.db.albumid)
        self._set_unrated(albumids)
    
    def set_next_unrated(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.set_next_unrated'
        if not self.Success:
            sh.com.cancel(f)
            return
        albumids = lg.objs.get_db().get_next_unrated(lg.objs.db.albumid)
        self._set_unrated(albumids)
    
    def _set_unrated(self, albumids):
        f = '[unmusic] album_editor.logic.AlbumEditor._set_unrated'
        if not albumids:
            mes = _('No more matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        albumid = self._has_any_album(albumids)
        if albumid is None:
            mes = _('No more matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        lg.objs.db.albumid = albumid
        self.check_no()
    
    def set_prev_rated(self, rating=0):
        # This code is orphaned, but may be useful in the future
        f = '[unmusic] album_editor.logic.AlbumEditor.set_prev_rated'
        if not self.Success:
            sh.com.cancel(f)
            return
        albumid = lg.objs.get_db().get_prev_rated(rating, lg.objs.db.albumid)
        if not albumid:
            mes = _('No more matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        lg.objs.db.albumid = albumid
        self.check_no()
    
    def set_next_rated(self, rating=0):
        # This code is orphaned, but may be useful in the future
        f = '[unmusic] album_editor.logic.AlbumEditor.set_next_rated'
        if not self.Success:
            sh.com.cancel(f)
            return
        albumid = lg.objs.get_db().get_next_rated(rating, lg.objs.db.albumid)
        if not albumid:
            mes = _('No more matches!')
            sh.objs.get_mes(f, mes).show_info()
            return
        lg.objs.db.albumid = albumid
        self.check_no()
    
    def get_mean_bitrate(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.get_mean_bitrate'
        if not self.Success:
            sh.com.cancel(f)
            return
        mean = lg.objs.get_db().get_bitrate()
        if not mean:
            sh.com.rep_empty(f)
            return
        mean = [rating for rating in mean if rating]
        if not mean:
            return 0
        # Return 'int' since we don't need 'float' here
        return sum(mean) // len(mean)
    
    def get_mean_rating(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.get_mean_rating'
        if not self.Success:
            sh.com.cancel(f)
            return 0.0
        mean = lg.objs.get_db().get_rates()
        if not mean:
            sh.com.rep_empty(f)
            return 0.0
        ''' We should not count tracks with an undefined (0) rating, otherwise,
            if there is a mix of tracks with zero and non-zero rating,
            an overall rating will be lower than a mean rating of the non-zero
            rating tracks.
        '''
        if not mean or 0 in mean:
            return 0.0
        ''' This intentionally returns float even if all elements are equal.
            It's better to show at least 2 digits after the dot since, for
            example, an album with 30 tracks, where 29 of them have the rating
            of 8 and 1 - of 9, will have the mean rating of ~8.03.
        '''
        return round(sum(mean) / len(mean), 2)
    
    def check_no(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.check_no'
        if self.Success:
            lg.objs.get_db().albumid = sh.lg.Input(f, lg.objs.get_db().albumid).get_integer()
        else:
            sh.com.cancel(f)
        return lg.objs.get_db().albumid
    
    def get_min(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.get_min'
        if not self.Success:
            sh.com.cancel(f)
            return 0
        return sh.lg.Input(f, lg.objs.get_db().get_min_id()).get_integer()
    
    def get_max(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.get_max'
        if not self.Success:
            sh.com.cancel(f)
            return 0
        _max = lg.objs.get_db().get_max_id()
        if not isinstance(_max, int):
            mes = _('The database is empty. You need to fill it first.')
            sh.objs.get_mes(f, mes).show_warning()
            return 0
        return _max
    
    def inc(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.inc'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.check_no() == self.get_max():
            lg.objs.get_db().albumid = self.get_min()
        else:
            lg.objs.get_db().albumid = lg.objs.get_db().get_next_id()
            self.check_no()
    
    def dec(self):
        f = '[unmusic] album_editor.logic.AlbumEditor.dec'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.check_no() == self.get_min():
            lg.objs.get_db().albumid = self.get_max()
        else:
            lg.objs.get_db().albumid = lg.objs.get_db().get_prev_id()
            self.check_no()

    def _compare_albums(self, old, new):
        # Quotes in the text will fail the query, so we screen them
        new[0] = str(new[0]).replace('"', '""')
        new[1] = str(new[1]).replace('"', '""')
        new[3] = str(new[3]).replace('"', '""')
        new[4] = str(new[4]).replace('"', '""')
        new[5] = str(new[5]).replace('"', '""')
        search = [new[0], new[1], str(new[2]), new[3], new[4], new[5]]
        search = ' '.join(search)
        search = sh.lg.Text(search).delete_duplicate_spaces()
        search = search.strip().lower()
        
        add = []
        for i in range(len(new)):
            if old[i] != new[i]:
                if i == 0:
                    base = 'ALBUM="%s"'
                elif i == 1:
                    base = 'ARTIST="%s"'
                elif i == 2:
                    base = 'YEAR="%d"'
                elif i == 3:
                    base = 'GENRE="%s"'
                elif i == 4:
                    base = 'COUNTRY="%s"'
                elif i == 5:
                    base = 'COMMENT="%s"'
                elif i == 6:
                    base = 'RATING="%f"'
                add.append(base % new[i])
        if add:
            add.append('SEARCH="%s"' % search)
            add = 'begin;update ALBUMS set ' + ','.join(add)
            add += ' where ALBUMID=%d;commit;' % lg.objs.get_db().albumid
            return add


COLLECTION = Collection()
com = Commands()
