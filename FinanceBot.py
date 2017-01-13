#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
import logging
import configparser
import json
import helper
import strings
import subprocess

# INITIALISE
logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO)

config = configparser.ConfigParser()
config.read("FinanceBot.ini")

global owner_ID
owner_ID = int(config["OWNER"]["Telegram_ID"])

global currency
currency = config["SETTINGS"]["currency_code"]

updater = Updater(config["KEYS"]["BOT_API_KEY"])
dispatcher = updater.dispatcher

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
    update.message.reply_text(strings.errUnknown)

def __repr__(self):
    return str(self)

# ACTUAL FUNCTIONS START HERE

def start(bot, update):
    update.message.reply_text(strings.msgStart)


def help(bot, update):
    update.message.reply_text(strings.msgHelp)


def owe(bot, update, args):
    owed = helper.loadjson("./owed.json", "owed.json")
    chat_id = str(update.message.chat_id)
    
    try: owed[chat_id]
    except KeyError: owed[chat_id] = {}
    
    res = strings.msgNoDebts
    if len(args) == 0: 
        if len(owed[chat_id]) == 0:
            res = strings.msgNoDebts    
        else:
            res = strings.msgListMoneyOwed
            for ower in owed[chat_id]:
                res = helper.print_owed(owed, chat_id, ower, res, currency)

    elif len(args) == 1:
        try: 
            res = "Here is a list of everyone " + args[0] \
                  + " owes money to: \n"
            res = helper.print_owed(owed, chat_id, args[0], res, currency)
        except KeyError:
            res = args[0] + " has no debts!"
    update.message.reply_text(res)


def clear(bot, update, args):
    owed = helper.loadjson("./owed.json", "owed.json")
    chat_id = str(update.message.chat_id)
    sender = update.message.from_user
    
    if sender.id != owner_ID:
        update.message.reply_text(strings.errNotAdmin)
        print ("User " + sender.username + " tried to issue an owner command.")
        return

    if len(args) == 1 and args[0] == "all":
            helper.dumpjson("./bckp.json", owed)
            owed.pop(chat_id)
            update.message.reply_text(strings.msgAllDebtsCleared)
            print(strings.msgAllDebtsClearedTerm)

    elif len(args) == 2:
        try: owed[chat_id][args[0]]
        except KeyError:
            update.message.reply_text(strings.errNoOwer + args[0])
            return

        if args[1] == "all":
            owed[chat_id].pop(args[0])
            print(args[0] + " had all debts cleared by the owner.")
        
        else:
            owed[chat_id][args[0]].pop(args[1])
            update.message.reply_text(args[0] + "'s debts to " \
                                      + args[1] + " were cleared.")
            print(args[0] + " had debts to " + args[1] + " cleared by owner.")

            # remove from database if no debts
            if owed[chat_id] == {}:
                owed.pop(chat_id)
            elif owed[chat_id][args[0]] == {}:
                owed[chat_id].pop(args[0])

    else: 
        update.message.reply_text(strings.errBadFormat)

    helper.dumpjson("./owed.json", owed)
    

def owes(bot, update, args):
    owed = helper.loadjson("./owed.json", "owed.json")
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
            update.message.reply_text(strings.errAllName)
            return

        try: float(args[2])
        except ValueError: update.message.reply_text(strings.errNotInt)

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
        # also this makes a nice shape if you have tabs = 4
        if owed[chat_id][args[0]][args[1]] == 0:
            owed[chat_id][args[0]].pop(args[1])
            if owed[chat_id][args[0]] == {}:
                owed[chat_id].pop(args[0])
                if owed[chat_id] == {}:
                    owed.pop(chat_id)
    
    else:
        update.message.reply_text(strings.errBadFormat)
    
    helper.dumpjson("./owed.json", owed)   


def idme(bot, update):
    update.message.reply_text("Your ID is: " \
                               + str(update.message.from_user.id))


def getBotIp(bot, update):
    sender = update.message.from_user
    if sender.id == owner_ID:
        msgToSend = ""
        try: 
            ip_string = subprocess.check_output(["curl", "ipinfo.io/ip"],
                                                 universal_newlines=True,
                                                 timeout=5)
            msgToSend = strings.msgIpAddress + ip_string
        except CalledProcessError: msgToSend = strings.errUnknown
        except TimeoutExpired: msgToSend = strings.errTimeout 
        update.message.reply_text(msgToSend)


# LINK FUNCTIONS

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler("clear", clear, pass_args=True))
dispatcher.add_handler(CommandHandler("owe", owe, pass_args=True))
dispatcher.add_handler(CommandHandler("owes", owes, pass_args=True))
dispatcher.add_handler(CommandHandler("idme", idme))
dispatcher.add_handler(CommandHandler("botip", getBotIp))
dispatcher.add_handler(CommandHandler("idme", idme))

updater.start_polling()
updater.idle()
