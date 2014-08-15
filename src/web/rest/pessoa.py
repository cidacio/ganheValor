# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from backend.pessoa import pessoa_negocio

def listar(_json):
    lista_dct = pessoa_negocio.listar()
    _json(lista_dct)