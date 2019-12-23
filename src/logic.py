#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import io
import re
import phrydy
import sqlite3

import skl_shared.shared as sh

VERSION = '1.0'
# Derived from 'phrydy.mediafile.TYPES'
TYPES = ['.mp3','.aac','.alac','.ogg','.opus','.flac','.ape','.wv'
        ,'.mpc','.asf','.aiff','.dsf'
        ]
#note: Do not localize (being stored in DB)
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

import gettext
import skl_shared.gettext_windows
skl_shared.gettext_windows.setup_env()
gettext.install('unmusic','../resources/locale')


class BadMusic:
    
    def __init__(self):
        self.values()
        self.Success = objs.db().Success
    
    def values(self):
        self.Success = True
        self.vrates  = []
        self.vsizes  = []
        self.vdelete = []
    
    def delete(self):
        f = '[unmusic] logic.BadMusic.delete'
        if self.Success:
            import time
            time.sleep(3)
        else:
            sh.com.cancel(f)
    
    def report(self):
        f = '[unmusic] logic.BadMusic.report'
        if self.Success:
            if self.vrates and self.vsizes:
                iterable = []
                for i in range(len(self.vrates)):
                    if self.vsizes[i]:
                        size = sh.com.human_size (bsize     = self.vsizes[i]
                                                 ,LargeOnly = True
                                                 )
                    else:
                        size = _('N/A')
                    iterable.append(self.vrates[i]+[size])
                headers = ('ID','ALBUM','MIN','MAX','SIZE')
                mes = sh.FastTable (iterable  = iterable
                                   ,headers   = headers
                                   ,Transpose = True
                                   ,maxrow    = 70
                                   ).run()
                sh.com.fast_debug(mes)
            else:
                sh.com.empty(f)
    
    def sizes(self):
        f = '[unmusic] logic.BadMusic.sizes'
        if self.Success:
            if self.vrates:
                local_col = objs.default().ihome.add_share(_('local collection'))
                exter_col = objs._default.ihome.add_share(_('external collection'))
                mobil_col = objs._default.ihome.add_share(_('mobile collection'))
                mes = _('Local collection: {}').format(local_col)
                sh.objs.mes(f,mes,True).debug()
                mes = _('External collection: {}').format(exter_col)
                sh.objs.mes(f,mes,True).debug()
                mes = _('Mobile collection: {}').format(mobil_col)
                sh.objs.mes(f,mes,True).debug()
                for item in self.vrates:
                    albumid = str(item[0])
                    path1   = os.path.join(local_col,albumid)
                    path2   = os.path.join(exter_col,albumid)
                    path3   = os.path.join(mobil_col,albumid)
                    if os.path.exists(path1):
                        size1 = sh.Directory(path1).size()
                        self.vdelete.append(path1)
                    else:
                        size1 = 0
                    if os.path.exists(path2):
                        size2 = sh.Directory(path2).size()
                        self.vdelete.append(path2)
                    else:
                        size2 = 0
                    if os.path.exists(path3):
                        size3 = sh.Directory(path3).size()
                        self.vdelete.append(path3)
                    else:
                        size3 = 0
                    size = size1 + size2 + size3
                    self.vsizes.append(size)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def rates(self,limit=0,max_rate=4):
        f = '[unmusic] logic.BadMusic.rates'
        if self.Success:
            # ALBUMID (0), ALBUM (1), ARTIST (2), YEAR (3)
            albums = objs.db().albums(limit)
            if albums:
                old = objs._db.albumid
                for album in albums:
                    objs._db.albumid = album[0]
                    mes = _('Process album ID: {}')
                    mes = mes.format(objs._db.albumid)
                    sh.objs.mes(f,mes,True).debug()
                    rates = objs._db.rates()
                    if rates:
                        if min(rates) > 0 and max(rates) == max_rate:
                            album_title = [str(album[2]),str(album[3])
                                          ,str(album[1])
                                          ]
                            album_title = ' - '.join(album_title)
                            item = [album[0],album_title
                                   ,min(rates),max(rates)
                                   ]
                            self.vrates.append(item)
                    else:
                        sh.com.empty(f)
                objs._db.albumid = old
                return self.vrates
            else:
                sh.com.cancel(f)
        else:
            sh.com.cancel(f)



class Caesar:
    
    def __init__(self):
        self._seq1 = ('a','b','c','d','e','f','g','h','i','j','k','l'
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
        self._seq2 = ('C','D','f','d','e','i','R','t','n','g','u','b'
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
        assert len(self._seq1) == len(self._seq2)
    
    def cypher(self,text):
        lst = list(text)
        for i in range(len(lst)):
            try:
                ind = self._seq1.index(lst[i])
                lst[i] = self._seq2[ind]
            except ValueError:
                pass
        return ''.join(lst)
    
    def decypher(self,text):
        lst = list(text)
        for i in range(len(lst)):
            try:
                ind = self._seq2.index(lst[i])
                lst[i] = self._seq1[ind]
            except ValueError:
                pass
        return ''.join(lst)
        



class Play:
    
    def __init__(self):
        self.values()
        self.Success = objs.db().Success
    
    def call_player(self):
        f = '[unmusic] logic.Play.call_player'
        if self.Success:
            if self.playlist():
                sh.lg.Launch(self._playlist).default()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success   = True
        self._album    = ''
        self._playlist = ''
        self._audio    = []
        self._nos      = []
        self._titles   = []
        self._len      = []
    
    def album(self):
        f = '[unmusic] logic.Play.album'
        if self.Success:
            if not self._album:
                local_album = objs.default().ihome.add_share (_('local collection')
                                                             ,str(objs.db().albumid)
                                                             )
                exter_album = objs._default.ihome.add_share (_('external collection')
                                                            ,str(objs._db.albumid)
                                                            )
                local_exists = os.path.exists(local_album)
                exter_exists = os.path.exists(exter_album)
                if local_exists:
                    self._album = local_album
                elif exter_exists:
                    self._album = exter_album
        else:
            sh.com.cancel(f)
        return self._album
    
    def audio(self):
        f = '[unmusic] logic.Play.audio'
        if self.Success:
            if not self._audio:
                idir = Directory(self.album())
                idir.create_list()
                self.Success = idir.Success
                if idir._audio:
                    self._audio = idir._audio
        else:
            sh.com.cancel(f)
        return self._audio
    
    def available(self):
        f = '[unmusic] logic.Play.available'
        if self.Success:
            self.audio()
            if self._audio and self._nos and self._titles and self._len:
                result = []
                errors = []
                for no in self._nos:
                    try:
                        result.append(self._audio[no])
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
                            del self._titles[no]
                            del self._nos[no]
                            del self._len[no]
                        except IndexError:
                            pass
                    errors = [str(error) for error in errors]
                    mes = _('Tracks {} have not been found in "{}"!')
                    mes = mes.format(errors,self.album())
                    sh.objs.mes(f,mes).warning()
                if len(self._nos) == len(self._titles) == len(self._len):
                    pass
                else:
                    self.Success= False
                    sub = '{} = {} = {}'.format (len(self._nos)
                                                ,len(self._titles)
                                                ,len(self._len)
                                                )
                    mes = _('Condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.mes(f,mes).error()
                return result
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def playlist(self):
        f = '[unmusic] logic.Play.playlist'
        if self.Success:
            if not self._playlist:
                self._playlist = _('playlist') + '.m3u8'
                self._playlist = objs.default().ihome.add_share(self._playlist)
        else:
            sh.com.cancel(f)
        return self._playlist
    
    def gen_list(self):
        f = '[unmusic] logic.Play.gen_list'
        if self.Success:
            if self._nos:
                self.out = io.StringIO()
                result   = objs.db().get_album()
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
                files    = self.available()
                if files and self._nos:
                    self.out.write('#EXTM3U\n')
                    for i in range(len(files)):
                        self.out.write('#EXTINF:')
                        self.out.write(str(int(self._len[i])))
                        self.out.write(',')
                        self.out.write(header)
                        self.out.write(str(self._nos[i]+1))
                        self.out.write('. ')
                        ''' Replacing a hyphen will allow 'deadbeef'
                            to correctly distinguish between an album
                            and a title.
                        '''
                        self.out.write(self._titles[i].replace(' - ',': ').replace(' ~ ',': '))
                        self.out.write('\n')
                        self.out.write(files[i])
                        self.out.write('\n')
                else:
                    sh.com.empty(f)
                text = self.out.getvalue()
                self.out.close()
                if text:
                    sh.lg.WriteTextFile (file    = self.playlist()
                                        ,Rewrite = True
                                        ).write(text)
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def all_tracks(self):
        f = '[unmusic] logic.Play.all_tracks'
        if self.Success:
            tracks = objs.db().tracks()
            if tracks:
                self._titles = [track[0] for track in tracks]
                self._len    = [track[5] for track in tracks]
                # '-1' since count starts with 1 in DB and we need 0
                self._nos = [track[1] - 1 for track in tracks]
                self.gen_list()
                self.call_player()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def good_tracks(self,rating=8):
        f = '[unmusic] logic.Play.good_tracks'
        if self.Success:
            tracks = objs.db().good_tracks(rating)
            if tracks:
                self._titles = [track[0] for track in tracks]
                self._len    = [track[5] for track in tracks]
                # '-1' since count starts with 1 in DB and we need 0
                self._nos = [track[1] - 1 for track in tracks]
                self.gen_list()
                self.call_player()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)



class AlbumEditor:
    
    def __init__(self):
        self.Success = True
    
    def prev_rated(self,rating=0):
        f = '[unmusic] logic.AlbumEditor.prev_rated'
        if self.Success:
            result = objs.db().prev_rated(rating)
            if result:
                objs.db().albumid = result
                self.get_no()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def next_rated(self,rating=0):
        f = '[unmusic] logic.AlbumEditor.next_rated'
        if self.Success:
            result = objs.db().next_rated(rating)
            if result:
                objs.db().albumid = result
                self.get_no()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def mean_bitrate(self):
        f = '[unmusic] logic.AlbumEditor.mean_bitrate'
        if self.Success:
            mean = objs.db().get_bitrate()
            if mean:
                mean = [rating for rating in mean if rating]
                if mean:
                    # Return 'int' since we don't need 'float' here
                    return sum(mean) // len(mean)
                else:
                    return 0
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def mean_rating(self):
        f = '[unmusic] logic.AlbumEditor.mean_rating'
        if self.Success:
            mean = objs.db().get_rating()
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
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def get_no(self):
        f = '[unmusic] logic.AlbumEditor.get_no'
        if self.Success:
            objs.db().albumid = sh.lg.Input (title = f
                                            ,value = objs.db().albumid
                                            ).integer()
        else:
            sh.com.cancel(f)
        return objs.db().albumid
    
    def get_min(self):
        f = '[unmusic] logic.AlbumEditor.get_min'
        if self.Success:
            return sh.lg.Input (title = f
                               ,value = objs.db().min_id()
                               ).integer()
        else:
            sh.com.cancel(f)
            return 0
    
    def get_max(self):
        f = '[unmusic] logic.AlbumEditor.get_max'
        if self.Success:
            _max = objs.db().max_id()
            if isinstance(_max,int):
                return _max
            else:
                mes = _('The database is empty. You need to fill it first.')
                sh.objs.mes(f,mes).warning()
                return 0
        else:
            sh.com.cancel(f)
            return 0
    
    def inc(self):
        f = '[unmusic] logic.AlbumEditor.inc'
        if self.Success:
            if self.get_no() == self.get_max():
                objs.db().albumid = self.get_min()
            else:
                objs.db().albumid = objs.db().next_id()
                self.get_no()
        else:
            sh.com.cancel(f)
    
    def dec(self):
        f = '[unmusic] logic.AlbumEditor.dec'
        if self.Success:
            if self.get_no() == self.get_min():
                objs.db().albumid = self.get_max()
            else:
                objs.db().albumid = objs.db().prev_id()
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
            add += ' where ALBUMID=%d;commit;' % objs.db().albumid
            return add



class Directory:
    
    def __init__(self,path):
        self.values()
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
            max_len = len(self._audio)
            max_len = len(str(max_len))
            for i in range(len(self._audio)):
                file     = self._audio[i]
                no       = self._set_no(i,max_len)
                basename = no + sh.lg.Path(file).extension().lower()
                dest     = os.path.join (self._target
                                        ,basename
                                        )
                success.append(sh.lg.File(file=file,dest=dest).move())
            self.Success = not (False in success or None in success)
        else:
            sh.com.cancel(f)
    
    def purge(self):
        f = '[unmusic] logic.Directory.purge'
        if self.Success:
            if self._tracks:
                mes = _('Purge tracks')
                sh.objs.mes(f,mes,True).info()
                for track in self._tracks:
                    track.purge()
                    track.save()
                    if not track.Success:
                        self.Success = False
                        break
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def create_target(self):
        f = '[unmusic] logic.Directory.create_target'
        if self.Success:
            if objs.db().albumid:
                self._target = objs.default().ihome.add_share (_('processed')
                                                              ,str(objs._db.albumid)
                                                              )
                self.Success = sh.lg.Path(self._target).create()
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def reset(self,path):
        self.values()
        self._path   = path
        self.idir    = sh.lg.Directory(self._path)
        self.Success = self.idir.Success
        if self.Success and '(decypher)' in self._path:
            self.Decypher = True
        
    def get_rating(self):
        f = '[unmusic] logic.Directory.get_rating'
        if self.Success:
            match = re.search(r'\(rating (\d+)\)',self._path)
            if match:
                try:
                    rating = match.group(1)
                    if rating.isdigit():
                        self._rating = int(rating)
                except IndexError:
                    pass
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.get_rating()
        self.create_list()
        self.tracks()
        if self._tracks:
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
                basename = sh.lg.Path(self._path).basename()
                basename = objs.caesar().decypher(basename)
                if basename:
                    if basename.count(' - ') == 2:
                        return basename.split(' - ')
                    else:
                        mes = _('Wrong input data: "{}"!')
                        mes = mes.format(basename)
                        sh.objs.mes(f,mes,True).warning()
                else:
                    sh.com.empty(f)
            else:
                sh.com.lazy(f)
        else:
            sh.com.cancel(f)
    
    def add_album_meta(self):
        f = '[unmusic] logic.Directory.add_album_meta'
        if self.Success:
            if self._tracks:
                ''' If a track could not be processed, empty tags will
                    be returned, which, when written to DB, can cause
                    confusion. Here we check that the track was
                    processed successfully.
                '''
                if self._tracks[0]._audio:
                    album  = self._tracks[0]._album
                    artist = self._tracks[0]._artist
                    year   = self._tracks[0]._year
                    genre  = self._tracks[0]._genre
                    image  = self._tracks[0]._image
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
                            sh.objs.mes(f,mes).error()
                    album  = com.sane(album)
                    album  = com.album_trash(album)
                    artist = com.sane(artist)
                    if str(year).isdigit():
                        year = int(year)
                    else:
                        # Prevent from storing an incorrect value
                        year = 0
                    genre = com.sane(genre)
                    
                    search = [album,artist,str(year),genre]
                    search = ' '.join(search)
                    search = search.lower()
                    
                    objs.db().add_album ([album,artist,year,genre,'',''
                                         ,search,image
                                         ]
                                        )
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def _add_tracks_meta(self,albumid):
        f = '[unmusic] logic.Directory._add_tracks_meta'
        for track in self._tracks:
            data = track.track_meta()
            ''' If a track could not be processed, empty tags will be
                returned, which, when written to DB, can cause
                confusion. Here we check that the track was processed
                successfully.
            '''
            if track._audio and data:
                objs.db().albumid = albumid
                objs._db.add_track ([albumid,data[0],data[1],data[2]
                                    ,'',data[3],data[4],data[5]
                                    ,self._rating
                                    ]
                                   )
            else:
                sh.com.empty(f)
    
    def save_meta(self):
        f = '[unmusic] logic.Directory.save_meta'
        if self.Success:
            if self._tracks:
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
                albumid = objs._db.max_id()
                if albumid:
                    self._add_tracks_meta(albumid)
                    mes = _('Album {}: {} tracks.')
                    mes = mes.format(albumid,len(self._tracks))
                    sh.objs.mes(f,mes,True).info()
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success  = True
        self.Decypher = False
        self.idir     = None
        self._path    = ''
        self._target  = ''
        self._rating  = 0
        self._files   = []
        self._audio   = []
        self._tracks  = []
    
    def create_list(self):
        f = '[unmusic] logic.Directory.create_list'
        if self.Success:
            if not self._files:
                if self.idir:
                    self._files = self.idir.files()
                    for file in self._files:
                        if sh.lg.Path(file).extension().lower() \
                        in TYPES:
                            self._audio.append(file)
                else:
                    sh.com.empty(f)
            return self._files
        else:
            sh.com.cancel(f)
    
    def renumber_tracks(self):
        ''' We use track NO field instead of an autoincrement, so we
            must keep these fields unique within the same album.
        '''
        f = '[unmusic] logic.Directory.renumber_tracks'
        if self.Success:
            nos = [i + 1 for i in range(len(self._tracks))]
            count = 0
            for i in range(len(self._tracks)):
                if self._tracks[i]._no != nos[i]:
                    count += 1
                    self._tracks[i]._no = nos[i]
            if count:
                mes = _('{}/{} tracks have been renumbered.')
                mes = mes.format(count,len(self._tracks))
                sh.objs.mes(f,mes,True).warning()
        else:
            sh.com.cancel(f)
    
    def tracks(self):
        f = '[unmusic] logic.Directory.tracks'
        if self.Success:
            if not self._tracks:
                if self._audio:
                    for file in self._audio:
                        self._tracks.append (Track (file     = file
                                                   ,Decypher = self.Decypher
                                                   )
                                            )
                else:
                    mes = _('Folder "{}" has no audio files.')
                    mes = mes.format(self._path)
                    sh.objs.mes(f,mes,True).info()
            return self._tracks
        else:
            sh.com.cancel(f)



class DefaultConfig:
    
    def __init__(self):
        self.values()
        self.ihome   = sh.lg.Home(app_name='unmusic')
        self.Success = self.ihome.create_conf()
    
    def run(self):
        self.db()
    
    def values(self):
        self._fdb = ''
    
    def db(self):
        f = '[unmusic] logic.DefaultConfig.db'
        if self.Success:
            self._fdb = self.ihome.add_config('unmusic.db')
            if self._fdb:
                if os.path.exists(self._fdb):
                    self.Success = sh.lg.File(file=self._fdb).Success
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)



class Objects:
    
    def __init__(self):
        self._default = self._db = self._caesar = None
        
    def caesar(self):
        if self._caesar is None:
            self._caesar = Caesar()
        return self._caesar
    
    def db(self):
        f = '[unmusic] logic.Objects.db'
        if self._db is None:
            path = self.default()._fdb
            if self._default.Success:
                self._db = DB(path=path)
            else:
                mes = _('Wrong input data!')
                sh.objs.mes(f,mes,True).warning()
                self._db = DB()
        return self._db
    
    def default(self):
        if self._default is None:
            self._default = DefaultConfig()
            self._default.run()
        return self._default



class DB:
    
    def __init__(self,path):
        self.Success = True
        self.albumid = 1
        self._path   = path
        self.connect()
        self.create_albums()
        self.create_tracks()
    
    def albums(self,limit=0):
        f = '[unmusic] logic.DB.albums'
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
    
    def rates(self):
        ''' When operating on entire albums (e.g., deleting bad music),
            we need to know minimum and maximum ratings
            (e.g., 0 < album rate < 5 for ALL tracks of bad albums).
        '''
        f = '[unmusic] logic.DB.rates'
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
    
    def prev_rated(self,rating=0):
        f = '[unmusic] logic.DB.prev_rated'
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
    
    def next_rated(self,rating=0):
        f = '[unmusic] logic.DB.next_rated'
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
    
    def brief(self,ids):
        f = '[unmusic] logic.DB.brief'
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
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def unknown_genre(self,limit=0):
        f = '[unmusic] logic.DB.unknown_genre'
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
    
    def rated(self,rating=0,limit=0):
        f = '[unmusic] logic.DB.unrated'
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
    
    def good_tracks(self,rating=8):
        f = '[unmusic] logic.DB.good_tracks'
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
                self.dbc.execute ('select ALBUMID \
                                   from   ALBUMS \
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
                    sh.objs.mes(f,mes).error()
            else:
                sh.com.empty(f)
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
                return self.dbc.fetchall()
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
                    sh.objs.mes(f,mes).error()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def tracks(self):
        f = '[unmusic] logic.DB.tracks'
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
    
    def search_track(self,search,limit=50):
        f = '[unmusic] logic.DB.search_track'
        if self.Success:
            if search:
                search = '%' + search.lower() + '%'
                try:
                    self.dbc.execute ('select   ALBUMID,TITLE,NO,LYRICS\
                                               ,COMMENT,BITRATE,LENGTH\
                                               ,RATING from TRACKS \
                                       where    SEARCH like ? \
                                       order by ALBUMID,NO limit ?'
                                      ,(search,limit,)
                                     )
                    return self.dbc.fetchall()
                except Exception as e:
                    self.fail(f,e)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def next_album(self,search):
        f = '[unmusic] logic.DB.next_album'
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
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def prev_album(self,search):
        f = '[unmusic] logic.DB.prev_album'
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
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def prev_id(self):
        f = '[unmusic] logic.DB.prev_id'
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
    
    def next_id(self):
        f = '[unmusic] logic.DB.next_id'
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
    
    def min_id(self):
        f = '[unmusic] logic.DB.min_id'
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
    
    def max_id(self):
        f = '[unmusic] logic.DB.max_id'
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
                sh.com.empty(f)
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
            mes = _('Save "{}"').format(self._path)
            sh.objs.mes(f,mes,True).info()
            try:
                self.db.commit()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def fail(self,func,error):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self._path,error)
        sh.objs.mes(func,mes).warning()
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
                self.db  = sqlite3.connect(self._path)
                self.dbc = self.db.cursor()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)



class Track:
    
    def __init__(self,file,Decypher=False):
        self.values()
        self.file     = file
        self.Success  = sh.lg.File(self.file).Success
        self.Decypher = Decypher
        self.load()
        self.info()
        self.decode()
        self.unsupported()
        self.decypher()
    
    def decypher(self):
        f = '[unmusic] logic.Track.decypher'
        if self.Success:
            ''' Since we need to create a SEARCH field, for the purpose
                of solidity we decypher track title right here.
            '''
            if self.Decypher:
                self._title = objs.caesar().decypher(self._title)
                self._genre = objs._caesar.decypher(self._genre)
        else:
            sh.com.cancel(f)
    
    def unsupported(self):
        f = '[unmusic] logic.Track.unsupported'
        if self.Success:
            # Other fields should be processed before writing to DB
            self._title  = sh.lg.Text(self._title).delete_unsupported()
            self._lyrics = sh.lg.Text(self._lyrics).delete_unsupported()
        else:
            sh.com.cancel(f)
    
    def purge(self):
        f = '[unmusic] logic.Track.purge'
        if self.Success:
            if self._audio:
                try:
                    self._audio.delete()
                    self._audio.images = {}
                except Exception as e:
                    self.Success = False
                    mes = _('Third-party module has failed!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.mes(f,mes).warning()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def save(self):
        ''' This is only needed if the file was changed by means of
            'phrydy', see, for example, 'self.purge'.
        '''
        f = '[unmusic] logic.Track.save'
        if self.Success:
            if self._audio:
                try:
                    self._audio.save()
                except Exception as e:
                    self.Success = False
                    mes = _('Third-party module has failed!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.mes(f,mes).warning()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    # Fix Cyrillic tags
    def decode(self):
        f = '[unmusic] logic.Track.decode'
        if self.Success:
            # Other fields should be decoded before writing to DB
            self._title  = com.decode(self._title)
            self._lyrics = com.decode(self._lyrics)
        else:
            sh.com.cancel(f)
    
    def track_meta(self):
        f = '[unmusic] logic.Track.track_meta'
        if self.Success:
            search = [self._title,self._lyrics]
            search = ' '.join(search)
            search = sh.lg.Text(search).delete_duplicate_spaces()
            search = search.strip().lower()
            return (self._title,self._no,self._lyrics,search
                   ,self._bitrate,self._length
                   )
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success  = True
        self._audio   = None
        self._image   = None
        self._artist  = ''
        self._album   = ''
        self._title   = ''
        self._lyrics  = ''
        self._genre   = ''
        self._year    = 0
        self._bitrate = 0
        self._length  = 0
        self._no      = 1
    
    def summary(self):
        f = '[unmusic] logic.Track.summary'
        if self.Success:
            mes = _('Artist: {}').format(self._artist)
            mes += '\n'
            mes += _('Album: {}').format(self._album)
            mes += '\n'
            mes += _('Genre: {}').format(self._genre)
            mes += '\n'
            mes += _('Year: {}').format(self._year)
            mes += '\n'
            mes += _('Track #: {}').format(self._no)
            mes += '\n'
            mes += _('Title: {}').format(self._title)
            mes += '\n'
            mes += _('Lyrics: {}').format(self._lyrics)
            if self._length:
                minutes = self._length // 60
                seconds = self._length - minutes * 60
            else:
                minutes = seconds = 0
            mes += _('Length: {} {} {} {}').format (minutes
                                                   ,_('min')
                                                   ,seconds
                                                   ,_('sec')
                                                   )
            mes +=  '\n'
            sh.objs.mes(f,mes).info()
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
    
    def info(self):
        f = '[unmusic] logic.Track.info'
        if self.Success:
            if self._audio:
                try:
                    artist = [self._audio.artist,self._audio.albumartist
                             ,self._audio.composer
                             ]
                    artist = [item for item in artist if item]
                    if artist:
                        self._artist = artist[0]
                    ''' Prevents from type mismatch (e.g., 'phrydy'
                        returns 'None' in case a year is not set).
                        If an input value is empty then we do not
                        overwrite a default value which should be of
                        a correct type. This does not work as
                        a separate procedure.
                    '''
                    if self._audio.album:
                        self._album = str(self._audio.album)
                    else:
                        dirname = sh.lg.Path(self.file).dirname()
                        dirname = sh.lg.Path(dirname).basename()
                        self._album = '[[' + dirname + ']]'
                    if self._audio.genre:
                        self._genre = str(self._audio.genre)
                    if self._audio.year:
                        self._year = sh.lg.Input (title = f
                                                 ,value = self._audio.year
                                                 ).integer()
                    if self._audio.title:
                        self._title = str(self._audio.title)
                    else:
                        extracted = self.extract_title()
                        if extracted:
                            self._title = extracted
                    if self._audio.bitrate:
                        self._bitrate = self._audio.bitrate
                    if self._audio.length:
                        self._length = self._audio.length
                    if str(self._audio.track).isdigit():
                        self._no = self._audio.track
                    if self._audio.lyrics:
                        self._lyrics = str(self._audio.lyrics)
                    if self._audio.images:
                        self._image = self._audio.images[0].data
                except Exception as e:
                    mes = _('Third-party module has failed!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.mes(f,mes).warning()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[unmusic] logic.Track.load'
        if self.Success:
            if not self._audio:
                try:
                    self._audio = phrydy.MediaFile(self.file)
                except Exception as e:
                    mes = _('Third-party module has failed!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.mes(f,mes).warning()
            return self._audio
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
        self.dirs()
        if self.Success:
            if self._dirs:
                for folder in self._dirs:
                    sh.lg.Directory(folder).delete_empty()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def reset(self,path):
        self.values()
        self._path   = path
        self.idir    = sh.lg.Directory(self._path)
        self.Success = self.idir.Success
    
    def dirs(self):
        f = '[unmusic] logic.Walker.dirs'
        if self.Success:
            if not self._dirs:
                for dirpath, dirnames, filenames \
                in os.walk(self.idir.dir):
                    if not dirpath in self._dirs:
                        self._dirs.append(dirpath)
            return self._dirs
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success = True
        self._path   = ''
        self._dirs   = []



class Commands:
    
    def __init__(self):
        pass
    
    def sane(self,field):
        field = sh.lg.Text(field).delete_unsupported()
        field = sh.lg.Text(field).delete_duplicate_spaces()
        field = field.strip()
        field = self.decode(field)
        if not field:
            field = '?'
        return field
    
    def album_trash(self,album):
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
objs.default()
com = Commands()



if __name__ == '__main__':
    f = '[unmusic] logic.__main__'
    ibad = BadMusic()
    ibad.vrates = [[1]]
    ibad.sizes()
    objs.db().close()
