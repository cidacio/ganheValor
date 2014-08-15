# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from backend.usuario.model import Usuario
from google.appengine.ext import ndb

class Conta(ndb.Model):
    nome = ndb.StringProperty()
    usuario = ndb.KeyProperty(Usuario, required=True)

    def to_dict(self):
        dct = super(Conta, self).to_dict()
        dct['usuario'] = self.usuario.get().to_dict()
        dct['id'] = self.key.id()
        return dct

class Saldo(ndb.Model):
    conta = ndb.KeyProperty(Conta, required=True)
    mes = ndb.DateProperty(required=True)
    saldo_acumulado = ndb.FloatProperty(required=True, default=0)
    saldo_mes = ndb.FloatProperty(required=True, default=0)

    def to_dict(self):
        dct = super(Saldo, self).to_dict()
        dct['conta'] = self.conta.get().to_dict()
        dct['id'] = self.key.id()
        return dct