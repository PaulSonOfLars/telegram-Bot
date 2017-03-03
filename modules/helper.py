#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
""" This is the helper file.

Functions that are commonly used accross multiple modules are found here.
"""
import json
import os
from modules import strings
from telegram import InlineKeyboardButton
import Bot


def loadjson(path):
    if not os.path.isfile(path) or not os.access(path, os.R_OK):
        print(strings.errNoFile)
        name = {}
        dumpjson(path, name)
    with open(path) as file:
        name = json.load(file)
    return name


def dumpjson(filename, var):
    with open(filename, "w") as file:
        json.dump(var, file)


def print_owed(owed, chat_id, ower):
    res = ""
    for owee in owed[chat_id][ower]:
        amount = owed[chat_id][ower][owee]
        res += "\n" + ower + " owes " + owee + " " + Bot.CURRENCY + str(amount)

    return res


def make_keyboard(data, callback_code):
    max_col_n = 3
    counter = 0
    keyboard = []
    for elem in data:
        if counter%max_col_n == 0:
            keyboard.append([])
                                    # // is used for integer division
        keyboard[counter//max_col_n].append(InlineKeyboardButton(
            elem,
            callback_data=callback_code + elem))
        counter += 1

    return keyboard
