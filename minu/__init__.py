from pyramid.config import Configurator
#Session Cookie setup
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    #Session factory (CSRF)
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    #SqlAlchemy:
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

     #Session factory included
    config = Configurator(settings=settings, session_factory = my_session_factory)


    #Jinja:
    #config.add_translation_dirs('locale/')
    config.include('pyramid_jinja2')

    #Static
    config.add_static_view('static', 'static', cache_max_age=3600)

    #Routes
    config.add_route('home', '/')

    #Departments
    config.add_route('department_view', '/departments')
    config.add_route('department_view:page', '/departments/page/{page:\d+}')
    config.add_route('department_add', '/departments/add')
    config.add_route('department_edit', '/departments/{dep_id:\d+}/edit')
    #config.add_route('department_delete', '/departments/{dep_id:\d+}/del')



    config.scan()
    return config.make_wsgi_app()
