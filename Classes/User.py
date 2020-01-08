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


def getTeamByNumber(number):
    for team in teams:
        if team.number == number:
            return team

    return None


def createTeam(number, member):
    team = Team(number, member)
    teams.append(team)
    return team


class User(UserMixin):
    name = ""
    email = ""
    id = '0x0'
    gID = None
    hasInit = False

    # account level can be 0, 1, or 2
    # level 0 is waiting to be accepted onto a team by an admin, can't do anything really
    # level 1 is a standard user account, with acess to view team picklists but not edit
    # level 2 is a team admin level account, that can edit picklists anf stuff on teams
    accountLevel = 0

    team = None

    def __init__(self, name, email, gID=None):
        self.name = name
        self.email = email
        self.gID = gID

        self.id = getID()

        self.team = getTeamByNumber(0)

    def isGoogle(self):
        return self.gID is not None

    def initUser(self, team):
        self.team = getTeamByNumber(team)

        if self.team is None:
            self.team = createTeam(team, self)
            self.accountLevel = 2

        else:
            self.team.applicants.append(self)
            self.accountLevel = 0

        self.hasInit = True


class Team:
    number = 0
    applicants = []
    members = []
    admins = []

    def __init__(self, number, member):
        self.number = number

        if number == 0:  # special case, i want everyone to be able to demo with this account
                         # dont know how i want to do that yet
            return

        self.members.append(member)
        self.admins.append(member)


# Users
# Array should only contain User objects (Classes.User.User)
users = []

# Teams
# Should only contain (Classes.User.Team)
teams = [Team(0, None)]
