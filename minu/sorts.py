#Dictionary of allowed sorting values for SqlAlchemy order_by
SORT_DICT = {
                '1': '1',
                '0': '0',
                '-department':'upper(hr_departments.department_name) desc',
                '+department':'upper(hr_departments.department_name) asc',
                'employee':'hr_employees.first_name',
                'salary':'hr_employees_salary'
             }

class SortValue:

    def __init__(self, sort_parameter, direction):
        self.sort_parameter=sort_parameter
        self.direction=direction

    def validate(self):
        #URL Query attribute validation
        if SORT_DICT.get(self.sort_parameter)==None:
            return False
        return True

    def sort_obj(self):
        return getattr(self.sort_parameter, 'desc')


    def sort_str(self):
        return SORT_DICT.get(self.sort_parameter, '')
        #sortstr=''
        #If there is mach in URL query value
        #if sort != '':
        #    if sort[0]=='-':
        #        return
        #    else:
        #        dirstr='ASC'
        #    sortstr=('%s %s' % (sort, dirstr))
        #return sortstr

    def reverse_direction(self):
        if self.sort_parameter[0]=='+':
            dir= str.replace(self.sort_parameter, '+', '-', 1)
        if self.sort_parameter[0]=='-':
            dir= str.replace(self.sort_parameter, '-', '+', 1)
        return dir