# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from web.model.Categoria import Categoria

def listar(_json):
    query = Categoria.query().order(Categoria.descricao)
    lista = query.fetch()
    lista_dct=[objeto.to_dict() for objeto in lista]
    _json(lista_dct)

def salvar(_json, descricao):
    objeto = Categoria(descricao=descricao)
    objeto.put()
    _json(objeto.to_dict())


def apagar(conta_id):
    chave = ndb.Key(Categoria, int(conta_id))
    chave.delete()


def atualizar(conta_id, descricao):
    conta_id = int(conta_id)
    conta = Categoria.get_by_id(conta_id)
    conta.descricao = descricao
    conta.put()