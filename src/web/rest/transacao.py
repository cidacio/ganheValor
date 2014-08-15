# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from backend.conta import saldo_negocio

from backend.transacao import transacao_negocio
from backend.util import datas


def listar(_json, mes=None, confirmada=None, contas=None):
    mes = datas.parser(mes, '%m/%Y')
    dct_retorno = transacao_negocio.consultar(mes, confirmada, contas)
    _json(dct_retorno)


def salvar(_json, complemento=None, categoria_id=None, conta_id=None, valor=None, confirmada=None,
           pessoa_id=None, pessoa_nome=None, tipo_parcelamento=None, nu_parcela=None, qt_parcelas=None,
           confirmacao_automatica=None, data=None):
    transacao = transacao_negocio.salvar(complemento, categoria_id, conta_id, valor, confirmada,
                                         pessoa_id, pessoa_nome, tipo_parcelamento, nu_parcela, qt_parcelas,
                                         confirmacao_automatica, data)
    _json(transacao)


def atualizar(_json, transacao_id, complemento=None, categoria_id=None, conta_id=None, valor=None, confirmada=None,
              pessoa_id=None, pessoa_nome=None, tipo_parcelamento=None, nu_parcela=None, qt_parcelas=None,
              confirmacao_automatica=None, data=None, atualiza_parcelamento=None):
    transacao = transacao_negocio.atualizar(transacao_id, complemento, categoria_id, conta_id, valor, confirmada,
                                            pessoa_id, pessoa_nome, tipo_parcelamento, nu_parcela, qt_parcelas,
                                            confirmacao_automatica, data, atualiza_parcelamento)

    _json(transacao)


def apagar(transacao_id):
    transacao_negocio.apagar(transacao_id)


def recalcula_saldo(_json, conta_id, data):
    saldo_negocio.recalcula_saldo_pelo_usuario(conta_id, data)
    _json('0')
