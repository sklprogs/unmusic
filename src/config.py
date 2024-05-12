#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

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
    
    def get_default(self):
        return sh.objs.get_pdir().add('..', 'resources', 'config', 'default.json')
    
    def get_schema(self):
        return sh.objs.get_pdir().add('..', 'resources', 'config', 'schema.json')
    
    def get_local(self):
        return self.ihome.add_config(PRODUCT_LOW + '.json')
    
    def get_db(self):
        return self.ihome.add_config(PRODUCT_LOW + '.db')
    
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



class Objects:
    
    def __init__(self):
        self.paths = self.config = None
    
    def get_paths(self):
        if self.paths is None:
            self.paths = Paths()
            self.paths.run()
        return self.paths
    
    def get_config(self):
        if self.config is None:
            default = self.get_paths().get_default()
            schema = self.paths.get_schema()
            local = self.paths.get_local()
            self.config = Config(default, schema, local)
            self.config.run()
        return self.config


objs = Objects()
