# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb

class Conta(ndb.Model):
    nome=ndb.StringProperty()

    def to_dict(self):
        dct=super(Conta, self).to_dict()
       # dct['data']=self.data.strftime('%d/%m/%Y')
       # dct['data_informada']=self.data_informada.strftime('%d/%m/%Y')
        dct['id']=self.key.id()
        return dct
