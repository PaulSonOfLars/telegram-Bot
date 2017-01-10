#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
import logging
import configparser
import json
import os

# DECLARE STRINGS

# messages
msgHelp = """Hi! This bot is currently WIP. I'm working on it!
current commands are:
- /start the bot introduces itself.
- /hey prints a welcome string.
- /help prints this message.
- /owes <ower> <owee> <sum> tells you ower owes X to owee.
- /owe prints a list of all people owing money.
- /owe <ower> prints a list of all people being owed money to.
- /clear `all` clears the entire database of owed money.
- /clear <ower> `all` clears everything the ower owes.
- /clear <ower> <owee> clears the debt of ower towards owee.
- /idme returns your telegram ID."""
msgStart = "This is FinanceBot! He can help you take care of your house finances. Use /help for more info."
msgNoMoneyOwed = "Lucky... that person doesn't owe anything!"
msgListMoneyOwed = "Here is a list of people owing money:\n"
msgNoDebts = "Wow... there are no debts here!"
msgAllDebtsCleared = "All debts cleared!"
msgAllDebtsClearedTerm = msgAllDebtsCleared + " A backup file can be found in bckp.json."
# error strings
errNoFile = "Either file is missing or is not readable. Creating."
errBadFormat = "Command badly formatted. Use /help for help."
errNotInt = "You gave me an invalid sum! Please only use numbers/decimals (ie, dont specify the currency, this is specified by the owner.)"
errNotAdmin = "You are not admin! You can't run this command."
errNoOwer = "There is no-one here with this name: "
errAllName = "\"all\" cannot be used as a name!"

# INITIALISE
config = configparser.ConfigParser()
config.read("FinanceBot.ini")

global admin_ID
admin_ID= int(config["ADMIN"]["Telegram_ID"])

global currency
# set correct currency from config file. Should be in hexadecimal.
currency = unichr(int(config["SETTINGS"]["currency_code"], 16))

updater = Updater(config["KEYS"]["BOT_API_KEY"])
dispatcher = updater.dispatcher

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
def __repr__(self):
    return str(self)

# COMMON FUNCTIONS

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

# ACTUAL FUNCTIONS START HERE

def start(bot, update):
    update.message.reply_text(msgStart)

def help(bot, update):
    update.message.reply_text(msgHelp)

def print_owed(owed, chat_id, ower, res):
    for owee in owed[chat_id][ower]:
        val = owed[chat_id][ower][owee]
        res += "\n" + ower + " owes " + owee + " " + currency + str(val)

    return res

def owe(bot, update, args):
    owed = loadjson("./owed.json", "owed.json")
    chat_id = str(update.message.chat_id)
    
    try: owed
    except NameError: owed = {}
    
    try: owed[chat_id]
    except KeyError: owed[chat_id] = {}
    
    res = msgNoDebts
    if len(args) == 0: 
        if len(owed[chat_id]) == 0:
            res = msgNoDebts    
        else:
            res = msgListMoneyOwed
            for ower in owed[chat_id]:
                res = print_owed(owed, chat_id, ower, res)

    elif len(args) == 1:
        res = "Here is a list of everyone " + args[0] + " owes money to: \n"
        
        try:
            if len(owed[chat_id][args[0]]) == 0:
                raise KeyError
            res = print_owed(owed, chat_id, args[0], res)
        except KeyError: 
            res = msgNoMoneyOwed
    
    update.message.reply_text(res)

def clear(bot, update, args):
    owed = loadjson("./owed.json", "owed.json")
    chat_id = str(update.message.chat_id)
    sender = update.message.from_user
    
    if sender.id != admin_ID:
        update.message.reply_text(errNotAdmin)
        print ("User " + sender.username + " tried to issue an admin command.")
        return

    try: owed
    except NameError:
        owed = {}
        print ("Got empty err. Creating...")

    try: owed[chat_id]
    except KeyError:
        print ("No key found. Ignoring.")

    if len(args) == 1 and args[0] == "all":
            dumpjson("./bckp.json", owed)
            owed.pop(chat_id)
            update.message.reply_text(msgAllDebtsCleared)
            print(msgAllDebtsClearedTerm)

    elif len(args) == 2:
        try: owed[chat_id][args[0]]
        except KeyError:
            update.message.reply_text(errNoOwer + args[0])
            return

        if args[1] == "all":
            owed[chat_id].pop(args[0])
            print(args[0] + " had all debts cleared by the admin.")
        
        else:
            owed[chat_id][args[0]].pop(args[1])
            update.message.reply_text(args[0] + "'s debts to " + args[1] + " were cleared.")
            print(args[0] + " had debts to " + args[1] + " cleared by admin.")

            # remove from database if no debts
            if owed[chat_id] == {}:
                owed.pop(chat_id)
            elif owed[chat_id][args[0]] == {}:
                owed[chat_id].pop(args[0])

    else: 
        update.message.reply_text(errBadFormat)

    dumpjson("./owed.json", owed)
    

def owes(bot, update, args):
    owed = loadjson("./owed.json", "owed.json")
    chat_id = str(update.message.chat_id)
    
    try: owed
    except NameError: 
        owed = {}
        print("Got empty err. Creating...")
    
    try: owed[chat_id]
    except KeyError: 
        owed[chat_id] = {}
        print ("No key found. Creating...")
    
    if len(args) == 3:
        
        if args[0] == "all" or args[1] == "all":
            update.message.reply_text(errAllName)
            return

        try: float(args[2])
        except ValueError: update.message.reply_text(errNotInt)

        try: owed[chat_id][args[0]]
        except: 
            owed[chat_id][args[0]] = {}
            print("Added new ower: " + args[0] + ".")
        
        try: owed[chat_id][args[0]][args[1]]
        except: 
            owed[chat_id][args[0]][args[1]] = 0
            print("Added new owee for ower " + args[0] + ".")

        owed[chat_id][args[0]][args[1]] += float(args[2])
        
        # check whether owed sum is now 0 and removes if necessary
        if owed[chat_id][args[0]][args[1]] == 0:
            owed[chat_id][args[0]].pop(args[1])
    
    else:
        update.message.reply_text(errBadFormat)
    
    dumpjson("./owed.json", owed)   

def idme(bot, update):
    update.message.reply_text("Your ID is: " + str(update.message.from_user.id))

# LINK FUNCTIONS

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("clear", clear, pass_args=True))
updater.dispatcher.add_handler(CommandHandler("owe", owe, pass_args=True))
updater.dispatcher.add_handler(CommandHandler("owes", owes, pass_args=True))
updater.dispatcher.add_handler(CommandHandler("idme", idme))

updater.start_polling()
updater.idle()
