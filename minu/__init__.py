from pyramid.config import Configurator
#Session Cookie setup
from pyramid.session import SignedCookieSessionFactory
#Security
from pyramid.authentication import AuthTktAuthenticationPolicy, RemoteUserAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder, RootFactory
from pyramid_multiauth import MultiAuthenticationPolicy
#DB connection
from sqlalchemy import engine_from_config

from .models import (DBSession, Base)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    #Session factory (CSRF)
    my_session_factory = SignedCookieSessionFactory(settings['session.secret'])

    #SqlAlchemy:
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    #Security
    #authn_policy = RemoteUserAuthenticationPolicy(environ_key='REMOTE_USER', callback=groupfinder)
    #authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    #Pyramid_multiauth seperate module for REMOTE_USER fallback
    policies = [
        RemoteUserAuthenticationPolicy(environ_key='REMOTE_USER', callback=groupfinder),
        AuthTktAuthenticationPolicy(settings['auth.secret'], callback=groupfinder, hashalg='sha512')
    ]
    authn_policy = MultiAuthenticationPolicy(policies)

    config = Configurator(settings=settings, root_factory=RootFactory, session_factory = my_session_factory)

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    #Jinja:
    #config.add_translation_dirs('locale/')
    config.include('pyramid_jinja2')


    #Static
    config.add_static_view('static', 'static', cache_max_age=3600)

    #Routes
    config.add_route('home', '/')

    #Security views
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    #Departments
    config.add_route('department_view', '/departments')
    config.add_route('department_view:page', '/departments/page/{page:\d+}')
    config.add_route('department_add', '/departments/add')
    config.add_route('department_edit', '/departments/{dep_id:\d+}/edit')
    #config.add_route('department_delete', '/departments/{dep_id:\d+}/del')

    #Employees


    config.add_route('employee_add', '/employees/add')



    config.scan()
    return config.make_wsgi_app()
