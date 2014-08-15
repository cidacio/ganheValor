from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb


class Parcelamento(ndb.Model):
    qt_parcelas = ndb.IntegerProperty(required=False)
    tipo_parcelamento = ndb.StringProperty(required=True)
    confirmacao_automatica = ndb.BooleanProperty(required=True, default=False)

    def to_dict(self):
        dct = super(Parcelamento, self).to_dict()
        dct['id'] = self.key.id()
        return dct
