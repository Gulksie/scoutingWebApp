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
    with open('users.p', 'rb+') as f:
        users = pickle.load(f)


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

    def __init__(self, name, email, gID=None):
        self.name = name
        self.email = email
        self.gID = gID

        self.id = getID()

    def isGoogle(self):
        return self.gID != None
