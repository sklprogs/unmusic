#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sqlite3
from skl_shared.localize import _
import skl_shared.shared as sh
import skl_shared.image.controller as im
import logic as lg
import gui as gi


class DeleteBad:
    
    def __init__(self):
        self.Success = True
        # Generated with tests.BadRating.report
        self.ids = ['593', '596', '597', '600', '609', '611', '613', '623', '642', '645', '651', '657', '659', '663', '664', '669', '685', '687', '691', '705', '712', '721', '723', '726', '735', '742', '743', '749', '751', '766', '774', '781', '786', '807', '820', '821', '828', '841', '852', '853', '854', '862', '866', '868', '872', '890', '901', '903', '904', '907', '912', '922', '933', '934', '950', '963', '968', '969', '978', '979', '994', '995', '997', '999', '1000', '1003', '1005', '1006', '1008', '1010', '1014', '1015', '1016', '1023', '1042', '1058', '1060', '1064', '1068', '1069', '1072', '1074', '1075', '1080', '1081', '1082', '1086', '1091', '1093', '1095', '1096', '1099', '1106', '1107', '1123', '1126', '1132', '1134', '1141', '1144', '1145', '1150', '1151', '1156', '1159', '1163', '1166', '1169', '1170', '1175', '1192', '1195', '1196', '1198', '1212', '1221', '1222', '1226', '1232', '1233', '1235', '1236', '1237', '1240', '1248', '1251', '1254', '1256', '1263', '1271', '1285', '1290', '1298', '1300', '1302', '1304', '1307', '1308', '1311', '1314', '1323', '1324', '1325', '1329', '1337', '1339', '1344', '1345', '1353', '1357', '1358', '1361', '1367', '1371', '1375', '1388', '1392', '1395', '1406', '1422', '1423', '1428', '1432', '1436', '1437', '1445', '1446', '1447', '1448', '1449', '1450', '1452', '1460', '1467', '1468', '1489', '1496', '1506', '1510', '1513', '1534', '1535', '1536', '1542', '1546', '1547', '1557', '1560', '1562', '1563', '1570', '1573', '1574', '1577', '1583', '1589', '1602', '1609', '1614', '1621', '1631', '1634', '1642', '1647', '1651', '1662', '1666', '1669', '1672', '1673', '1677', '1681', '1688', '1703', '1711', '1712', '1718', '1719', '1726', '1735', '1736', '1749', '1751', '1757', '1772', '1775', '1782', '1788', '1791', '1792', '1793', '1798', '1801', '1806', '1807', '1824', '1830', '1832', '1844', '1851', '1857', '1859', '1860', '1863', '1870', '1874', '1875', '1881', '1882', '1883', '1891', '1894', '1905', '1906', '1908', '1910', '1925', '1932', '1937', '1938', '1943', '1949', '1955', '1963', '1971', '1973', '1981', '1993', '1996', '1998', '2008', '2019', '2020', '2024', '2025', '2030', '2039', '2040', '2044', '2049', '2051', '2065', '2070', '2075', '2076', '2081', '2089', '2093', '2094', '2095', '2100', '2101', '2121', '2122', '2127', '2128', '2132', '2135', '2145', '2147', '2155', '2167', '2172', '2174', '2175', '2177', '2180', '2183', '2187', '5015', '5954', '6006', '7044', '7359', '7364', '7366', '7368', '7375', '7381', '7383', '7385', '7390', '7391', '7401', '7406', '7411', '7415', '7416', '7420', '7422', '7431', '7439', '7441', '7442', '7445', '7454', '7468', '7469', '7471', '7479', '7480', '7481', '7487', '7490', '7494', '7498', '7499', '7501', '7516', '7525', '7530', '7532', '7533', '7535', '7541', '7542', '7545', '7553', '7554', '7559', '7565', '7568', '7571', '7574', '7578', '7582', '7593', '7596', '7603', '7610', '7612', '7618', '7620', '7622', '7623', '7626', '7635', '7645', '7651', '7660', '7662', '7669', '7675', '7677', '7688', '7692', '7693', '7694', '7702', '7705', '7709', '7718', '7721', '7725', '7726', '7730', '7735', '7738', '7746', '7749', '7766', '7773', '7774', '7776', '7777', '7779', '7781', '7783', '7795', '7803', '7810', '7822', '7830', '7840', '7842', '7847', '7848', '7851', '7852', '7854', '7857', '7862', '7865', '7866', '7870', '7873', '7874', '7884', '7886', '7894', '7896', '7897', '7899', '7900', '7901', '9093', '9132', '10101']
        self.del_dirs = []
    
    def delete(self):
        f = '[unmusic] utils.DeleteBad.delete'
        if not self.Success:
            sh.com.cancel(f)
            return
        gi.objs.get_progress().set_text(_('Delete folders'))
        gi.objs.progress.show()
        count = 0
        for i in range(len(self.del_dirs)):
            shown_path = sh.Text(self.del_dirs[i]).shorten (max_len = 40
                                                           ,FromEnd = True
                                                           ,ShowGap = True
                                                           )
            mes = _('Delete "{}"').format(shown_path)
            gi.objs.progress.set_text(mes)
            gi.objs.progress.update(i,len(self.del_dirs))
            # Avoid GUI freezing
            sh.objs.get_root().update()
            if sh.Directory(self.del_dirs[i]).delete():
                count += 1
        gi.objs.progress.close()
        mes = _('{}/{} folders have been deleted.')
        mes = mes.format(count,len(self.del_dirs))
        sh.objs.get_mes(f,mes).show_info()
    
    def get_sizes(self):
        f = '[unmusic] utils.DeleteBad.get_sizes'
        if not self.Success:
            sh.com.cancel(f)
            return
        ihome = sh.Home('unmusic')
        local = lg.objs.get_default().ihome.add_share(_('local collection'))
        local = os.path.realpath(local)
        external = lg.objs.default.ihome.add_share(_('external collection'))
        external = os.path.realpath(external)
        mobile = lg.objs.default.ihome.add_share(_('mobile collection'))
        mobile = os.path.realpath(mobile)
        total_size = 0
        local_size = 0
        external_size = 0
        mobile_size = 0
        gi.objs.get_progress().set_text(_('Calculate space to be freed'))
        gi.objs.progress.show()
        for i in range(len(self.ids)):
            gi.objs.progress.update(i,len(self.ids))
            path = os.path.join(local,self.ids[i])
            if os.path.exists(path):
                local_size += sh.Directory(path).get_size()
                self.del_dirs.append(path)
            path = os.path.join(external,self.ids[i])
            if os.path.exists(path):
                external_size += sh.Directory(path).get_size()
                self.del_dirs.append(path)
            path = os.path.join(mobile,self.ids[i])
            if os.path.exists(path):
                mobile_size += sh.Directory(path).get_size()
                self.del_dirs.append(path)
        gi.objs.progress.close()
        total_size = sh.com.get_human_size(total_size,True)
        local_size = sh.com.get_human_size(local_size,True)
        external_size = sh.com.get_human_size(external_size,True)
        mobile_size = sh.com.get_human_size(mobile_size,True)
        mes = []
        sub = _('Space to be freed:')
        mes.append(sub)
        sub = _('in total: {}').format(total_size)
        mes.append(sub)
        sub = _('external collection: {}').format(external_size)
        mes.append(sub)
        sub = _('local collection: {}').format(local_size)
        mes.append(sub)
        sub = _('mobile collection: {}').format(mobile_size)
        mes.append(sub)
        mes.append('')
        sub = _('Do you really want to continue?')
        mes.append(sub)
        self.Success = sh.objs.get_mes(f,'\n'.join(mes)).show_question()
        if not self.Success:
            mes = _('Operation has been canceled by the user.')
            sh.objs.get_mes(f,mes,True).show_info()
    
    def run(self):
        self.get_sizes()
        self.delete()



class Image:
    
    def __init__(self):
        self.dir = sh.Home('unmusic').add_share(_('Images'))
        self.Success = sh.Path(self.dir).create()
        self.path = ''
        self.albumid = 0
        self.bytes = None
        self.Present = False
        self.Processed = False
        self.Skipped = False
    
    def save(self):
        f = '[unmusic] utils.Image.save'
        if self.Success:
            if self.path:
                if os.path.exists(self.path):
                    mes = _('File "{}" already exists.')
                    mes = mes.format(self.path)
                    sh.objs.get_mes(f,mes,True).show_debug()
                    self.Present = True
                elif self.bytes:
                    mes = _('Save "{}"').format(self.path)
                    sh.objs.get_mes(f,mes,True).show_info()
                    iimage = im.Image()
                    iimage.bytes_ = self.bytes
                    iimage.get_loader()
                    iimage.convert2rgb()
                    iimage.save(self.path,'JPEG')
                    self.Processed = iimage.Success
                else:
                    mes = _('Album {} has no cover!')
                    mes = mes.format(self.albumid)
                    sh.objs.get_mes(f,mes,True).show_debug()
                    self.Skipped = True
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_path(self):
        f = '[unmusic] utils.Image.set_path'
        if self.Success:
            name = str(self.albumid)
            if name:
                name += '.jpg'
                self.path = os.path.join(self.dir,name)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def reset(self,albumid,bytes_):
        self.path = ''
        self.albumid = albumid
        self.bytes = bytes_
        self.Present = False
        self.Processed = False
        self.Skipped = False
    
    def run(self):
        self.set_path()
        self.save()



class Commands:
    
    def __init__(self):
        self.path = '/home/pete/.config/unmusic/unmusic.db'
        self.clone = '/tmp/unmusic.db'
    
    def extract_images(self):
        f = '[unmusic] utils.Commands.extract_images'
        sh.GUI_MES = False
        idb = DB(self.path,self.clone)
        idb.connect()
        data = idb.fetch_images()
        if data:
            errors = 0
            present = 0
            processed = 0
            skipped = 0
            iimage = Image()
            for row in data:
                iimage.reset(row[0],row[1])
                iimage.run()
                if iimage.Present:
                    present += 1
                elif iimage.Skipped:
                    skipped += 1
                elif iimage.Processed:
                    processed += 1
                else:
                    errors += 1
            mes = _('Files in total: {}, processed: {}, already existing: {}, skipped: {}, errors: {}')
            mes = mes.format(len(data),processed,present,skipped,errors)
            sh.objs.get_mes(f,mes,True).show_info()
        else:
            sh.com.rep_empty(f)
        idb.close()
    
    def alter(self):
        if os.path.exists(self.clone):
            sh.File(self.clone).delete()
        # Alter DB and add/remove some columns
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connect()
        idb.connectw()
        idb.fetch()
        idb.create_tables()
        idb.fill()
        idb.savew()
        idb.close()
        idb.closew()
        
    def is_camel_case(self,title):
        words = title.split(' ')
        for word in words:
            if word != word.upper() and len(word) > 1 \
            and word[0].isalpha():
                for sym in word[1:]:
                    if sym in 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЪЬЭЮЯ':
                        return True
    
    def show_cyphered(self):
        f = '[unmusic] utils.Commands.show_cyphered'
        if lg.objs.get_db().Success:
            titles = []
            #query = 'select TITLE from TRACKS order by ALBUMID'
            query = 'select ALBUM from ALBUMS order by ALBUM'
            try:
                lg.objs.db.dbc.execute(query)
                titles = lg.objs.db.dbc.fetchall()
                if titles:
                    titles = [item[0] for item in titles]
            except Exception as e:
                mes = _('Operation has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.get_mes(f,mes).show_warning()
            result = [title for title in titles \
                      if self.is_camel_case(title)
                     ]
            print('\n'.join(result))
            print(len(result))
        else:
            sh.com.cancel(f)



class DB:
    
    def __init__(self,path,clone):
        self.albums = ()
        self.tracks = ()
        self.path = path
        self.clone = clone
        self.Success = self.clone and sh.File(self.path).Success
    
    def fetch_images(self):
        f = '[unmusic] utils.DB.fetch_images'
        if self.Success:
            mes = _('Fetch data')
            sh.objs.get_mes(f,mes,True).show_debug()
            query = 'select ALBUMID,IMAGE from ALBUMS order by ALBUMID'
            try:
                self.dbc.execute(query)
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_tables(self):
        self.create_albums()
        self.create_tracks()
    
    def fetch(self):
        self.fetch_albums()
        self.fetch_tracks()
    
    def fail(self,f,e):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self.path,e)
        sh.objs.get_mes(f,mes).show_warning()
    
    def fail_clone(self,f,e):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self.clone,e)
        sh.objs.get_mes(f,mes).show_warning()
    
    def savew(self):
        f = '[unmusic] utils.DB.savew'
        if self.Success:
            try:
                self.dbw.commit()
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
        
    def connect(self):
        f = '[unmusic] utils.DB.connect'
        if self.Success:
            try:
                self.db = sqlite3.connect(self.path)
                self.dbc = self.db.cursor()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def connectw(self):
        f = '[unmusic] utils.DB.connectw'
        if self.Success:
            try:
                self.dbw = sqlite3.connect(self.clone)
                self.dbcw = self.dbw.cursor()
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def fetch_albums(self):
        f = '[unmusic] utils.DB.fetch_albums'
        if self.Success:
            mes = _('Fetch data from {}').format('ALBUMS')
            sh.objs.get_mes(f,mes,True).show_info()
            # 8 columns to fetch
            query = 'select ALBUMID,ALBUM,ARTIST,YEAR,GENRE,COUNTRY \
                    ,COMMENT,SEARCH from ALBUMS'
            try:
                self.dbc.execute(query)
                self.albums = self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def fetch_tracks(self):
        f = '[unmusic] utils.DB.fetch_tracks'
        if self.Success:
            mes = _('Fetch data from {}').format('TRACKS')
            sh.objs.get_mes(f,mes,True).show_info()
            # 9 columns to fetch
            query = 'select ALBUMID,TITLE,NO,LYRICS,COMMENT,SEARCH \
                    ,BITRATE,LENGTH,RATING from TRACKS'
            try:
                self.dbc.execute(query)
                self.tracks = self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_albums(self):
        f = '[unmusic] utils.DB.create_albums'
        if self.Success:
            # 9 columns by now
            query = 'create table ALBUMS (\
                     ALBUMID integer primary key autoincrement \
                    ,ALBUM   text    \
                    ,ARTIST  text    \
                    ,YEAR    integer \
                    ,GENRE   text    \
                    ,COUNTRY text    \
                    ,COMMENT text    \
                    ,SEARCH  text    \
                    ,RATING  integer \
                                         )'
            self._create_table(f,query)
        else:
            sh.com.cancel(f)
    
    def _create_table(self,f,query):
        try:
            self.dbcw.execute(query)
        except Exception as e:
            self.fail_clone(f,e)
    
    def create_tracks(self):
        f = '[unmusic] utils.DB.create_tracks'
        if self.Success:
            # 9 columns by now
            query = 'create table if not exists TRACKS (\
                     ALBUMID integer \
                    ,TITLE   text    \
                    ,NO      integer \
                    ,LYRICS  text    \
                    ,COMMENT text    \
                    ,SEARCH  text    \
                    ,BITRATE integer \
                    ,LENGTH  integer \
                    ,RATING  integer \
                                                       )'
            self._create_table(f,query)
        else:
            sh.com.cancel(f)
    
    def _get_mean(self,ratings):
        if 0 in ratings:
            return 0
        else:
            return round(sum(ratings)/len(ratings))
    
    def _fill_albums(self):
        f = '[unmusic] utils.DB._fill_albums'
        query = 'insert into ALBUMS values (?,?,?,?,?,?,?,?,?)'
        for row in self.albums:
            lg.objs.get_db().albumid = row[0]
            ratings = lg.objs.db.get_rating()
            if ratings:
                rating = self._get_mean(ratings)
            else:
                rating = 0
                sh.com.rep_empty(f)
            mes = _('Album ID: {}. Rating: {}').format(row[0],rating)
            sh.objs.get_mes(f,mes,True).show_debug()
            row += (rating,)
            self._fill_row(f,query,row)
    
    def _fill_tracks(self):
        f = '[unmusic] utils.DB._fill_tracks'
        query = 'insert into TRACKS values (?,?,?,?,?,?,?,?,?)'
        for row in self.tracks:
            self._fill_row(f,query,row)
    
    def _fill_row(self,f,query,row):
        try:
            self.dbcw.execute(query,row)
        except Exception as e:
            self.Success = False
            self.fail(f,e)
            return
    
    def fill(self):
        f = '[unmusic] utils.DB.fill'
        if self.Success:
            if self.albums and self.tracks:
                mes = _('Copy "{}" to "{}"').format (self.path
                                                    ,self.clone
                                                    )
                sh.objs.get_mes(f,mes,True).show_info()
                self._fill_albums()
                self._fill_tracks()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
                          
    def close(self):
        f = '[unmusic] utils.DB.close'
        if self.Success:
            try:
                self.dbc.close()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def closew(self):
        f = '[unmusic] utils.DB.closew'
        if self.Success:
            try:
                self.dbcw.close()
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)


com = Commands()


if __name__ == '__main__':
    f = '[unmusic] utils.__main__'
    sh.com.start()
    #com.alter()
    DeleteBad().run()
    mes = _('Goodbye!')
    sh.objs.get_mes(f,mes,True).show_debug()
    sh.com.end()
