# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.ext import ndb

from backend.categoria.model import Categoria


def listar(_json):
    query = Categoria.query().order(Categoria.descricao)
    lista = query.fetch()
    lista_dct = [objeto.to_dict() for objeto in lista]
    _json(lista_dct)


def salvar(_json, descricao, categoria_pai_id=None, tipo=None):
    objeto = Categoria(descricao=descricao, tipo=tipo)

    if categoria_pai_id:
        categoria_pai_key = ndb.Key(Categoria, int(categoria_pai_id))
        objeto.categoria_pai = categoria_pai_key

    objeto.put()
    _json(objeto.to_dict())


def apagar(categoria_id):
    chave = ndb.Key(Categoria, int(categoria_id))
    chave.delete()


def atualizar(categoria_id, descricao, tipo=None):
    categoria_id = int(categoria_id)
    categoria = Categoria.get_by_id(categoria_id)
    categoria.descricao = descricao
    if tipo:
        categoria.tipo = tipo
    categoria.put()