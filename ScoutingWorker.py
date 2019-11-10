from os import makedirs, path
from json import load, dump


# first thing is to create all folders (teams)
# TODO: once team-account association is made, this needs to check for folders for all teams (rather than just 4618)

makedirs("teams/4618", exist_ok=True)

# TODO: next step is to check for a template
# this SHOULD be user generated using a whole custom thing but that would require team associations and different account levels and i would like to sleep tonight


# next step: we need to accept JSON data and save/merge it for later use
def saveData(team, data):
    todump = [data]
    folder = "teams/" + str(team) + "//"

    file_ = folder + str(data['match']) + '.json'

    if (path.isfile(file_)):
        with open(file_, 'r+') as f:
            jsonData = load(f)

        todump += jsonData

    with open(file_, 'w+') as f:
        dump(todump, f, indent=4)
