#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
import logging
import configparser
import json
import os

# DECLARE STRINGS

msgHelp = """Hi! This bot is currently WIP. I'm working on it!
current commands are:
- /start the bot introduces itself.
- /hey prints a welcome string.
- /help prints this message.
- /owes <ower> <owee> <sum> tells you ower owes X to owee.
- /owes <ower> 'clear' resets all the ower's debts.
- /owes <ower> <owee> 'clear' resets the ower's debts towards the owee.
- /owes 'clearall' clears all debts.
- /owe prints a list of all people owing money.
- /owe <ower> prints a list of all people being owed money to.
- /idme returns your telegram ID."""
msgWelcome = "Hello to you too!"
msgStart = "This is FinanceBot! He can help you take care of your house finances. Use /help for more info."
msgNoMoneyOwed = "Lucky... that person doesn't owe anything!"
msgListMoneyOwed = "Here is a list of people owing money:\n"
msgNoDebts = "Wow... there are no debts here!"

errNoFile = "Either file is missing or is not readable. Creating."
errBadFormat = "Command badly formatted. Use /help for help."
errNotInt = "You gave me an invalid sum! Please only use numbers/decimals (ie, dont specify the currency, this is specified by the owner.)"

# INITIALISE
config = configparser.ConfigParser()
config.read("FinanceBot.ini")

global my_ID
my_ID= int(config["ADMIN"]["Telegram_ID"])

global currency
# currency = config["SETTINGS"]["currency_code"].decode("utf-8")
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

def hey(bot, update): 
    update.message.reply_text(msgWelcome)

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
    if len(args) == 0 and len(owed[chat_id]) > 0:
        res = msgListMoneyOwed
        for ower in owed[chat_id]:
            res = print_owed(owed, chat_id, ower, res)

    elif len(args) == 1:
        res = "here is a list of everyone " + args[0] + " owes money to: \n"
        
        try:
            if len(owed[chat_id][args[0]]) == 0:
                raise KeyError
            res = print_owed(owed, chat_id, args[0], res)
        except KeyError: 
            res = msgNoMoneyOwed
    
    update.message.reply_text(res)

def owes(bot, update, args):
    owed = loadjson("./owed.json", "owed.json")
    chat_id = str(update.message.chat_id)
    #print(update.message.from_user.id)
    #print(my_ID)
    
    try: owed
    except NameError: 
        owed = {}
        print("Got empty err. Creating...")
    
    try: owed[chat_id]
    except KeyError: 
        owed[chat_id] = {}
        print ("No key found. Creating...")
    
    if len(args) == 1 and update.message.from_user.id == my_ID and args[0] == "clearall":
            owed[chat_id] = {}
    
    elif len(args) == 2 and update.message.from_user.id == my_ID and args[1] == "clear":
            print(args[0] + " had all debts cleared by the admin.")
            owed[chat_id][args[0]] = {}

    elif len(args) == 3:
        
        if args[2] == "clear" and update.message.from_user.id == my_ID:
            print(args[0] + " had debts to " + args[1] + " cleared by admin.")
            owed[chat_id][args[0]].pop(args[1]) # duplicate N1
        
        else:
            try: float(args[2])
            except ValueError: update.message.reply_text(errNotInt)

            try: owed[chat_id][args[0]]
            except: 
                owed[chat_id][args[0]] = {}
                print("got new ower: " + args[0] + ".")
        
            try: owed[chat_id][args[0]][args[1]]
            except: 
                owed[chat_id][args[0]][args[1]] = 0
                print("got new owee for ower " + args[0] + ".")

            owed[chat_id][args[0]][args[1]] += float(args[2])

            if owed[chat_id][args[0]][args[1]] == 0:
                owed[chat_id][args[0]].pop(args[1]) # duplicate N1
    else:
        update.message.reply_text(errBadFormat)
    
    dumpjson("./owed.json", owed)   

def idme(bot, update):
    update.message.reply_text("Your ID is: " + str(update.message.from_user.id))

# LINK FUNCTIONS

updater.dispatcher.add_handler(CommandHandler("hey", hey))
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("owe", owe, pass_args=True))
updater.dispatcher.add_handler(CommandHandler("owes", owes, pass_args=True))
updater.dispatcher.add_handler(CommandHandler("idme", idme))

updater.start_polling()
updater.idle()
