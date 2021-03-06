from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import remember, forget, authenticated_userid

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import text

from .security import (userfinder)
from .models import (DBSession, Department, Employee, ITEMS_PER_PAGE )

#SqlAlchemy object pagination logic extends Paginate
from paginate_sqlalchemy import SqlalchemyOrmPage
#Sorting logic
from .sorts import SortValue

from .forms import (LoginForm, DepartmentForm, EmployeeForm)



@view_config(route_name='home', renderer='home.jinja2', request_method='GET', permission='view')
def home(request):
    project_name = 'Demo App'

    return {'project': project_name,
            'logged_in': authenticated_userid(request)}



@view_config(route_name='department_view', renderer='department_r.jinja2', request_method='GET', permission='view')
@view_config(route_name='department_view:page', renderer='department_r.jinja2', request_method='GET', permission='view')
def department_view(request):
    #Getting 'sort' URL query parameter and initializing if not present
    sort_input = request.GET.get('sort','+department')
    #Sorting custom code from sorts.py
    sv = SortValue(sort_input)
    sort_value=sv.sort_str()
    #If sort value not found reroute to homepage
    if sort_value is '':
        return HTTPFound(location=request.route_url('home'))
    #For supporting two-way sorting on the template
    sort_dir = sv.reverse_direction()

    #SqlAlchemy query object for the report
    departments = DBSession.query(Department).order_by(text(sort_value))

    #Debug break point example
    #import pdb; pdb.set_trace()

    #Pagination logic with Sqlalchemy object
    current_page = int(request.matchdict.get('page','1'))
    url_for_page = lambda p: request.route_url('department_view:page', page=p,
                                               _query=(('sort', sort_input), ))
    try:
        records = SqlalchemyOrmPage(departments, current_page,
                                    url_maker=url_for_page, items_per_page=ITEMS_PER_PAGE)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    return {'departments': records,
            'sortdir': sort_dir,
            'logged_in': authenticated_userid(request) }



@view_config(route_name='department_add', renderer='department_f.jinja2', request_method=['GET','POST'], permission='edit')
def department_add(request):

    form = DepartmentForm(request.POST, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        dep = Department(department_name = form.department_name.data)
        DBSession.add(dep)
        request.session.flash('Department Added!')
        return HTTPFound(location=request.route_url('department_view'))

    return {'form': form,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='department_edit', renderer='department_f.jinja2', request_method=['GET','POST'], permission='edit')
def department_edit(request):

    try:
        department = DBSession.query(Department).filter(Department.department_id==request.matchdict['dep_id']).one()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    except NoResultFound:
        return HTTPNotFound('Department not found!')

    form = DepartmentForm(request.POST, department, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        form.populate_obj(department)
        DBSession.add(department)
        request.session.flash('Department Updated!')
        return HTTPFound(location=request.route_url('department_view'))

    return {'form': form,
            'logged_in': authenticated_userid(request)}




@view_config(route_name='employee_add', renderer='employee_f.jinja2', request_method=['GET','POST'], permission='edit')
def employee_add(request):

    form = EmployeeForm(request.POST, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        emp = Employee(first_name = form.first_name.data,
                       last_name = form.last_name.data,
                       email = form.email.data,
                       phone_number = form.phone_number.data,
                       salary = form.salary.data,
                       hire_date = form.hire_date.data,
                       end_date = form.end_date.data,
                       department = form.department.data)
        DBSession.add(emp)
        request.session.flash('Employee Added!')
        return HTTPFound(location=request.route_url('home'))

    return {'form': form,
            'logged_in': authenticated_userid(request)}




@view_config(route_name='login', renderer='login.jinja2', permission='view')
@forbidden_view_config(renderer='login.jinja2')#For customizing default 404 forbidden template
def login(request):
    came_from = request.referer or request.route_url('home')
    login_url = request.route_url('login')
    if came_from == login_url:
        came_from = '/' # never use the login form itself as came_from
    login = ''
    form = LoginForm(request.POST, came_from, login, csrf_context=request.session)
    message = ''
    if request.method == 'POST' and form.validate():
        login = request.params['login']
        password = request.params['password']
        if userfinder(login, password) == True:
            headers = remember(request, login)
            request.session.flash('User: '+ login + ' logged in!')
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login!'
    return {'form' : form,
            'message' : message,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='logout',
             permission='view')
def logout(request):
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location = loc, headers = headers)



conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_minu_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

