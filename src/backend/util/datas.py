# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date, timedelta


def calcula_ultimo_dia_do_mes(data):
    ano = data.year
    mes = data.month
    mes += 1
    if mes > 12:
        mes = 1
        ano += 1

    ultimo_dia_mes = date(ano, mes, 1)
    ultimo_dia_mes = ultimo_dia_mes - timedelta(days=1)
    return ultimo_dia_mes


def calcula_ultimo_dia_do_mes_anterior(data):
    ultimo_dia_mes = date(data.year, data.month, 1) - timedelta(days=1)
    return ultimo_dia_mes


def calcula_ultimo_dia_do_mes_posterior(data):
    ultimo_dia_mes = calcula_ultimo_dia_do_mes(data) + timedelta(days=1)
    ultimo_dia_mes = calcula_ultimo_dia_do_mes(ultimo_dia_mes)
    return ultimo_dia_mes


def parser(data_string, formato='%Y-%m-%d'):
    return datetime.strptime(data_string, formato)


def mes_por_extenso(data):
    meses = (
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro',
        'Dezembro')
    return meses[data.month - 1]


def calcula_primeiro_dia_do_mes(data):
    return date(data.year, data.month, 1)
