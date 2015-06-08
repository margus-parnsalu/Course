from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from sqlalchemy.exc import DBAPIError

from .models import (DBSession, Department, ITEMS_PER_PAGE )

from paginate import Page

from .forms import (DepartmentForm)




@view_config(route_name='home', renderer='home.jinja2', request_method='GET')
def home(request):
    return {'project': 'Hello World'}



@view_config(route_name='department_view', renderer='department_r.jinja2', request_method='GET')
@view_config(route_name='department_view:page', renderer='department_r.jinja2', request_method='GET')
def department_view(request):

    #Sorting custom code
    sort_value = 'hr_departments_department_name'
    if request.GET.get('sort'):
        sort_value = request.GET.get('sort')

    try:
        departments = DBSession.query(Department).order_by(sort_value).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    #Pagination logic
    current_page = int(request.matchdict.get('page','1'))
    url_for_page = lambda p: request.route_url('department_view:page', page=p) + '?sort=' + sort_value
    records = Page(departments, current_page, url_maker=url_for_page, items_per_page=ITEMS_PER_PAGE)

    return {'departments': records}



@view_config(route_name='department_add', renderer='department_f.jinja2', request_method=['GET','POST'])
def department_add(request):
    form = DepartmentForm(request.POST, csrf_context=request.session)
    if request.method == 'POST' and form.validate():
        dep = Department(department_name = form.department_name.data)
        DBSession.add(dep)
        request.session.flash('Department Added!')
        return HTTPFound(location=request.route_url('department_view'))
    return {'form': form}

@view_config(route_name='department_edit', renderer='department_f.jinja2', request_method=['GET','POST'])
def department_edit(request):
    department = DBSession.query(Department).filter(Department.department_id==request.matchdict['dep_id']).first()
    form = DepartmentForm(request.POST, department, csrf_context=request.session)
    if request.method == 'POST' and form.validate():
        form.populate_obj(department)
        DBSession.add(department)
        request.session.flash('Department Updated!')
        return HTTPFound(location=request.route_url('department_view'))
    return {'form': form}



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

