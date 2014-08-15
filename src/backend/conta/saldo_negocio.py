# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from backend.conta import conta_negocio
from backend.conta.model import Saldo
from backend.conta.model import Conta
from backend.transacao.model import Transacao
from backend.util import datas


def atualiza_saldo(conta_key, data, valor, confirmada):
    mes = datas.calcula_ultimo_dia_do_mes(data)
    query = Saldo.query()
    query = query.filter(Saldo.conta == conta_key)
    query = query.filter(Saldo.mes >= mes)

    saldos = query.fetch()

    if len(saldos) == 0:
        saldo = Saldo(conta=conta_key, mes=mes, saldo_mes=valor)
        if confirmada:
            mes_anterior = datas.calcula_ultimo_dia_do_mes_anterior(data)
            query = Saldo.query().filter(Saldo.mes == mes_anterior)
            query = query.filter(Saldo.conta == conta_key)
            saldo_mes_anterior = query.get()
            if saldo_mes_anterior:
                saldo.saldo_acumulado = saldo_mes_anterior.saldo_acumulado + valor
            else:
                saldo.saldo_acumulado = valor
            saldo.saldo_mes = valor
        saldo.put()
    else:
        for saldo in saldos:
            if confirmada:
                saldo.saldo_acumulado += valor

            if mes == saldo.mes:
                saldo.saldo_mes += valor

            saldo.put()


def recalcula_saldo_pelo_usuario(conta_id, data):
    conta_key = ndb.Key(Conta, int(conta_id))
    data = datas.parser(data[:10], '%Y-%m-%d')
    recalcula_saldo(conta_key, data)


def recalcula_saldo(conta_key, data):
    mes_atual = datas.calcula_ultimo_dia_do_mes(data)
    mes_anterior = datas.calcula_ultimo_dia_do_mes_anterior(data)

    query = Saldo.query().filter(Saldo.mes == mes_anterior, Saldo.conta == conta_key)
    saldo_mes_anterior = query.get()

    valor_saldo_acumuldado = 0
    if saldo_mes_anterior:
        valor_saldo_acumuldado = saldo_mes_anterior.saldo_acumulado

    query = Saldo.query().filter(Saldo.mes >= mes_atual, Saldo.conta == conta_key)
    saldos = query.fetch(keys_only=True)

    for saldo in saldos:
        saldo.delete()

    query = Transacao.query().filter(Transacao.conta == conta_key).order(Transacao.data)
    query = query.filter(Transacao.data > mes_anterior)
    transacoes = query.fetch()

    valor_saldo_mes = 0
    for transacao in transacoes:

        if transacao.data > mes_atual:
            saldo = Saldo(conta=conta_key, mes=mes_atual, saldo_acumulado=valor_saldo_acumuldado,
                          saldo_mes=valor_saldo_mes)
            saldo.put()
            valor_saldo_mes = 0
            mes_atual = datas.calcula_ultimo_dia_do_mes_posterior(mes_atual)

        valor_transacao = transacao.valor
        categoria = transacao.categoria.get()
        if categoria.tipo == 'D':
            valor_transacao = valor_transacao * -1

        valor_saldo_mes += valor_transacao

        if transacao.confirmada:
            valor_saldo_acumuldado += valor_transacao

    saldo = Saldo(conta=conta_key, mes=mes_atual, saldo_acumulado=valor_saldo_acumuldado,
                  saldo_mes=valor_saldo_mes)
    saldo.put()


def consultar_orcamento(mes_inicial):
    mes_atual = datas.parser(mes_inicial)
    mes_atual = datas.calcula_ultimo_dia_do_mes(mes_atual)
    mes_anterior = datas.calcula_ultimo_dia_do_mes_anterior(mes_atual)

    query = Saldo.query().filter(Saldo.mes == mes_anterior)
    query = query.filter(Saldo.conta.IN(conta_negocio.find_keys_by_usuario_logado()))
    saldos_anteriores = query.fetch()

    valor_acumulado = 0
    for saldo_anterior in saldos_anteriores:
        valor_acumulado += saldo_anterior.saldo_acumulado

    query = Transacao.query().filter(Transacao.data <= mes_anterior, Transacao.confirmada == False)
    query = query.filter(Transacao.conta.IN(conta_negocio.find_keys_by_usuario_logado()))
    transacoes_em_atraso = query.fetch()
    valor_saldo_mes = 0
    for transacao in transacoes_em_atraso:

        valor_transacao = transacao.valor
        categoria = transacao.categoria.get()
        if categoria.tipo == 'D':
            valor_transacao = valor_transacao * -1

        valor_saldo_mes += valor_transacao

    rows = []

    for nu_mes in range(1, 12):

        query = Saldo.query().filter(Saldo.mes == mes_atual)
        query = query.filter(Saldo.conta.IN(conta_negocio.find_keys_by_usuario_logado()))
        saldos = query.fetch()

        for saldo in saldos:
            valor_saldo_mes += saldo.saldo_mes

        dct_mes = [{"v": datas.mes_por_extenso(mes_atual)}, {"v": valor_acumulado, "f": str(valor_acumulado)},
                   {"v": valor_saldo_mes, "f": str(valor_saldo_mes)}]

        rows += [{"c": dct_mes}]

        mes_atual = datas.calcula_ultimo_dia_do_mes_posterior(mes_atual)
        valor_acumulado += valor_saldo_mes
        valor_saldo_mes = 0

    return rows


def consultar_saldo(mes, contas):
    contas_key = []

    if (not contas) or (contas == ''):
        contas_key = conta_negocio.find_keys_by_usuario_logado()
    else:
        for valor in contas.split(','):
            conta_key = ndb.Key(Conta, int(valor))
            contas_key.append(conta_key)

    mes = datas.calcula_ultimo_dia_do_mes(mes)
    query = Saldo.query().filter(Saldo.mes == mes)
    query = query.filter(Saldo.conta.IN(contas_key))

    saldos = query.fetch()
    valor_saldo_mes = 0
    for saldo in saldos:
        valor_saldo_mes += saldo.saldo_acumulado

    return valor_saldo_mes