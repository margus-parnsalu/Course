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

    #URL Query attribute validation
    def validate(self):
        if self.sort_parameter in SORT_DICT:
            return True
        return False

    #Return validated order_by string or None
    def sort_str(self):
        if self.validate() is True:
            return SORT_DICT[self.sort_parameter]
        return ''

    #Reverses sort direction
    def reverse_direction(self):
        dir = ''
        if self.sort_parameter[0] == '+':
            dir = self.sort_parameter.replace('+', '-', 1)
        if self.sort_parameter[0] == '-':
            dir = self.sort_parameter.replace('-', '+', 1)
        return dir