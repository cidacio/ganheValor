# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb


class Categoria(ndb.Model):
    descricao = ndb.StringProperty()
    tipo = ndb.StringProperty()
    categoria_pai = ndb.KeyProperty(kind="Categoria", required=False)
    # categorias_filhas = ndb.KeyProperty(kind="Categoria", repeated=True)

    def to_dict(self):
        dct = super(Categoria, self).to_dict()
        if self.categoria_pai:
            dct['categoria_pai'] = self.categoria_pai.get().to_dict()
        dct['id'] = self.key.id()
        return dct