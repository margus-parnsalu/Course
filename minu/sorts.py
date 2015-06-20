#Dictionary of allowed sorting values for SqlAlchemy order_by
SORT_DICT = {'department':'hr_departments.department_name',
             }

class SortValue:

    def __init__(self, sort_parameter, direction):
        self.sort_parameter=sort_parameter
        self.direction=direction

    def sort_str(self):
        order = SORT_DICT.get(self.sort_parameter, '')
        if self.direction=='0':
            sort='DESC'
        else:
            sort='ASC'
        return ('UPPER(%s) %s' % (order, sort))

    def reverse_direction(self):
        if self.direction=='1':
            dir='0'
        elif self.direction=='0':
            dir='1'
        else:
            dir='1'
        return dir