# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb

class Categoria(ndb.Model):
    descricao=ndb.StringProperty()
    tipo=ndb.StringProperty()

    def to_dict(self):
        dct=super(Categoria, self).to_dict()
        dct['id']=self.key.id()
        return dct