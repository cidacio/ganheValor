# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from backend.conta import saldo_negocio


def consultar_orcamento_grafico(_json, mes_inicial):
    dados_grafico = saldo_negocio.consultar_orcamento(mes_inicial)

    _json(dados_grafico)
