# Run tests with Nose and Coverage: nosetests --with-coverage --cover-package=minu

import unittest
import transaction

from pyramid import testing


def _initTestingDB():
    from sqlalchemy import create_engine
    from .models import (
        DBSession,
        Base,
        Department
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        model1 = Department(department_name = 'A Minu Test')
        model2 = Department(department_name = 'Z Minu Test')
        DBSession.add(model1)
        DBSession.add(model2)
    return DBSession



def _registerRoutes(config):
    config.add_route('home', '/')
    config.add_route('department_view', '/departments')
    config.add_route('department_view:page', '/departments/page/{page:\d+}')
    config.add_route('department_add', '/departments/add')
    config.add_route('department_edit', '/departments/{dep_id:\d+}/edit')


class ViewHomeTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from .views import home
        return home(request)

    def test_it(self):
        request = testing.DummyRequest()
        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['project'], 'Koolitus')



class ViewDepartmentTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from .views import department_view
        return department_view(request)

    def test_it(self):
        #from .models import Department
        request = testing.DummyRequest()
        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['departments'][0].department_name, 'A Minu Test')
        self.assertEqual(len(info['departments']), 2)

    def test_it_sort_asc(self):
        request = testing.DummyRequest()
        request.GET['sort']='+department'
        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['departments'][0].department_name, 'A Minu Test')
        self.assertEqual(info['departments'][1].department_name, 'Z Minu Test')
        self.assertEqual(info['sortdir'], '-department')


    def test_it_sort_desc(self):
        request = testing.DummyRequest()
        request.GET['sort']='-department'
        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['departments'][0].department_name, 'Z Minu Test')
        self.assertEqual(info['departments'][1].department_name, 'A Minu Test')
        self.assertEqual(info['sortdir'], '+department')



class FunctionalTests(unittest.TestCase):

    def setUp(self):
        from minu import main
        settings = { 'sqlalchemy.url': 'sqlite://',
                     'jinja2.directories' : 'minu:templates'
                     }
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        _initTestingDB()

    def tearDown(self):
        del self.testapp
        from minu.models import DBSession
        DBSession.remove()

    def test_homepage(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Koolitus</h1>', res.body)

    def test_unexisting_page(self):
        self.testapp.get('/SomePage', status=404)

    def test_query_sort_unknown(self):
        res = self.testapp.get('/departments?sort=SqlInjection', status=302)
        self.assertEqual(res.location, 'http://localhost/')



