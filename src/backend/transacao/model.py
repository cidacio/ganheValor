# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.ext import ndb

from backend.categoria.model import Categoria
from backend.conta.model import Conta
from backend.pessoa.model import Pessoa
from backend.parcelamento.model import Parcelamento


class Transacao(ndb.Model):
    data = ndb.DateProperty(auto_now_add=True)
    categoria = ndb.KeyProperty(Categoria, required=True)
    valor = ndb.FloatProperty(required=True)
    confirmada = ndb.BooleanProperty(default=False)
    pessoa = ndb.KeyProperty(Pessoa, required=True)
    conta = ndb.KeyProperty(Conta, required=True)
    conta_destino = ndb.KeyProperty(Conta, required=False)
    parcelamento = ndb.KeyProperty(Parcelamento, required=False)
    complemento = ndb.StringProperty(required=False)
    nu_parcela = ndb.IntegerProperty(required=False)

    def to_dict(self):
        dct = super(Transacao, self).to_dict()
        dct['data'] = self.data.isoformat()  # 1385989325053  #self.data.strftime('%a, %d %b %Y %H:%M:%S GMT')
        dct['categoria'] = self.categoria.get().to_dict()
        dct['conta'] = self.conta.get().to_dict()
        dct['pessoa'] = self.pessoa.get().to_dict()

        if self.conta_destino:
            dct['conta_destino'] = self.conta_destino.get().to_dict()

        dct['tipo_parcelamento'] = 'S'
        if self.parcelamento:
            dct['parcelamento'] = self.parcelamento.get().to_dict()
            dct['tipo_parcelamento'] = dct['parcelamento']['tipo_parcelamento']

        dct['id'] = self.key.id()
        return dct