import json
import os
import strings

def loadjson(PATH, filename):
    if not os.path.isfile(PATH) or not os.access(PATH, os.R_OK):
        print(strings.errNoFile)
        name = {}
        dumpjson(filename, name)
    with open(filename) as f:
        name = json.load(f)
    return name

def dumpjson(filename, var):
    with open(filename, "w") as f:
        json.dump(var, f)

def print_owed(owed, chat_id, ower, res, currency):
    for owee in owed[chat_id][ower]:
        amount = owed[chat_id][ower][owee]
        res += "\n" + ower + " owes " + owee + " " + currency + str(amount)

    return res
