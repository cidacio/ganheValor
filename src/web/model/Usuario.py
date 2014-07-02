# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb

class Usuario(Pessoa):
    login=ndb.StringProperty()
    senha=ndb.StringProperty()