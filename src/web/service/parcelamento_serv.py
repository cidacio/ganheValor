# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from web.model.Parcelamento import Parcelamento
from web.model.Transacao import Transacao
from copy import copy
import datetime

def crie_parcelamento(tipo_parcelamento, qt_parcelas, confirmacao_automatica):
    parcelamento = Parcelamento(tipo_parcelamento=tipo_parcelamento, qt_parcelas=qt_parcelas,
                                confirmacao_automatica=confirmacao_automatica)
    parcelamento.put()
    parcelamento = parcelamento.to_dict()
    return ndb.Key(Parcelamento, int(parcelamento['id']))

def atualiza_parcelas(transacao, tipo_parcelamento, qt_parcelas, confirmacao_automatica):

    parcelamento = Parcelamento.get_by_id(transacao.parcelamento.id())
    parcelamento.qt_parcelas = qt_parcelas
    parcelamento.tipo_parcelamento = tipo_parcelamento
    parcelamento.confirmacao_automatica = confirmacao_automatica
    parcelamento.put()

#, parcelamento=parcelamento.key, data>transacao.data, keys_only=True
    query = Transacao.query(Transacao.parcelamento==parcelamento.key, Transacao.data>transacao.data)
    transacoes = query.fetch(keys_only=True)
    for transacao_excluir in transacoes:
        transacao_excluir.delete()

    if tipo_parcelamento == 'I':
        qt_parcelas = 12

    for nu_parcela in range(transacao.nu_parcela + 1, qt_parcelas):
        nova_transacao = copy(transacao)
        nova_transacao.confirmada = False
        nova_transacao.nu_parcela = nu_parcela
        nova_transacao.key = None
        qt_dias = (nu_parcela - transacao.nu_parcela)*30
        nova_transacao.data = transacao.data + datetime.timedelta(days=qt_dias)
        nova_transacao.put()

def apagar(objeto_id):
    chave = ndb.Key(Parcelamento, int(objeto_id))
    chave.delete()
