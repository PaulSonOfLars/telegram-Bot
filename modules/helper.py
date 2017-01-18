#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import json
import os
from modules import strings
from telegram import InlineKeyboardButton
import FinanceBot


def loadjson(PATH):
    if not os.path.isfile(PATH) or not os.access(PATH, os.R_OK):
        print(strings.errNoFile)
        name = {}
        dumpjson(PATH, name)
    with open(PATH) as f:
        name = json.load(f)
    return name


def dumpjson(filename, var):
    with open(filename, "w") as f:
        json.dump(var, f)


def print_owed(owed, chat_id, ower, res):
    for owee in owed[chat_id][ower]:
        amount = owed[chat_id][ower][owee]
        res += "\n" + ower + " owes " + owee + " " + FinanceBot.currency + str(amount)

    return res


def makeKeyboard(data, callbackCode):
    colN = 3
    counter = 0
    keyboard=[]
    for elem in data:
        if counter%colN == 0:
            keyboard.append([])

        keyboard[counter//colN].append(InlineKeyboardButton(
                                            elem,
                                            callback_data=callbackCode + elem))
        counter += 1

    return keyboard
