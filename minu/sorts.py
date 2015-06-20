#Dictionary of allowed sorting values for SqlAlchemy order_by
SORT_DICT = {
                '1': '1',
                '0': '0',
                'department':'hr_departments.department_name',
             }

class SortValue:

    def __init__(self, sort_parameter, direction):
        self.sort_parameter=sort_parameter
        self.direction=direction

    def sort_str(self):
        sort = SORT_DICT.get(self.sort_parameter, '')
        sortstr=''
        #If there is mach in URL query value
        if sort != '':
            if self.direction=='0':
                dirstr='DESC'
            else:
                dirstr='ASC'
            sortstr=('UPPER(%s) %s' % (sort, dirstr))
        return sortstr

    def reverse_direction(self):
        if self.direction=='1':
            dir='0'
        elif self.direction=='0':
            dir='1'
        else:
            dir='1'
        return dir