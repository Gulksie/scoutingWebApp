import random
import pickle
from flask_login import UserMixin


def getID():
    while 1:
        # min and max for 32-bit int (python is unbound but whatever)
        id = random.randint(-2147483647, 2147483647)

        id = hex(id)
        if getUser(id) == None:
            break

    return id


def getUser(id):
    for user in users:
        if user.get_id() == id:
            return user

    return None


def getGUser(id):
    for user in users:
        if user.gID == id:
            return user

    return None


# Users
# Array should only contain User objects (Classes.User.User)
users = []


def loadUsers():
    global users
    try:
        with open('users.p', 'rb+') as f:
            users = pickle.load(f)
    except FileNotFoundError:
        # create the empty file and set users to blank array

        f = open('users.p', 'w+')
        f.close()
        users = []
    except EOFError:
        users = []


def saveUsers():
    with open('users.p', 'wb+') as f:
        pickle.dump(users, f)


def addUser(user):
    global users
    users.append(user)


class User(UserMixin):
    name = ""
    email = ""
    id = '0x0'
    gID = None

    # account level can be 0 or 1
    # level 0 is a standard user account, with acess to view team picklists but not edit
    # level 1 is a team admin level account, that can edit picklists anf stuff on teams
    accountLevel = 0

    team = 0

    def __init__(self, name, email, gID=None):
        self.name = name
        self.email = email
        self.gID = gID

        self.id = getID()

    def isGoogle(self):
        return self.gID != None
