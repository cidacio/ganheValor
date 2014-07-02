# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from web.model.Categoria import Categoria
from web.model.Conta import Conta
from web.model.Pessoa import Pessoa


class Transacao(ndb.Model):
    data=ndb.DateProperty(auto_now_add=True)
    categoria = ndb.KeyProperty(Categoria, required=False)
    # valor=ndb.FloatProperty(required=True)
    # favorecido=ndb.KeyProperty(Pessoa, required=True)
    # conta=ndb.KeyProperty(Conta, required=True)
    # contaDestino=ndb.KeyProperty(Conta)
    complemento=ndb.StringProperty()

    def to_dict(self):
        dct=super(Transacao, self).to_dict()
        # dct['data']=self.data.strftime('%d/%m/%Y')
        # dct['data_informada']=self.data_informada.strftime('%d/%m/%Y')
        dct['categoria_id']=self.categoria.id()
        dct['id']=self.key.id()
        return dct