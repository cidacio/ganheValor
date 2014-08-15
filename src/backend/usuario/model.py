# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.ext import ndb
from google.appengine.api import users

from backend.pessoa.model import Pessoa


class Usuario(Pessoa):
    email = ndb.StringProperty()
    google_id = ndb.StringProperty()

    def to_dict(self):
        dct = super(Usuario, self).to_dict()
        dct['id'] = self.key.id()
        return dct

    @classmethod
    def query_by_google_id(cls, google_id):
        return cls.query(cls.google_id == google_id)

    @classmethod
    def key_usuario_logado(cls):
        usuario_google = users.get_current_user()
        query = Usuario.query_by_google_id(usuario_google.user_id())
        usuario = query.get()
        return usuario.key
