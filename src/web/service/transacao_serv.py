# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date, timedelta
from google.appengine.ext import ndb
from web.model.Transacao import Transacao
from web.model.Transacao import Categoria
from web.model.Transacao import Conta
from web.service import pessoa_serv
from web.service import parcelamento_serv


def listar(_json, mes=None, confirmada=None):

    query = Transacao.query().order(Transacao.data)

    if mes:
        data_inicial = datetime.strptime(mes, '%m/%Y')
        data_final = date(data_inicial.year, data_inicial.month + 1, 1) - timedelta(days=1)
        query = query.filter(Transacao.data >= data_inicial)
        query = query.filter(Transacao.data <= data_final)

    if confirmada:
        if confirmada == 'pendentes':
            query = query.filter(Transacao.confirmada == False)
        else:
            if confirmada == 'confirmadas':
                query = query.filter(Transacao.confirmada == True)

    lista = query.fetch()
    lista_dct=[objeto.to_dict() for objeto in lista]
    _json(lista_dct)

def salvar(_json, complemento=None, categoria_id=None, conta_id=None, valor=None, confirmada=None,
           pessoa_id=None, pessoa_nome=None, tipo_parcelamento=None, nu_parcela=None, qt_parcelas=None,
           confirmacao_automatica=None, data=None):

    categoria_key = ndb.Key(Categoria, int(categoria_id))
    conta_key = ndb.Key(Conta, int(conta_id))
    pessoa_key = pessoa_serv.crie_se_nao_existir(pessoa_id, pessoa_nome)
    data = datetime.strptime(data, '%d/%m/%Y')

    transacao = Transacao(complemento=complemento, categoria=categoria_key, conta=conta_key, valor=valor,
                          confirmada=confirmada, pessoa=pessoa_key, data=data)

    if (tipo_parcelamento != None) and (tipo_parcelamento != 'S'):
        parcelamento_key = parcelamento_serv.crie_parcelamento(tipo_parcelamento, qt_parcelas, confirmacao_automatica)
        transacao.parcelamento = parcelamento_key

    if nu_parcela:
        transacao.nu_parcela = nu_parcela

    transacao.put()

    if transacao.parcelamento:
        parcelamento_serv.atualiza_parcelas(transacao, tipo_parcelamento, qt_parcelas, confirmacao_automatica)

    _json(transacao.to_dict())


def atualizar(_json, transacao_id, complemento=None, categoria_id=None, conta_id=None, valor=None, confirmada=None,
              pessoa_id=None, pessoa_nome=None, tipo_parcelamento=None, nu_parcela=None, qt_parcelas=None,
              confirmacao_automatica=None, data=None):

    transacao_id = int(transacao_id)
    transacao = Transacao.get_by_id(transacao_id)

    if complemento:
        transacao.complemento = complemento

    if categoria_id:
        categoria_key = ndb.Key(Categoria, int(categoria_id))
        transacao.categoria = categoria_key

    if conta_id:
        conta_key = ndb.Key(Conta, int(conta_id))
        transacao.conta = conta_key

    if confirmada:
        transacao.confirmada = confirmada

    if (pessoa_id != None) or (pessoa_nome != None):
        pessoa_key = pessoa_serv.crie_se_nao_existir(pessoa_id, pessoa_nome)
        transacao.pessoa = pessoa_key

    if valor:
        transacao.valor = valor

    if data:
        transacao.data = datetime.strptime(data, '%d/%m/%Y')

    if nu_parcela:
        transacao.nu_parcela = nu_parcela

    if (tipo_parcelamento != None):

        if (transacao.parcelamento == None) and (tipo_parcelamento != 'S'):
            transacao.parcelamento = parcelamento_serv.crie_parcelamento(tipo_parcelamento, qt_parcelas,
                                                                         confirmacao_automatica)

        if (tipo_parcelamento == 'S') and (transacao.parcelamento):
            id_parcelamento_apagar = transacao.parcelamento.id()
            transacao.parcelamento = None
            transacao.nu_parcela = None

    transacao.put()

    if transacao.parcelamento:
        parcelamento_serv.atualiza_parcelas(transacao, tipo_parcelamento, qt_parcelas, confirmacao_automatica)
    else:
        if id_parcelamento_apagar:
            parcelamento_serv.apagar(id_parcelamento_apagar)

    _json(transacao.to_dict())

def apagar(objeto_id):
    chave = ndb.Key(Transacao, int(objeto_id))
    chave.delete()
