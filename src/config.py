#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh
import skl_shared_qt.config as qc

PRODUCT_LOW = 'unmusic'


class Paths:
    
    def __init__(self):
        self.Success = True
    
    def check(self):
        self.ihome = sh.Home(PRODUCT_LOW)
        self.Success = self.ihome.create_conf()
    
    def get_default_config(self):
        return sh.objs.get_pdir().add('..', 'resources', 'config', 'default.json')
    
    def get_schema(self):
        return sh.objs.get_pdir().add('..', 'resources', 'config', 'schema.json')
    
    def get_local_config(self):
        return self.ihome.add_config(PRODUCT_LOW + '.json')
    
    def get_db(self):
        return self.ihome.add_config(PRODUCT_LOW + '.db')
    
    def get_local_collection(self):
        return self.ihome.add_share(_('local collection'))
    
    def get_local_album(self, albumid):
        return self.ihome.add_share(_('local collection'), str(albumid))
    
    def get_external_album(self, albumid):
        return self.ihome.add_share(_('external collection'), str(albumid))
    
    def get_processed_album(self, albumid):
        return self.ihome.add_share(_('processed'), str(albumid))
    
    def get_external_collection(self):
        return self.ihome.add_share(_('external collection'))
    
    def get_mobile_collection(self):
        return self.ihome.add_share(_('mobile collection'))
    
    def get_playlist(self):
        return self.ihome.add_share(_('playlist') + '.m3u8')
    
    def run(self):
        self.check()



class Config(qc.Config):
    
    def __init__(self, default, schema, local):
        super().__init__(default, schema, local)
        self.set_values()
        self.default = default
        self.schema = schema
        self.local = local
    
    def update(self):
        f = '[unmusic] config.Config.update'
        if not self.Success:
            sh.com.cancel(f)
            return
        self._copy()
        if self.ilocal.Success:
            mes = _('Update default configuration')
            self.new = qc.Update(self.idefault.get(), self.ilocal.get()).run()
        else:
            mes = _('Use default configuration')
        sh.objs.get_mes(f, mes, True).show_info()
    
    def quit(self):
        self.save()
    
    def run(self):
        self.load()
        self.update()
        self.set_local_dump()


PATHS = Paths()
PATHS.run()
default = PATHS.get_default_config()
schema = PATHS.get_schema()
local = PATHS.get_local_config()
CONFIG = Config(default, schema, local)
CONFIG.run()
