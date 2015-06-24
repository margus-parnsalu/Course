#Dictionary of allowed sorting values for SqlAlchemy order_by
SORT_DICT = {
                '-department':'upper(hr_departments.department_name) desc',
                '+department':'upper(hr_departments.department_name) asc',
                '+employee':'upper(hr_employees.first_name || hr_employees.last_name) asc',
                '-employee':'upper(hr_employees.first_name || hr_employees.last_name) desc',
                '+salary':'hr_employees.salary asc',
                '-salary':'hr_employees.salary desc',
                '+hired':'hr_employees.hire_date asc',
                '-hired':'hr_employees.hire_date desc',
                '+hireend':'hr_employees.end_date asc',
                '-hireend':'hr_employees.end_date desc',
             }

class SortValue:

    def __init__(self, sort_parameter):
        self.sort_parameter=sort_parameter

    def validate(self):
        #URL Query attribute validation
        if SORT_DICT.get(self.sort_parameter)==None:
            return False
        return True

    def sort_str(self):
        return SORT_DICT.get(self.sort_parameter, '')

    def reverse_direction(self):
        if self.sort_parameter[0]=='+':
            dir= self.sort_parameter.replace('+', '-', 1)
        if self.sort_parameter[0]=='-':
            dir= self.sort_parameter.replace('-', '+', 1)
        return dir