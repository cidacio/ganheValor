# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import tmpl
from tekton.gae.middleware import Middleware


def execute(next_process, handler, dependencies, **kwargs):
    def write_tmpl(template_name, values=None):
        values = values or {}
        return handler.response.write(tmpl.render(template_name, values))

    dependencies["_write_tmpl"] = write_tmpl
    dependencies["_render"] = tmpl.render
    next_process(dependencies, **kwargs)


class TemplateMiddleware(Middleware):
    def set_up(self):
        def write_tmpl(template_name, values=None):
            dct={'_usuario_logado': self.dependencies.get('_usuario_logado'),
                 '_logout_url': self.dependencies.get('_logout_url'),
                 '_login_url': self.dependencies.get('_login_url')}

            dct.update(values or {})
            return self.handler.response.write(tmpl.render(template_name, dct))

        self.dependencies["_write_tmpl"] = write_tmpl
        self.dependencies["_render"] = tmpl.render
