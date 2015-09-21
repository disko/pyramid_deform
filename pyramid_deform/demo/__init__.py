# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

# from pyramid_deform.demo.views import wizard_view


session_factory = SignedCookieSessionFactory('secret')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """

    config = Configurator(settings=settings)

    config.set_session_factory(session_factory)

    config.include('pyramid_chameleon')

    config.add_static_view('static', 'pyramid_deform.demo:static',
                           cache_max_age=3600)

    config.add_route('wizard', '/')

    config.scan()

    return config.make_wsgi_app()
