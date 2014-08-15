# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from copy import copy
import datetime

from google.appengine.ext import ndb

from backend.parcelamento.model import Parcelamento
from backend.transacao.model import Transacao


def crie_parcelamento(tipo_parcelamento, qt_parcelas, confirmacao_automatica):
    parcelamento = Parcelamento(tipo_parcelamento=tipo_parcelamento, qt_parcelas=qt_parcelas)

    if confirmacao_automatica:
        parcelamento.confirmacao_automatica = confirmacao_automatica
    parcelamento.put()
    parcelamento = parcelamento.to_dict()
    return ndb.Key(Parcelamento, int(parcelamento['id']))


def atualiza_parcelas(transacao, tipo_parcelamento, qt_parcelas, confirmacao_automatica):
    parcelamento = Parcelamento.get_by_id(transacao.parcelamento.id())
    if qt_parcelas:
        parcelamento.qt_parcelas = qt_parcelas
    if tipo_parcelamento:
        parcelamento.tipo_parcelamento = tipo_parcelamento
    if confirmacao_automatica:
        parcelamento.confirmacao_automatica = confirmacao_automatica
    parcelamento.put()

    query = Transacao.query(Transacao.parcelamento == parcelamento.key, Transacao.data > transacao.data)
    transacoes = query.fetch(keys_only=True)
    for transacao_excluir in transacoes:
        transacao_excluir.delete()

    qt_parcelas = parcelamento.qt_parcelas
    if parcelamento.tipo_parcelamento == 'I':
        qt_parcelas = 12

    parcela_inicial = transacao.nu_parcela
    if not parcela_inicial:
        parcela_inicial = 0

    for nu_parcela in range(parcela_inicial + 1, qt_parcelas):
        nova_transacao = copy(transacao)
        nova_transacao.confirmada = False
        nova_transacao.nu_parcela = nu_parcela
        nova_transacao.key = None
        qt_dias = (nu_parcela - parcela_inicial) * 30
        nova_transacao.data = transacao.data + datetime.timedelta(days=qt_dias)
        nova_transacao.put()


def apagar(objeto_id):
    chave = ndb.Key(Parcelamento, int(objeto_id))
    chave.delete()
