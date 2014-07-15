# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb

class Conta(ndb.Model):
    nome=ndb.StringProperty()

    def to_dict(self):
        dct=super(Conta, self).to_dict()
        dct['id']=self.key.id()
        return dct
