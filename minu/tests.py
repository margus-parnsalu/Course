# Run tests with Nose and Coverage: nosetests --with-coverage --cover-package=minu

import unittest
import transaction

from pyramid import testing


def _initTestingDB():
    from sqlalchemy import create_engine
    from .models import (
        DBSession,
        Base,
        Department,
        Employee
        )
    import datetime
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        dep1 = Department(department_name = 'A Minu Test')
        dep2 = Department(department_name = 'Z Minu Test')
        DBSession.add(dep1)
        DBSession.add(dep2)
        emp1 = Employee(first_name = 'John', last_name= 'Dow', email= 'john.dow@mail.com',
                        phone_number= '879593535', hire_date= datetime.date(2015, 3, 15), salary= 3000)
        emp2 = Employee(first_name = 'Tom', last_name= 'Taylor', email= 'tom.taylor@mail.com',
                        phone_number= '87959789', hire_date= datetime.date(2015, 6, 12), salary= 5000)
        DBSession.add(emp1)
        DBSession.add(emp2)

    return DBSession


def _registerRoutes(config):
    config.add_route('home', '/')
    config.add_route('department_view', '/departments')
    config.add_route('department_view:page', '/departments/page/{page:\d+}')
    config.add_route('department_add', '/departments/add')
    config.add_route('department_edit', '/departments/{dep_id:\d+}/edit')

    #Employees
    config.add_route('employee_view', '/employees')
    config.add_route('employee_view:page', '/employees/page/{page:\d+}')
    config.add_route('employee_add', '/employees/add')
    config.add_route('employee_edit', '/employees/{emp_id:\d+}/edit')


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


class ViewEmployeeTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from .views import employee_view
        return employee_view(request)

    def test_it(self):
        request = testing.DummyRequest()
        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['employees'][0].Employee.first_name, 'John')
        self.assertEqual(len(info['employees']), 2)

    def test_it_sort_asc(self):
        request = testing.DummyRequest()
        request.GET['sort']='+employee'
        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['employees'][0].Employee.first_name, 'John')
        self.assertEqual(info['employees'][1].Employee.first_name, 'Tom')
        self.assertEqual(info['sortdir'], '-employee')


    def test_it_sort_desc(self):
        request = testing.DummyRequest()
        request.GET['sort']='-employee'
        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['employees'][0].Employee.first_name, 'Tom')
        self.assertEqual(info['employees'][1].Employee.first_name, 'John')
        self.assertEqual(info['sortdir'], '+employee')


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

    def test_departments_query_sort_unknown(self):
        res = self.testapp.get('/departments?sort=SqlInjection', status=302)
        self.assertEqual(res.location, 'http://localhost/')

    def test_departments_report(self):
        res = self.testapp.get('/departments', status=200)
        self.assertIn(b'<h3>Departments</h3>', res.body)

    def test_employees_report(self):
        res = self.testapp.get('/employees', status=200)
        self.assertIn(b'<h3>Employees</h3>', res.body)
