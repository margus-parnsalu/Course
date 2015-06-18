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
    engine = create_engine('sqlite:///my_test.sqlite')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        model = Department(department_name = 'Minu Test')
        DBSession.add(model)
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
        self.assertEqual(info['departments'][0].department_name, 'Minu Test')
        #self.assertEqual(len(info['departments']), 1)


