# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from backend.transacao.model import Transacao
from backend.conta.model import Conta
from backend.categoria.model import Categoria
from datetime import datetime, date, timedelta
from backend.parcelamento import parcelamento_negocio
from backend.pessoa import pessoa_negocio
from backend.conta import saldo_negocio, conta_negocio
from backend.util import datas

import locale


def apagar(transacao_id):
    transacao_key = ndb.Key(Transacao, int(transacao_id))
    transacao = transacao_key.get()
    transacao_key.delete()
    saldo_negocio.atualiza_saldo(transacao.conta, transacao.data, transacao.valor * -1, transacao.confirmada)


def consultar(mes=None, confirmada=None, contas=None):
    contas_key = []

    if (not contas) or (contas == ''):
        contas_key = conta_negocio.find_keys_by_usuario_logado()
    else:
        for valor in contas.split(','):
            conta_key = ndb.Key(Conta, int(valor))
            contas_key.append(conta_key)

    query = Transacao.query().order(Transacao.data)

    if mes:
        data_inicial = datas.calcula_primeiro_dia_do_mes(mes)
        data_final = datas.calcula_ultimo_dia_do_mes(mes)
        query = query.filter(Transacao.data >= data_inicial)
        query = query.filter(Transacao.data <= data_final)

    if confirmada:
        if confirmada == 'pendentes':
            query = query.filter(Transacao.confirmada == False)
        else:
            if confirmada == 'confirmadas':
                query = query.filter(Transacao.confirmada == True)

    query = query.filter(Transacao.conta.IN(contas_key))

    lista = query.fetch()

    data_atual = datetime.now()
    data_atual = date(data_atual.year, data_atual.month, data_atual.day)

    if (data_atual <= data_final) and (data_atual >= data_inicial):
        if confirmada != 'confirmadas':
            query = Transacao.query().order(Transacao.data)
            query = query.filter(Transacao.confirmada == False)
            query = query.filter(Transacao.data < data_inicial)
            query = query.filter(Transacao.conta.IN(contas_key))
            lista_atrasadas = query.fetch()
            lista = lista_atrasadas + lista

    transacoes_dct = [objeto.to_dict() for objeto in lista]

    mes_anterior = datas.calcula_ultimo_dia_do_mes_anterior(mes)
    saldo_anterior = saldo_negocio.consultar_saldo(mes_anterior, contas)
    valor_saldo = saldo_anterior

    for objeto in transacoes_dct:
        valor_transacao = objeto['valor']
        if objeto['categoria']['tipo'] == 'D':
            valor_transacao = objeto['valor'] * -1
        valor_saldo += valor_transacao
        objeto['saldo'] = locale.format("%1.2f", valor_saldo, 1)

    data = str(mes.day) + '/' + str(mes.month) + '/' + str(mes.year)

    return {"saldo_anterior": {"data": data, "saldo": saldo_anterior},
            "transacoes": transacoes_dct}


def salvar(complemento=None, categoria_id=None, conta_id=None, valor=None, confirmada=None,
           pessoa_id=None, pessoa_nome=None, tipo_parcelamento=None, nu_parcela=None, qt_parcelas=None,
           confirmacao_automatica=None, data=None):
    categoria_key = ndb.Key(Categoria, int(categoria_id))
    conta_key = ndb.Key(Conta, int(conta_id))
    pessoa_key = pessoa_negocio.crie_se_nao_existir(pessoa_id, pessoa_nome)
    data = datetime.strptime(data[:10], '%Y-%m-%d')

    transacao = Transacao(complemento=complemento, categoria=categoria_key, conta=conta_key, valor=valor,
                          confirmada=confirmada, pessoa=pessoa_key, data=data)

    if (tipo_parcelamento != None) and (tipo_parcelamento != 'S'):
        parcelamento_key = parcelamento_negocio.crie_parcelamento(tipo_parcelamento, qt_parcelas,
                                                                  confirmacao_automatica)
        transacao.parcelamento = parcelamento_key

    if nu_parcela:
        transacao.nu_parcela = nu_parcela

    transacao.put()

    if transacao.parcelamento:
        parcelamento_negocio.atualiza_parcelas(transacao, tipo_parcelamento, qt_parcelas, confirmacao_automatica)
        saldo_negocio.recalcula_saldo(transacao.conta, transacao.data)
    else:
        categoria = transacao.categoria.get()
        valor_transacao = 0
        if categoria.tipo == 'D':
            valor_transacao = transacao.valor * -1
        saldo_negocio.atualiza_saldo(transacao.conta, transacao.data, valor_transacao, transacao.confirmada)

    return transacao.to_dict()


def atualizar(transacao_id, complemento=None, categoria_id=None, conta_id=None, valor=None, confirmada=None,
              pessoa_id=None, pessoa_nome=None, tipo_parcelamento=None, nu_parcela=None, qt_parcelas=None,
              confirmacao_automatica=None, data=None, atualiza_parcelamento=None):
    transacao_id = int(transacao_id)
    transacao = Transacao.get_by_id(transacao_id)
    conta_anterior = transacao.conta
    id_parcelamento_apagar = None;

    if complemento:
        transacao.complemento = complemento

    if categoria_id:
        categoria_key = ndb.Key(Categoria, int(categoria_id))
        transacao.categoria = categoria_key

    if conta_id:
        conta_key = ndb.Key(Conta, int(conta_id))
        transacao.conta = conta_key

    if confirmada != None:
        transacao.confirmada = confirmada

    if (pessoa_id != None) or (pessoa_nome != None):
        pessoa_key = pessoa_negocio.crie_se_nao_existir(pessoa_id, pessoa_nome)
        transacao.pessoa = pessoa_key

    diferenca_valores = 0
    if valor:
        diferenca_valores = valor - transacao.valor
        transacao.valor = valor

    menor_data_atualizar_saldo = transacao.data
    if data:
        nova_data = datetime.strptime(data[:10], '%Y-%m-%d')
        if nova_data.toordinal() < transacao.data.toordinal():
            menor_data_atualizar_saldo = nova_data
        transacao.data = nova_data

    if nu_parcela:
        transacao.nu_parcela = nu_parcela

    if (tipo_parcelamento != None):

        if (transacao.parcelamento == None) and (tipo_parcelamento != 'S'):
            transacao.parcelamento = parcelamento_negocio.crie_parcelamento(tipo_parcelamento, qt_parcelas,
                                                                            confirmacao_automatica)

        if (tipo_parcelamento == 'S') and (transacao.parcelamento):
            id_parcelamento_apagar = transacao.parcelamento.id()
            transacao.parcelamento = None
            transacao.nu_parcela = None

    transacao.put()

    if transacao.parcelamento:
        if atualiza_parcelamento:
            parcelamento_negocio.atualiza_parcelas(transacao, tipo_parcelamento, qt_parcelas, confirmacao_automatica)
        saldo_negocio.recalcula_saldo(transacao.conta, menor_data_atualizar_saldo)
        if transacao.conta != conta_anterior:
            saldo_negocio.recalcula_saldo(conta_anterior, menor_data_atualizar_saldo)

    else:
        if id_parcelamento_apagar:
            parcelamento_negocio.apagar(id_parcelamento_apagar)
            saldo_negocio.recalcula_saldo(transacao.conta, menor_data_atualizar_saldo)
            if transacao.conta != conta_anterior:
                saldo_negocio.recalcula_saldo(conta_anterior, menor_data_atualizar_saldo)
        else:
            if diferenca_valores > 0:
                saldo_negocio.atualiza_saldo(transacao.conta, menor_data_atualizar_saldo, diferenca_valores,
                                             transacao.confirmada)
                if transacao.conta != conta_anterior:
                    saldo_negocio.atualiza_saldo(conta_anterior, menor_data_atualizar_saldo, diferenca_valores,
                                                 transacao.confirmada)

    return transacao.to_dict()