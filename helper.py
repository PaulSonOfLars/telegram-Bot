import json
import os


def loadjson(PATH, filename):
    if not os.path.isfile(PATH) or not os.access(PATH, os.R_OK):
        print(errNoFile)
        name = {}
        with open(filename, "w") as f:
            json.dump(name, f)
    with open(filename) as f:
        name = json.load(f)
    return name

def dumpjson(filename, var):
    with open(filename, "w") as f:
        json.dump(var, f)

def print_owed(owed, chat_id, ower, res, currency):
    for owee in owed[chat_id][ower]:
        val = owed[chat_id][ower][owee]
        res += "\n" + ower + " owes " + owee + " " + currency + str(val)
                            
    return res

