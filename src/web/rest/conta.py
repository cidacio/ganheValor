# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from backend.conta import conta_negocio


def listar(_json):
    contas = conta_negocio.find_by_usuario_logado()
    _json(contas)


def salvar(_json, nome):
    conta = conta_negocio.salvar(nome=nome)
    _json(conta)


def apagar(conta_id):
    conta_negocio.apagar(conta_id=conta_id)


def atualizar(_json, conta_id, nome):
    conta = conta_negocio.atualizar(conta_id=conta_id, nome=nome)
    _json(conta)
