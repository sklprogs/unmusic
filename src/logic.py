#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import io
import re
import phrydy
import sqlite3

import skl_shared.shared as sh
from skl_shared.localize import _

VERSION = '1.0'
# Derived from 'phrydy.mediafile.TYPES'
TYPES = ['.mp3','.aac','.alac','.ogg','.opus','.flac','.ape','.wv'
        ,'.mpc','.asf','.aiff','.dsf'
        ]
#NOTE: Do not localize (being stored in DB)
GENRES = ('?','Alternative Rock','Ambient','Black Metal','Blues'
         ,'Brutal Death Metal','Chanson','Classical','Death Metal'
         ,'Death Metal/Grindcore','Death/Black Metal'
         ,'Death/Thrash Metal','Deathcore','Electronic','Ethnic','Game'
         ,'Goregrind','Grindcore','Heavy Metal','Industrial Metal'
         ,'Melodic Death Metal','Metal','Pop','Power Metal','Rap'
         ,'Relaxation','Rock','Soundtrack'
         ,'Technical Brutal Death Metal','Technical Death Metal'
         ,'Thrash Metal','Vocal'
         )
''' Can have genres not comprised by GENRES (since GENRES is used to
    fill GUI and has a limit).
'''
LIGHT = ('Alternative Rock','Ambient','Blues','Chanson','Classical'
        ,'Electronic','Ethnic','Game','Pop','Rap','Relaxation','Rock'
        ,'Soundtrack','Vocal','Folk'
        )
HEAVY = ('Black Metal','Brutal Death Metal','Death Metal'
        ,'Death Metal/Grindcore','Death/Black Metal'
        ,'Death/Thrash Metal','Deathcore','Goregrind','Grindcore'
        ,'Heavy Metal','Industrial Metal','Melodic Death Metal','Metal'
        ,'Power Metal','Technical Brutal Death Metal'
        ,'Technical Death Metal','Thrash Metal'
        )


class BadMusic:
    
    def __init__(self):
        self.set_values()
        self.Success = objs.get_db().Success
    
    def set_values(self):
        self.Success = True
        self.rates  = []
        self.sizes  = []
        self.dellst = []
        self.local  = ''
        self.exter  = ''
        self.mobil  = ''
        
    def get_all_carriers(self):
        f = '[unmusic] logic.BadMusic.get_all_carriers'
        if self.Success:
            self.local = objs.get_default().ihome.add_share(_('local collection'))
            self.exter = objs.default.ihome.add_share(_('external collection'))
            self.mobil = objs.default.ihome.add_share(_('mobile collection'))
            mes = _('Local collection: {}').format(self.local)
            sh.objs.get_mes(f,mes,True).show_debug()
            mes = _('External collection: {}').format(self.exter)
            sh.objs.get_mes(f,mes,True).show_debug()
            mes = _('Mobile collection: {}').format(self.mobil)
            sh.objs.get_mes(f,mes,True).show_debug()
            if self.local and self.exter and self.mobil:
                return True
            else:
                self.Success = False
                mes = _('Empty output is not allowed!')
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.cancel(f)
    
    def get_affected_carriers(self):
        f = '[unmusic] logic.BadMusic.get_affected_carriers'
        self.get_all_carriers()
        if self.Success:
            if self.dellst:
                affected = []
                for item in self.dellst:
                    if self.local in item:
                        affected.append(_('local collection'))
                        break
                for item in self.dellst:
                    if self.exter in item:
                        affected.append(_('external collection'))
                        break
                for item in self.dellst:
                    if self.mobil in item:
                        affected.append(_('mobile collection'))
                        break
                return affected
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def delete(self):
        f = '[unmusic] logic.BadMusic.delete'
        if self.Success:
            if self.dellst:
                for album in self.dellst:
                    if not sh.Directory(album).delete():
                        mes = _('Operation has been canceled.')
                        sh.objs.get_mes(f,mes).show_warning()
                        break
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def report(self):
        f = '[unmusic] logic.BadMusic.report'
        if self.Success:
            if self.rates and self.sizes:
                iterable = []
                for i in range(len(self.rates)):
                    if self.sizes[i]:
                        size = sh.com.get_human_size (bsize     = self.sizes[i]
                                                     ,LargeOnly = True
                                                     )
                    else:
                        size = _('N/A')
                    iterable.append(self.rates[i]+[size])
                headers = ('ID','ALBUM','MIN','MAX','SIZE')
                mes = sh.FastTable (iterable  = iterable
                                   ,headers   = headers
                                   ,Transpose = True
                                   ,maxrow    = 70
                                   ).run()
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_empty(f)
    
    def get_sizes(self):
        f = '[unmusic] logic.BadMusic.get_sizes'
        self.get_all_carriers()
        if self.Success:
            if self.rates:
                for item in self.rates:
                    albumid = str(item[0])
                    path1   = os.path.join(self.local,albumid)
                    path2   = os.path.join(self.exter,albumid)
                    path3   = os.path.join(self.mobil,albumid)
                    if os.path.exists(path1):
                        size1 = sh.Directory(path1).get_size()
                        self.dellst.append(path1)
                    else:
                        size1 = 0
                    if os.path.exists(path2):
                        size2 = sh.Directory(path2).get_size()
                        self.dellst.append(path2)
                    else:
                        size2 = 0
                    if os.path.exists(path3):
                        size3 = sh.Directory(path3).get_size()
                        self.dellst.append(path3)
                    else:
                        size3 = 0
                    size = size1 + size2 + size3
                    self.sizes.append(size)
                return self.sizes
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_rates(self,limit=0,max_rate=4):
        f = '[unmusic] logic.BadMusic.get_rates'
        if self.Success:
            # ALBUMID (0), ALBUM (1), ARTIST (2), YEAR (3)
            albums = objs.get_db().get_albums(limit)
            if albums:
                old = objs.db.albumid
                for album in albums:
                    objs.db.albumid = album[0]
                    mes = _('Process album ID: {}')
                    mes = mes.format(objs.db.albumid)
                    sh.objs.get_mes(f,mes,True).show_debug()
                    rates = objs.db.get_rates()
                    if rates:
                        if min(rates) > 0 and max(rates) <= max_rate:
                            album_title = [str(album[2]),str(album[3])
                                          ,str(album[1])
                                          ]
                            album_title = ' - '.join(album_title)
                            item = [album[0],album_title
                                   ,min(rates),max(rates)
                                   ]
                            self.rates.append(item)
                    else:
                        sh.com.rep_empty(f)
                objs.db.albumid = old
                return self.rates
            else:
                sh.com.cancel(f)
        else:
            sh.com.cancel(f)



class Caesar:
    
    def __init__(self):
        self.seq1 = ('a','b','c','d','e','f','g','h','i','j','k','l'
                    ,'m','n','o','p','q','r','s','t','u','v','w','x'
                    ,'y','z','A','B','C','D','E','F','G','H','I','J'
                    ,'K','L','M','N','O','P','Q','R','S','T','U','V'
                    ,'W','X','Y','Z','а','б','в','г','д','е','ё','ж'
                    ,'з','и','й','к','л','м','н','о','п','р','с','т'
                    ,'у','ф','х','ц','ч','ш','щ','ь','ъ','ы','э','ю'
                    ,'я','А','Б','В','Г','Д','Е','Ё','Ж','З','И','Й'
                    ,'К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х'
                    ,'Ц','Ч','Ш','Щ','Ь','Ъ','Ы','Э','Ю','Я'
                    )
        self.seq2 = ('C','D','f','d','e','i','R','t','n','g','u','b'
                    ,'B','k','S','N','y','m','j','U','P','J','M','H'
                    ,'E','V','I','p','v','l','G','s','Q','Z','h','A'
                    ,'X','a','W','O','K','c','o','w','T','q','z','x'
                    ,'r','F','L','Y','Н','И','Щ','ю','д','з','к','г'
                    ,'л','й','б','ж','ё','в','а','Ш','э','Ы','О','Ф'
                    ,'П','и','У','е','п','ы','В','А','К','н','м','Л'
                    ,'ъ','у','ф','М','Б','с','Ц','о','я','Ь','Й','Х'
                    ,'х','Я','Г','Е','Т','С','Р','Ъ','р','Ж','ц','щ'
                    ,'Ё','Э','т','Ч','ч','ш','ь','Ю','Д','З'
                    )
        assert len(self.seq1) == len(self.seq2)
    
    def cypher(self,text):
        lst = list(text)
        for i in range(len(lst)):
            try:
                ind = self.seq1.index(lst[i])
                lst[i] = self.seq2[ind]
            except ValueError:
                pass
        return ''.join(lst)
    
    def decypher(self,text):
        lst = list(text)
        for i in range(len(lst)):
            try:
                ind = self.seq2.index(lst[i])
                lst[i] = self.seq1[ind]
            except ValueError:
                pass
        return ''.join(lst)
        



class Play:
    
    def __init__(self):
        self.set_values()
        self.Success = objs.get_db().Success
    
    def call_player(self):
        f = '[unmusic] logic.Play.call_player'
        if self.Success:
            if self.get_playlist():
                sh.lg.Launch(self.playlist).launch_default()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success  = True
        self.album    = ''
        self.playlist = ''
        self.audio    = []
        self.nos      = []
        self.titles   = []
        self.len_     = []
    
    def get_album(self):
        f = '[unmusic] logic.Play.get_album'
        if self.Success:
            if not self.album:
                local_album = objs.get_default().ihome.add_share (_('local collection')
                                                                 ,str(objs.get_db().albumid)
                                                                 )
                exter_album = objs.default.ihome.add_share (_('external collection')
                                                           ,str(objs.db.albumid)
                                                           )
                local_exists = os.path.exists(local_album)
                exter_exists = os.path.exists(exter_album)
                if local_exists:
                    self.album = local_album
                elif exter_exists:
                    self.album = exter_album
        else:
            sh.com.cancel(f)
        return self.album
    
    def get_audio(self):
        f = '[unmusic] logic.Play.get_audio'
        if self.Success:
            if not self.audio:
                idir = Directory(self.get_album())
                idir.create_list()
                self.Success = idir.Success
                if idir.audio:
                    self.audio = idir.audio
        else:
            sh.com.cancel(f)
        return self.audio
    
    def get_available(self):
        f = '[unmusic] logic.Play.get_available'
        if self.Success:
            self.get_audio()
            if self.audio and self.nos and self.titles and self.len_:
                result = []
                errors = []
                for no in self.nos:
                    try:
                        result.append(self.audio[no])
                    except IndexError:
                        errors.append(no)
                ''' This may happen when some tracks have been deleted
                    from a collection after filling DB or when there is
                    a mismatch of ALBUMID stored in DB and the folder
                    named after ALBUMID in the collection. In any case,
                    this should not normally happen.
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
                    mes = mes.format(errors,self.get_album())
                    sh.objs.get_mes(f,mes).show_warning()
                if len(self.nos) == len(self.titles) == len(self.len_):
                    pass
                else:
                    self.Success= False
                    sub = '{} = {} = {}'.format (len(self.nos)
                                                ,len(self.titles)
                                                ,len(self.len_)
                                                )
                    mes = _('Condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.get_mes(f,mes).show_error()
                return result
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_playlist(self):
        f = '[unmusic] logic.Play.get_playlist'
        if self.Success:
            if not self.playlist:
                self.playlist = _('playlist') + '.m3u8'
                self.playlist = objs.get_default().ihome.add_share(self.playlist)
        else:
            sh.com.cancel(f)
        return self.playlist
    
    def gen_list(self):
        f = '[unmusic] logic.Play.gen_list'
        if self.Success:
            if self.nos:
                self.out = io.StringIO()
                result = objs.get_db().get_album()
                ''' Adding #EXTINF will allow to use tags in those
                    players that support it (e.g., clementine,
                    deadbeef). This entry should have the following
                    format: #EXTINF:191,Artist Name - Track Title
                    (multiple hyphens may not be supported).
                '''
                if result:
                    ''' The hyphen here is actually useless, but
                        'deadbeef' will not separate an album and
                        a title correctly otherwise.
                    '''
                    header = result[1] + ': ' + result[0] + ' - '
                else:
                    header = ''
                files = self.get_available()
                if files and self.nos:
                    self.out.write('#EXTM3U\n')
                    for i in range(len(files)):
                        self.out.write('#EXTINF:')
                        self.out.write(str(int(self.len_[i])))
                        self.out.write(',')
                        self.out.write(header)
                        self.out.write(str(self.nos[i]+1))
                        self.out.write('. ')
                        ''' Replacing a hyphen will allow 'deadbeef'
                            to correctly distinguish between an album
                            and a title.
                        '''
                        self.out.write(self.titles[i].replace(' - ',': ').replace(' ~ ',': '))
                        self.out.write('\n')
                        self.out.write(files[i])
                        self.out.write('\n')
                else:
                    sh.com.rep_empty(f)
                text = self.out.getvalue()
                self.out.close()
                if text:
                    sh.lg.WriteTextFile (file    = self.get_playlist()
                                        ,Rewrite = True
                                        ).write(text)
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def play_all_tracks(self):
        f = '[unmusic] logic.Play.play_all_tracks'
        if self.Success:
            tracks = objs.get_db().get_tracks()
            if tracks:
                self.titles = [track[0] for track in tracks]
                self.len_   = [track[5] for track in tracks]
                # '-1' since count starts with 1 in DB and we need 0
                self.nos = [track[1] - 1 for track in tracks]
                self.gen_list()
                self.call_player()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def play_good_tracks(self,rating=8):
        f = '[unmusic] logic.Play.play_good_tracks'
        if self.Success:
            tracks = objs.get_db().get_good_tracks(rating)
            if tracks:
                self.titles = [track[0] for track in tracks]
                self.len_   = [track[5] for track in tracks]
                # '-1' since count starts with 1 in DB and we need 0
                self.nos = [track[1] - 1 for track in tracks]
                self.gen_list()
                self.call_player()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)



class AlbumEditor:
    
    def __init__(self):
        self.Success = True
    
    def get_prev_rated(self,rating=0):
        f = '[unmusic] logic.AlbumEditor.get_prev_rated'
        if self.Success:
            result = objs.get_db().get_prev_rated(rating)
            if result:
                objs.get_db().albumid = result
                self.get_no()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_next_rated(self,rating=0):
        f = '[unmusic] logic.AlbumEditor.next_rated'
        if self.Success:
            result = objs.get_db().get_next_rated(rating)
            if result:
                objs.get_db().albumid = result
                self.get_no()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_mean_bitrate(self):
        f = '[unmusic] logic.AlbumEditor.get_mean_bitrate'
        if self.Success:
            mean = objs.get_db().get_bitrate()
            if mean:
                mean = [rating for rating in mean if rating]
                if mean:
                    # Return 'int' since we don't need 'float' here
                    return sum(mean) // len(mean)
                else:
                    return 0
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_mean_rating(self):
        f = '[unmusic] logic.AlbumEditor.get_mean_rating'
        if self.Success:
            mean = objs.get_db().get_rating()
            if mean:
                ''' We should not count tracks with an undefined (0)
                    rating, otherwise, if there is a mix of tracks with
                    zero and non-zero rating, an overall rating will be
                    lower than a mean rating of the non-zero rating
                    tracks.
                '''
                mean = [rating for rating in mean if rating]
                if mean:
                    ''' This (intentionally) returns float even if all
                        elements are equal.
                    '''
                    return sum(mean) / len(mean)
                else:
                    return 0.0
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_no(self):
        f = '[unmusic] logic.AlbumEditor.get_no'
        if self.Success:
            objs.get_db().albumid = sh.lg.Input(f,objs.get_db().albumid).get_integer()
        else:
            sh.com.cancel(f)
        return objs.get_db().albumid
    
    def get_min(self):
        f = '[unmusic] logic.AlbumEditor.get_min'
        if self.Success:
            return sh.lg.Input(f,objs.get_db().get_min_id()).get_integer()
        else:
            sh.com.cancel(f)
            return 0
    
    def get_max(self):
        f = '[unmusic] logic.AlbumEditor.get_max'
        if self.Success:
            _max = objs.get_db().get_max_id()
            if isinstance(_max,int):
                return _max
            else:
                mes = _('The database is empty. You need to fill it first.')
                sh.objs.get_mes(f,mes).show_warning()
                return 0
        else:
            sh.com.cancel(f)
            return 0
    
    def inc(self):
        f = '[unmusic] logic.AlbumEditor.inc'
        if self.Success:
            if self.get_no() == self.get_max():
                objs.get_db().albumid = self.get_min()
            else:
                objs.get_db().albumid = objs.get_db().get_next_id()
                self.get_no()
        else:
            sh.com.cancel(f)
    
    def dec(self):
        f = '[unmusic] logic.AlbumEditor.dec'
        if self.Success:
            if self.get_no() == self.get_min():
                objs.get_db().albumid = self.get_max()
            else:
                objs.get_db().albumid = objs.get_db().get_prev_id()
                self.get_no()
        else:
            sh.com.cancel(f)

    def _compare_albums(self,old,new):
        f = '[unmusic] logic.AlbumEditor.compare_albums'
        # Quotes in the text will fail the query, so we screen them
        new[0] = str(new[0]).replace('"','""')
        new[1] = str(new[1]).replace('"','""')
        new[3] = str(new[3]).replace('"','""')
        new[4] = str(new[4]).replace('"','""')
        new[5] = str(new[5]).replace('"','""')
        search = [new[0],new[1],str(new[2]),new[3],new[4],new[5]]
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
                add.append(base % new[i])
        if add:
            add.append('SEARCH="%s"' % search)
            add = 'begin;update ALBUMS set ' + ','.join(add)
            add += ' where ALBUMID=%d;commit;' % objs.get_db().albumid
            return add



class Directory:
    
    def __init__(self,path):
        self.set_values()
        if path:
            self.reset(path)
    
    def _set_no(self,i,max_len):
        no = str(i+1)
        while len(no) < max_len:
            no = '0' + no
        return no
    
    def move_tracks(self):
        f = '[unmusic] logic.Directory.move_tracks'
        if self.Success:
            success = []
            ''' The current algorithm of tracks renumbering guarantees
                that the file list (*unless changed*) will have
                a consecutive numbering of tracks.
            '''
            max_len = len(self.audio)
            max_len = len(str(max_len))
            for i in range(len(self.audio)):
                file     = self.audio[i]
                no       = self._set_no(i,max_len)
                basename = no + sh.lg.Path(file).get_ext().lower()
                dest     = os.path.join (self.target
                                        ,basename
                                        )
                success.append(sh.lg.File(file=file,dest=dest).move())
            self.Success = not (False in success or None in success)
        else:
            sh.com.cancel(f)
    
    def purge(self):
        f = '[unmusic] logic.Directory.purge'
        if self.Success:
            if self.tracks:
                mes = _('Purge tracks')
                sh.objs.get_mes(f,mes,True).show_info()
                for track in self.tracks:
                    track.purge()
                    track.save()
                    if not track.Success:
                        self.Success = False
                        break
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def create_target(self):
        f = '[unmusic] logic.Directory.create_target'
        if self.Success:
            if objs.get_db().albumid:
                self.target = objs.get_default().ihome.add_share (_('processed')
                                                              ,str(objs.db.albumid)
                                                              )
                self.Success = sh.lg.Path(self.target).create()
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def reset(self,path):
        self.set_values()
        self.path   = path
        self.idir    = sh.lg.Directory(self.path)
        self.Success = self.idir.Success
        if self.Success and '(decypher)' in self.path:
            self.Decypher = True
        
    def get_rating(self):
        f = '[unmusic] logic.Directory.get_rating'
        if self.Success:
            match = re.search(r'\(rating (\d+)\)',self.path)
            if match:
                try:
                    rating = match.group(1)
                    if rating.isdigit():
                        self.rating = int(rating)
                except IndexError:
                    pass
        else:
            sh.com.cancel(f)
    
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
        return self.Success
    
    def decypher_album(self):
        f = '[unmusic] logic.Directory.decypher_album'
        if self.Success:
            if self.Decypher:
                basename = sh.lg.Path(self.path).get_basename()
                basename = objs.get_caesar().decypher(basename)
                if basename:
                    if basename.count(' - ') == 2:
                        return basename.split(' - ')
                    else:
                        mes = _('Wrong input data: "{}"!')
                        mes = mes.format(basename)
                        sh.objs.get_mes(f,mes,True).show_warning()
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def add_album_meta(self):
        f = '[unmusic] logic.Directory.add_album_meta'
        if self.Success:
            if self.tracks:
                ''' If a track could not be processed, empty tags will
                    be returned, which, when written to DB, can cause
                    confusion. Here we check that the track was
                    processed successfully.
                '''
                if self.tracks[0].audio:
                    album  = self.tracks[0].album
                    artist = self.tracks[0].artist
                    year   = self.tracks[0].year
                    genre  = self.tracks[0].genre
                    image  = self.tracks[0].image
                    result = self.decypher_album()
                    if result:
                        if len(result) == 3:
                            artist = result[0]
                            if str(result[1]).isdigit():
                                year = int(result[1])
                            album = result[2]
                        else:
                            sub = '{} = {}'.format(len(result),3)
                            mes = _('Condition "{}" is not observed!')
                            mes = mes.format(sub)
                            sh.objs.get_mes(f,mes).show_error()
                    album  = com.sanitize(album)
                    album  = com.delete_album_trash(album)
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
                    
                    objs.get_db().add_album ([album,artist,year,genre
                                             ,'','',search,image
                                             ]
                                            )
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def _add_tracks_meta(self,albumid):
        f = '[unmusic] logic.Directory._add_tracks_meta'
        for track in self.tracks:
            data = track.get_track_meta()
            ''' If a track could not be processed, empty tags will be
                returned, which, when written to DB, can cause
                confusion. Here we check that the track was processed
                successfully.
            '''
            if track.audio and data:
                objs.get_db().albumid = albumid
                objs.db.add_track ([albumid,data[0],data[1],data[2]
                                    ,'',data[3],data[4],data[5]
                                    ,self.rating
                                    ]
                                   )
            else:
                sh.com.rep_empty(f)
    
    def save_meta(self):
        f = '[unmusic] logic.Directory.save_meta'
        if self.Success:
            if self.tracks:
                ''' It seems better to create new ALBUMID without
                    checking if it already exists. Reasons:
                    1) CD1, CD2, etc. may share same tags.
                    2) Albums of different bitrate may share same tags,
                       however, they are actually different albums.
                    3) Since extracting metadata and obfucating are 
                       united by default, the program may try to 
                       overwrite already existing files in case there is
                       an ALBUMID conflict (which does not and should
                       not fail 'Success').
                    4) If tags have been edited after extraction, there
                       is no easy way to establish if DB already has
                       a corresponding ALBUMID.
                '''
                self.add_album_meta()
                albumid = objs.db.get_max_id()
                if albumid:
                    self._add_tracks_meta(albumid)
                    mes = _('Album {}: {} tracks.')
                    mes = mes.format(albumid,len(self.tracks))
                    sh.objs.get_mes(f,mes,True).show_info()
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success  = True
        self.Decypher = False
        self.idir     = None
        self.path     = ''
        self.target   = ''
        self.rating   = 0
        self.files    = []
        self.audio    = []
        self.tracks   = []
    
    def create_list(self):
        f = '[unmusic] logic.Directory.create_list'
        if self.Success:
            if not self.files:
                if self.idir:
                    self.files = self.idir.get_files()
                    for file in self.files:
                        if sh.lg.Path(file).get_ext().lower() in TYPES:
                            self.audio.append(file)
                else:
                    sh.com.rep_empty(f)
            return self.files
        else:
            sh.com.cancel(f)
    
    def renumber_tracks(self):
        ''' We use track NO field instead of an autoincrement, so we
            must keep these fields unique within the same album.
        '''
        f = '[unmusic] logic.Directory.renumber_tracks'
        if self.Success:
            nos = [i + 1 for i in range(len(self.tracks))]
            count = 0
            for i in range(len(self.tracks)):
                if self.tracks[i].no != nos[i]:
                    count += 1
                    self.tracks[i].no = nos[i]
            if count:
                mes = _('{}/{} tracks have been renumbered.')
                mes = mes.format(count,len(self.tracks))
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def get_tracks(self):
        f = '[unmusic] logic.Directory.get_tracks'
        if self.Success:
            if not self.tracks:
                if self.audio:
                    for file in self.audio:
                        self.tracks.append (Track (file     = file
                                                   ,Decypher = self.Decypher
                                                   )
                                            )
                else:
                    mes = _('Folder "{}" has no audio files.')
                    mes = mes.format(self.path)
                    sh.objs.get_mes(f,mes,True).show_info()
            return self.tracks
        else:
            sh.com.cancel(f)



class DefaultConfig:
    
    def __init__(self):
        self.set_values()
        self.ihome   = sh.lg.Home(app_name='unmusic')
        self.Success = self.ihome.create_conf()
    
    def run(self):
        self.get_db()
    
    def set_values(self):
        self.fdb = ''
    
    def get_db(self):
        f = '[unmusic] logic.DefaultConfig.get_db'
        if self.Success:
            self.fdb = self.ihome.add_config('unmusic.db')
            if self.fdb:
                if os.path.exists(self.fdb):
                    self.Success = sh.lg.File(file=self.fdb).Success
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)



class Objects:
    
    def __init__(self):
        self.default = self.db = self.caesar = None
        
    def get_caesar(self):
        if self.caesar is None:
            self.caesar = Caesar()
        return self.caesar
    
    def get_db(self):
        f = '[unmusic] logic.Objects.get_db'
        if self.db is None:
            path = self.get_default().fdb
            if self.default.Success:
                self.db = DB(path=path)
            else:
                mes = _('Wrong input data!')
                sh.objs.get_mes(f,mes,True).show_warning()
                self.db = DB()
        return self.db
    
    def get_default(self):
        if self.default is None:
            self.default = DefaultConfig()
            self.default.run()
        return self.default



class DB:
    
    def __init__(self,path):
        self.Success = True
        self.albumid = 1
        self.path    = path
        self.connect()
        self.create_albums()
        self.create_tracks()
    
    def get_albums(self,limit=0):
        f = '[unmusic] logic.DB.get_albums'
        if self.Success:
            try:
                # limit=0 provides an empty ouput
                if limit:
                    self.dbc.execute ('select ALBUMID,ALBUM,ARTIST,YEAR\
                                       from ALBUMS order by ALBUMID \
                                       limit ?',(limit,)
                                     )
                else:
                    self.dbc.execute ('select ALBUMID,ALBUM,ARTIST,YEAR\
                                       from ALBUMS order by ALBUMID'
                                     )
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_rates(self):
        ''' When operating on entire albums (e.g., deleting bad music),
            we need to know minimum and maximum ratings
            (e.g., 0 < album rate < 5 for ALL tracks of bad albums).
        '''
        f = '[unmusic] logic.DB.get_rates'
        if self.Success:
            try:
                self.dbc.execute ('select RATING from TRACKS \
                                   where ALBUMID = ? \
                                   order by NO'
                                 ,(self.albumid,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_prev_rated(self,rating=0):
        f = '[unmusic] logic.DB.get_prev_rated'
        if self.Success:
            try:
                self.dbc.execute ('select ALBUMID from TRACKS \
                                   where ALBUMID < ? and RATING = ? \
                                   order by ALBUMID desc'
                                 ,(self.albumid,rating,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_next_rated(self,rating=0):
        f = '[unmusic] logic.DB.get_next_rated'
        if self.Success:
            try:
                self.dbc.execute ('select ALBUMID from TRACKS \
                                   where ALBUMID > ? and RATING = ? \
                                   order by ALBUMID'
                                 ,(self.albumid,rating,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_brief(self,ids):
        f = '[unmusic] logic.DB.get_brief'
        if self.Success:
            if ids:
                ''' Sometimes ARTIST + YEAR + ALBUM combinations are
                    identical, e.g., there are several CDs for the same
                    album or there are identical albums of a different
                    quality. This leads to identical IDs at
                    'unmusic.Copy.select_albums'. To avoid this, we add
                    ALBUMID.
                '''
                try:
                    query = 'select ALBUMID,ARTIST,YEAR,ALBUM \
                             from ALBUMS where ALBUMID in (%s)' \
                             % ','.join('?'*len(ids))
                    self.dbc.execute(query,ids)
                    result = self.dbc.fetchall()
                    if result:
                        lst = [str(item[0]) + ': ' + ' - '.join ([item[1]
                                                                 ,str(item[2])
                                                                 ,item[3]
                                                                 ]
                                                                )\
                               for item in result
                              ]
                        return '\n'.join(lst)
                        
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_unknown_genre(self,limit=0):
        f = '[unmusic] logic.DB.get_unknown_genre'
        if self.Success:
            try:
                if limit:
                    self.dbc.execute ('select ALBUMID from ALBUMS \
                                       where GENRE = ? limit ? \
                                       order by ALBUMID'
                                     ,('?',limit,)
                                     )
                else:
                    self.dbc.execute ('select ALBUMID from ALBUMS \
                                       where GENRE = ? order by ALBUMID'
                                     ,('?',)
                                     )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_rated(self,rating=0,limit=0):
        f = '[unmusic] logic.DB.get_unrated'
        if self.Success:
            try:
                if limit:
                    self.dbc.execute ('select distinct ALBUMID \
                                       from TRACKS where RATING = ? \
                                       limit ?',(rating,limit,)
                                     )
                else:
                    self.dbc.execute ('select distinct ALBUMID \
                                       from TRACKS where RATING = ?'
                                     ,(rating,)
                                     )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_good_tracks(self,rating=8):
        f = '[unmusic] logic.DB.get_good_tracks'
        if self.Success:
            try:
                self.dbc.execute ('select   TITLE,NO,LYRICS,COMMENT \
                                           ,BITRATE,LENGTH,RATING \
                                   from     TRACKS where ALBUMID = ? \
                                   and      RATING >= ?\
                                   order by NO',(self.albumid,rating,)
                                 )
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def has_id(self,albumid):
        ''' A major difference from 'get_album': we do not need
            to assign 'self.albumid' to establish whether the input is
            valid or not.
        '''
        f = '[unmusic] logic.DB.has_id'
        if self.Success:
            try:
                self.dbc.execute ('select ALBUMID from ALBUMS \
                                   where  ALBUMID = ?',(albumid,)
                                 )
                return self.dbc.fetchone()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def update_track(self,no,data):
        f = '[unmusic] logic.DB.update_track'
        if self.Success:
            if no and data:
                if len(data) == 4:
                    try:
                        self.dbc.execute ('update TRACKS set TITLE = ?\
                                                 ,LYRICS = ?,COMMENT = ?\
                                                 ,RATING = ? \
                                           where ALBUMID = ? and NO = ?'
                                          ,(data[0],data[1],data[2]
                                           ,data[3],self.albumid,no
                                           )
                                         )
                    except Exception as e:
                        self.fail(f,e)
                else:
                    sub = '{} = {}'.format(len(data),4)
                    mes = _('Condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.get_mes(f,mes).show_error()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def check_nos(self):
        ''' We use track NO field instead of an autoincrement, so we
            must keep these fields unique within the same album.
            Tracks should have already been renumbered if required
            with 'unmusic.logic.Directory.renumber_tracks', however, we check
            this again just to be sure.
        '''
        f = '[unmusic] logic.DB.check_nos'
        if self.Success:
            try:
                self.dbc.execute ('select NO from TRACKS \
                                   where ALBUMID = ? order by NO'
                                  ,(self.albumid,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    result = [item[0] for item in result]
                    nos    = [i + 1 for i in range(len(result))]
                    return result == nos
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_length(self):
        f = '[unmusic] logic.DB.get_length'
        if self.Success:
            try:
                self.dbc.execute ('select LENGTH from TRACKS \
                                   where ALBUMID = ? order by NO'
                                  ,(self.albumid,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_bitrate(self):
        f = '[unmusic] logic.DB.get_bitrate'
        if self.Success:
            try:
                self.dbc.execute ('select BITRATE from TRACKS \
                                   where ALBUMID = ? order by NO'
                                  ,(self.albumid,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def delete(self):
        f = '[unmusic] logic.DB.delete'
        if self.Success:
            try:
                self.dbc.execute ('delete from ALBUMS where ALBUMID = ?'
                                 ,(self.albumid,)
                                 )
                self.dbc.execute ('delete from TRACKS where ALBUMID = ?'
                                 ,(self.albumid,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_rating(self):
        f = '[unmusic] logic.DB.get_rating'
        if self.Success:
            try:
                self.dbc.execute ('select RATING from TRACKS \
                                   where ALBUMID = ? order by NO'
                                  ,(self.albumid,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def set_rating(self,value):
        f = '[unmusic] logic.DB.set_rating'
        if self.Success:
            try:
                self.dbc.execute ('update TRACKS set RATING = ? \
                                   where ALBUMID = ?'
                                 ,(value,self.albumid,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def updateDB(self,query):
        f = '[unmusic] logic.DB.updateDB'
        if self.Success:
            if query:
                try:
                    self.dbc.executescript(query)
                except Exception as e:
                    mes = _('Unable to execute:\n"{}"\n\nDetails: {}')
                    mes = mes.format(str(query).replace(';',';\n'),e)
                    sh.objs.get_mes(f,mes).show_error()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_tracks(self):
        f = '[unmusic] logic.DB.get_tracks'
        if self.Success:
            try:
                self.dbc.execute ('select   TITLE,NO,LYRICS,COMMENT \
                                           ,BITRATE,LENGTH,RATING \
                                   from     TRACKS where ALBUMID = ? \
                                   order by NO',(self.albumid,)
                                 )
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def search_track(self,pattern,limit=50):
        f = '[unmusic] logic.DB.search_track'
        if self.Success:
            if pattern:
                pattern = '%' + pattern.lower() + '%'
                try:
                    self.dbc.execute ('select   ALBUMID,TITLE,NO,LYRICS\
                                               ,COMMENT,BITRATE,LENGTH\
                                               ,RATING from TRACKS \
                                       where    SEARCH like ? \
                                       order by ALBUMID,NO limit ?'
                                      ,(pattern,limit,)
                                     )
                    return self.dbc.fetchall()
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_next_album(self,search):
        f = '[unmusic] logic.DB.get_next_album'
        if self.Success:
            if search:
                search = '%' + search.lower() + '%'
                try:
                    self.dbc.execute ('select   ALBUMID from ALBUMS \
                                       where    ALBUMID > ? \
                                       and      SEARCH like ? \
                                       order by ALBUMID'
                                      ,(self.albumid,search,)
                                     )
                    result = self.dbc.fetchone()
                    if result:
                        return result[0]
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_prev_album(self,search):
        f = '[unmusic] logic.DB.get_prev_album'
        if self.Success:
            if search:
                search = '%' + search.lower() + '%'
                try:
                    self.dbc.execute ('select   ALBUMID from ALBUMS \
                                       where    ALBUMID < ? \
                                       and      SEARCH like ? \
                                       order by ALBUMID desc'
                                      ,(self.albumid,search,)
                                     )
                    result = self.dbc.fetchone()
                    if result:
                        return result[0]
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_prev_id(self):
        f = '[unmusic] logic.DB.get_prev_id'
        if self.Success:
            try:
                self.dbc.execute ('select   ALBUMID from ALBUMS \
                                   where    ALBUMID < ? \
                                   order by ALBUMID desc'
                                 ,(self.albumid,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_next_id(self):
        f = '[unmusic] logic.DB.get_next_id'
        if self.Success:
            try:
                self.dbc.execute ('select ALBUMID from ALBUMS \
                                   where  ALBUMID > ? order by ALBUMID'
                                  ,(self.albumid,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_album(self):
        f = '[unmusic] logic.DB.get_album'
        if self.Success:
            try:
                self.dbc.execute ('select ALBUM,ARTIST,YEAR,GENRE\
                                         ,COUNTRY,COMMENT,IMAGE \
                                   from   ALBUMS \
                                   where  ALBUMID = ?',(self.albumid,)
                                 )
                return self.dbc.fetchone()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_min_id(self):
        f = '[unmusic] logic.DB.get_min_id'
        if self.Success:
            try:
                ''' 'self.dbc.lastrowid' returns 'None' if an album is
                    already in DB.
                '''
                self.dbc.execute ('select   ALBUMID from ALBUMS \
                                   order by ALBUMID'
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_max_id(self):
        f = '[unmusic] logic.DB.get_max_id'
        if self.Success:
            try:
                ''' 'self.dbc.lastrowid' returns 'None' if an album is
                    already in DB.
                '''
                self.dbc.execute ('select   ALBUMID from ALBUMS \
                                   order by ALBUMID desc'
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def has_track(self,no,bitrate):
        ''' Since tags may be missing, we use a track number to identify
            a track. Different bitrates refer to different tracks.
        '''
        f = '[unmusic] logic.DB.has_track'
        if self.Success:
            try:
                self.dbc.execute ('select TITLE from TRACKS \
                                   where  ALBUMID = ? and NO = ? \
                                   and    BITRATE = ?'
                                  ,(self.albumid,no,bitrate,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def has_album(self,artist,year,album):
        f = '[unmusic] logic.DB.has_album'
        if self.Success:
            try:
                self.dbc.execute ('select ALBUMID from ALBUMS \
                                   where  ARTIST = ? and YEAR = ? \
                                   and    ALBUM = ?'
                                   ,(artist,year,album,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def print (self,Selected=False,Shorten=False
              ,MaxRow=20,MaxRows=20,table='TRACKS'
              ):
        f = '[unmusic] logic.DB.print'
        if self.Success:
            ''' 'self.dbc.description' is 'None' without performing 
                'select' first
             '''
            if not Selected:
                self.dbc.execute('select * from %s' % table)
            headers = [cn[0] for cn in self.dbc.description]
            rows    = self.dbc.fetchall()
            sh.lg.Table (headers = headers
                        ,rows    = rows
                        ,Shorten = Shorten
                        ,MaxRow  = MaxRow
                        ,MaxRows = MaxRows
                        ).print()
        else:
            sh.com.cancel(f)
    
    def add_track(self,data):
        f = '[unmusic] logic.DB.add_track'
        if self.Success:
            if data:
                try:
                    self.dbc.execute ('insert into TRACKS values \
                                       (?,?,?,?,?,?,?,?,?)',data
                                     )
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def add_album(self,data):
        f = '[unmusic] logic.DB.add_album'
        if self.Success:
            if data:
                try:
                    self.dbc.execute ('insert into ALBUMS values \
                                       (NULL,?,?,?,?,?,?,?,?)',data
                                     )
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def create_tracks(self):
        f = '[unmusic] logic.DB.create_tracks'
        if self.Success:
            try:
                # 9 columns by now
                self.dbc.execute (
                    'create table if not exists TRACKS (\
                     ALBUMID   integer \
                    ,TITLE     text    \
                    ,NO        integer \
                    ,LYRICS    text    \
                    ,COMMENT   text    \
                    ,SEARCH    text    \
                    ,BITRATE   integer \
                    ,LENGTH    integer \
                    ,RATING    integer \
                                                       )'
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_albums(self):
        f = '[unmusic] logic.DB.create_albums'
        if self.Success:
            try:
                # 8 columns by now
                self.dbc.execute (
                    'create table if not exists ALBUMS (\
                     ALBUMID   integer primary key autoincrement \
                    ,ALBUM     text    \
                    ,ARTIST    text    \
                    ,YEAR      integer \
                    ,GENRE     text    \
                    ,COUNTRY   text    \
                    ,COMMENT   text    \
                    ,SEARCH    text    \
                    ,IMAGE     binary  \
                                                       )'
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def save(self):
        f = '[unmusic] logic.DB.save'
        if self.Success:
            mes = _('Save "{}"').format(self.path)
            sh.objs.get_mes(f,mes,True).show_info()
            try:
                self.db.commit()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def fail(self,func,error):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self.path,error)
        sh.objs.get_mes(func,mes).show_warning()
        ''' We need to quit as soon as possible, otherwise, folders
            will be obfuscated, but the info about them will not be
            stored in the DB!
        '''
        sys.exit()
    
    def close(self):
        f = '[unmusic] logic.DB.close'
        if self.Success:
            try:
                self.dbc.close()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def connect(self):
        f = '[unmusic] logic.DB.connect'
        if self.Success:
            try:
                self.db  = sqlite3.connect(self.path)
                self.dbc = self.db.cursor()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)



class Track:
    
    def __init__(self,file,Decypher=False):
        self.set_values()
        self.file     = file
        self.Success  = sh.lg.File(self.file).Success
        self.Decypher = Decypher
        self.load()
        self.set_info()
        self.decode()
        self.delete_unsupported()
        self.decypher()
    
    def decypher(self):
        f = '[unmusic] logic.Track.decypher'
        if self.Success:
            ''' Since we need to create a SEARCH field, for the purpose
                of solidity we decypher track title right here.
            '''
            if self.Decypher:
                self.title = objs.get_caesar().decypher(self.title)
                self.genre = objs.caesar.decypher(self.genre)
        else:
            sh.com.cancel(f)
    
    def delete_unsupported(self):
        f = '[unmusic] logic.Track.delete_unsupported'
        if self.Success:
            # Other fields should be processed before writing to DB
            self.title  = sh.lg.Text(self.title).delete_unsupported()
            self.lyrics = sh.lg.Text(self.lyrics).delete_unsupported()
        else:
            sh.com.cancel(f)
    
    def purge(self):
        f = '[unmusic] logic.Track.purge'
        if self.Success:
            if self.audio:
                try:
                    self.audio.delete()
                    self.audio.images = {}
                except Exception as e:
                    self.Success = False
                    mes = _('Third-party module has failed!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def save(self):
        ''' This is only needed if the file was changed by means of
            'phrydy', see, for example, 'self.purge'.
        '''
        f = '[unmusic] logic.Track.save'
        if self.Success:
            if self.audio:
                try:
                    self.audio.save()
                except Exception as e:
                    self.Success = False
                    mes = _('Third-party module has failed!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    # Fix Cyrillic tags
    def decode(self):
        f = '[unmusic] logic.Track.decode'
        if self.Success:
            # Other fields should be decoded before writing to DB
            self.title  = com.decode(self.title)
            self.lyrics = com.decode(self.lyrics)
        else:
            sh.com.cancel(f)
    
    def get_track_meta(self):
        f = '[unmusic] logic.Track.get_track_meta'
        if self.Success:
            search = [self.title,self.lyrics]
            search = ' '.join(search)
            search = sh.lg.Text(search).delete_duplicate_spaces()
            search = search.strip().lower()
            return (self.title,self.no,self.lyrics,search
                   ,self.bitrate,self.length
                   )
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success  = True
        self.audio   = None
        self.image   = None
        self.artist  = ''
        self.album   = ''
        self.title   = ''
        self.lyrics  = ''
        self.genre   = ''
        self.year    = 0
        self.bitrate = 0
        self.length  = 0
        self.no      = 1
    
    def show_summary(self):
        f = '[unmusic] logic.Track.show_summary'
        if self.Success:
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
            mes += _('Length: {} {} {} {}').format (minutes
                                                   ,_('min')
                                                   ,seconds
                                                   ,_('sec')
                                                   )
            mes +=  '\n'
            sh.objs.get_mes(f,mes).show_info()
        else:
            sh.com.cancel(f)
    
    def extract_title(self):
        f = '[unmusic] logic.Track.extract_title'
        if self.Success:
            title = sh.lg.Path(self.file).filename()
            if title:
                result = re.sub('^\d+[\.]{0,1}[\s]{0,1}','',title)
                if result:
                    return result
                else:
                    # If a title is just a digit + an extension.
                    return title
        else:
            sh.com.cancel(f)
    
    def set_info(self):
        f = '[unmusic] logic.Track.set_info'
        if self.Success:
            if self.audio:
                try:
                    artist = [self.audio.artist,self.audio.albumartist
                             ,self.audio.composer
                             ]
                    artist = [item for item in artist if item]
                    if artist:
                        self.artist = artist[0]
                    ''' Prevents from type mismatch (e.g., 'phrydy'
                        returns 'None' in case a year is not set).
                        If an input value is empty then we do not
                        overwrite a default value which should be of
                        a correct type. This does not work as
                        a separate procedure.
                    '''
                    if self.audio.album:
                        self.album = str(self.audio.album)
                    else:
                        dirname = sh.lg.Path(self.file).dirname()
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
                except Exception as e:
                    mes = _('Third-party module has failed!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[unmusic] logic.Track.load'
        if self.Success:
            if not self.audio:
                try:
                    self.audio = phrydy.MediaFile(self.file)
                except Exception as e:
                    mes = _('Third-party module has failed!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.get_mes(f,mes).show_warning()
            return self.audio
        else:
            sh.com.cancel(f)



class Walker:
    
    def __init__(self,path=''):
        if path:
            self.reset(path=path)
    
    def delete_empty(self):
        ''' Delete empty folders. Since 'sh.lg.Directory' instance is
            recreated each time, we can call this procedure at any time
            without the need to reset 'Walker'.
        '''
        f = '[unmusic] logic.Walker.delete_empty'
        self.get_dirs()
        if self.Success:
            if self.dirs:
                for folder in self.dirs:
                    sh.lg.Directory(folder).delete_empty()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def reset(self,path):
        self.set_values()
        self.path   = path
        self.idir    = sh.lg.Directory(self.path)
        self.Success = self.idir.Success
    
    def get_dirs(self):
        f = '[unmusic] logic.Walker.get_dirs'
        if self.Success:
            if not self.dirs:
                for dirpath, dirnames, filenames \
                in os.walk(self.idir.dir):
                    if not dirpath in self.dirs:
                        self.dirs.append(dirpath)
            return self.dirs
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success = True
        self.path    = ''
        self.dirs    = []



class Commands:
    
    def __init__(self):
        pass
    
    def sanitize(self,field):
        field = sh.lg.Text(field).delete_unsupported()
        field = sh.lg.Text(field).delete_duplicate_spaces()
        field = field.strip()
        field = self.decode(field)
        if not field:
            field = '?'
        return field
    
    def delete_album_trash(self,album):
        album = album.replace(' (@FLAC)','').replace(' (@VBR)','')
        album = album.replace(' (@vbr)','').replace(', @FLAC','')
        album = album.replace(',@FLAC','').replace(', @VBR','')
        album = album.replace(',@VBR','').replace(', @vbr','')
        album = album.replace(',@vbr','')
        album = re.sub(' \(@\d+\)','',album)
        album = re.sub(',[\s]{0,1}@\d+\)','',album)
        return album
    
    def decode(self,text):
        try:
            byted = bytes(text,'iso-8859-1')
            return byted.decode('cp1251')
        except:
            return text
    
    def decode_back(self,text):
        try:
            byted = bytes(text,'cp1251')
            return byted.decode('utf-8')
        except:
            return text



objs = Objects()
objs.get_default()
com = Commands()



if __name__ == '__main__':
    f = '[unmusic] logic.__main__'
    ibad = BadMusic()
    ibad.rates = [[1]]
    ibad.get_sizes()
    objs.get_db().close()
