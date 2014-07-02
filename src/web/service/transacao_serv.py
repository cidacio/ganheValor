# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from web.model.Transacao import Transacao
from web.model.Transacao import Categoria

def listar(_json):
    query = Transacao.query().order(Transacao.data)
    lista = query.fetch()
    lista_dct=[objeto.to_dict() for objeto in lista]
    _json(lista_dct)

def salvar(_json, complemento, categoria=None):

    if categoria:
        categoria_key=ndb.Key(Categoria, int(categoria['id']))
        objeto = Transacao(complemento=complemento, categoria=categoria_key)
    #objeto = Transacao(complemento=complemento)
    objeto.put()
    _json(objeto.to_dict())


#

    #   data=ndb.DateProperty(auto_now_add=True)
    #   categoria = ndb.KeyProperty(Categoria, required=True)
    #   valor=ndb.FloatProperty(required=True)
    #   favorecido=ndb.KeyProperty(Pessoa, required=True)
    #   conta=ndb.KeyProperty(Conta, required=True)
    #   contaDestino=ndb.KeyProperty(Conta)
    #   complemento=ndb.StringProperty()



def apagar(objeto_id):
    chave = ndb.Key(Transacao, int(objeto_id))
    chave.delete()


def atualizar(objeto_id, nome):
    objeto_id = int(objeto_id)
    transacao = Transacao.get_by_id(objeto_id)
    transacao.nome = nome
    transacao.put()
