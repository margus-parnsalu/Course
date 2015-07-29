from pyramid.security import (Allow, Everyone)

USERS = {'editor':'editor',
          'viewer':'viewer'}
GROUPS = {'editor':['group:editors'],
          'gunnva@ET.EE':['group:editors'],
          'margusp@ET.EE':['group:editors']}

# Validate user login in view
def userfinder(userid, password):
    found = False
    if userid in USERS and USERS[userid]==password:
        found = True
    return found


def groupfinder(userid, request):
    return GROUPS.get(userid, [])


class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
    def __init__(self, request):
        pass





