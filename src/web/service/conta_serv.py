# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from web.model.Conta import Conta


def listar(_json):
    query = Conta.query().order(Conta.nome)
    contas = query.fetch()
    contas_lista_dct=[c.to_dict() for c in contas]
    _json(contas_lista_dct)

def salvar(_json, nome):
    conta = Conta(nome=nome)
    conta.put()
    _json(conta.to_dict())


def apagar(conta_id):
    chave = ndb.Key(Conta, int(conta_id))
    chave.delete()


def atualizar(conta_id, nome):
    conta_id = int(conta_id)
    conta = Conta.get_by_id(conta_id)
    conta.nome = nome
    conta.put()


