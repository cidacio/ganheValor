# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from backend.conta.model import Conta
from backend.usuario.model import Usuario


def find_by_usuario_logado():
    query = Conta.query(Conta.usuario == Usuario.key_usuario_logado()).order(Conta.nome)
    contas = query.fetch()
    contas_lista_dct = [c.to_dict() for c in contas]
    return contas_lista_dct


def salvar(nome):
    usuario_key = Usuario.key_usuario_logado()
    conta = Conta(nome=nome, usuario=usuario_key)
    conta.put()
    return conta.to_dict()


def apagar(conta_id):
    conta = ndb.Key(Conta, int(conta_id))
    conta.delete()


def atualizar(conta_id, nome):
    conta = Conta.get_by_id(int(conta_id))
    conta.nome = nome
    conta.put()


def find_keys_by_usuario_logado():
    query = Conta.query(Conta.usuario == Usuario.key_usuario_logado())
    contas = query.fetch(keys_only=True)
    contas_key = []
    for conta in contas:
        contas_key.append(conta)
    return contas_key

