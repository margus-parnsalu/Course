USERS = {'editor':'editor',
          'viewer':'viewer'}
GROUPS = {'editor':['group:editors']}

# Validate user login in view
def userfinder(userid, password):
    found = False
    if userid in USERS and USERS[userid]==password:
        found = True
    return found


def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])





