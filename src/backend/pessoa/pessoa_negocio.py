# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.ext import ndb

from backend.pessoa.model import Pessoa


def listar():
    query = Pessoa.query().order(Pessoa.nome)
    lista = query.fetch()
    lista_dct = [objeto.to_dict() for objeto in lista]
    return lista_dct

def apagar(objeto_id):
    chave = ndb.Key(Pessoa, int(objeto_id))
    chave.delete()


def crie_se_nao_existir(pessoa_id, pessoa_nome):
    if pessoa_id:
        return ndb.Key(Pessoa, int(pessoa_id))
    else:
        if pessoa_nome:
            novaPessoa = Pessoa(nome=pessoa_nome)
            novaPessoa.put()
            novaPessoa = novaPessoa.to_dict()
            return ndb.Key(Pessoa, int(novaPessoa['id']))


def atualizar(objeto_id, nome):
    objeto_id = int(objeto_id)
    pessoa = Pessoa.get_by_id(objeto_id)
    pessoa.nome = nome
    pessoa.put()
