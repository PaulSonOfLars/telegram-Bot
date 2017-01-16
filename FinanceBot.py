#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, ConversationHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
import logging
import configparser
import json
import helper
import strings
import subprocess
import os

# INITIALISE

# enable logging
logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO)

logger=logging.getLogger(__name__)

OWER, OWEE, AMOUNT = range(3)

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
    owed = helper.loadjson("./data/owed.json")
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
    else:
        res = strings.errBadFormat
    update.message.reply_text(res)


def clear(bot, update, args):
    owed = helper.loadjson("./data/owed.json")
    chat_id = str(update.message.chat_id)
    sender = update.message.from_user

    try: owed[chat_id]
    except KeyError: owed[chat_id] = {}

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

    helper.dumpjson("./data/owed.json", owed)


def owesHelper(owed, chat_id, ower, owee, amount):

    try: owed[chat_id]
    except KeyError: owed[chat_id] = {}

    try: owed[chat_id][ower]
    except:
        owed[chat_id][ower] = {}
        print("Added new ower: " + ower + ".")

    try: owed[chat_id][ower][owee]
    except:
        owed[chat_id][ower][owee] = 0
        print("Added new owee for ower " + ower + ".")

    owed[chat_id][ower][owee] += float(amount)

    # check whether owed sum is now 0 and removes if necessary
    if owed[chat_id][ower][owee] == 0:
        owed[chat_id][ower].pop(owee)
        if owed[chat_id][ower] == {}:
            owed[chat_id].pop(ower)
            if owed[chat_id] == {}:
                owed.pop(chat_id)


def owes(bot, update, args):
    owed = helper.loadjson("./data/owed.json")
    chat_id = str(update.message.chat_id)

    if len(args) == 3:

        if args[0] == "all" or args[1] == "all":
            update.message.reply_text(strings.errAllName)
            return

        try: owesHelper(owed, chat_id, args[0], args[1], args[2])
        except ValueError: update.message.reply_text(strings.errNotInt)

    else:
        update.message.reply_text(strings.errBadFormat)

    helper.dumpjson("./data/owed.json", owed)


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


def saveNote(bot, update, args):
    notes = helper.loadjson("./data/notes.jsonn")
    chat_id = str(update.message.chat_id)

    try: notes[chat_id]
    except KeyError: notes[chat_id] = {}

    if len(args) >= 2:
        # add note to note repo
        notename = args[0]
        del args[0]
        noteData = " ".join(args)
        notes[chat_id][notename]= noteData
        print("Added new note \"" + notename + "\" with content \"" \
                + noteData + "\"." )
    else:
        update.message.reply_text(strings.errBadFormat)

    helper.dumpjson("./notes.json", notes)


def getNote(bot, update, args):
    notes = helper.loadjson("./data/notes.jsonn")
    chat_id = str(update.message.chat_id)

    try: notes[chat_id]
    except KeyError: notes[chat_id] = {}

    if len(args) == 1:
        msg = ""
        try:
            msg = notes[chat_id][args[0]]

        except KeyError:
            msg = strings.errNoNoteFound + args[0]

        update.message.reply_text(msg)
    else:
        update.message.reply_text(strings.errBadFormat)


def allNotes(bot, update, args):
    notes = helper.loadjson("./data/notes.jsonn")
    chat_id = str(update.message.chat_id)

    try: notes[chat_id]
    except KeyError: notes[chat_id] = {}

    msg = "These are the notes I have saved for this chat: \n"
    for note in notes[chat_id]:
        msg += "\n" + note

    update.message.reply_text(msg)


def unknown(bot, update, user_data):
    if update.message.text == "/iowes" :
        user_data.clear()
        update.message.reply_text(strings.errCommandStillRunning)
        return ConversationHandler.END
    else:
        update.message.reply_text(strings.errUnknownCommand)


def inlineOwe(bot,update):
    owed = helper.loadjson("./data/owed.json")
    chat_id = str(update.message.chat_id)

    try:
        keyboard = makeKeyboard(owed[chat_id].keys(), "owers")
        reply = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("here are the people who owe money:",
                                  reply_markup=reply)
    except KeyError:
        update.message.reply_text(strings.msgNoDebts)


def cancel(bot,update, user_data):
    user_data.clear()
    update.message.reply_text("Command cancelled",
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def create_ower(bot, update, user_data):
    owername = update.message.text
    user_data["ower"] = owername
    update.message.reply_text(owername + " was saved as a new ower. Please" \
                              + "input a new owee for this ower.")
    return OWEE


def create_owee(bot, update, user_data):
    owee = update.message.text
    ower = user_data["ower"]
    user_data["owee"] = owee
    update.message.reply_text(owee + " was saved as a new owee for user " \
                              + ower + ". How much does " + ower + " owe " \
                              + owee + "? Please type a number.")
    return AMOUNT


def amount(bot,update, user_data):
    owed = helper.loadjson("./data/owed.json")
    chat_id = str(update.message.chat_id)
    ower = user_data["ower"]
    owee = user_data["owee"]
    amount = update.message.text

    msg = ower + " now owes " + owee + " " + currency + amount + " more."
    try: owesHelper(owed, chat_id, ower, owee, amount) # save
    except ValueError: msg = strings.errNotInt

    update.message.reply_text(msg)

    helper.dumpjson("./data/owed.json", owed)
    user_data.clear()
    return ConversationHandler.END

def inlineOwes(bot,update, user_data):
    owed = helper.loadjson("./data/owed.json")
    chat_id = str(update.message.chat_id)
    try: keyboard = makeKeyboard(owed[chat_id].keys(), "")
    except KeyError: keyboard = []

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Here is the current list of people who owe " \
                              + "money. Please select one, or reply with a " \
                              + "new name to add a new ower.",
                              reply_markup=reply_markup)
    return OWER


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

def ower_button(bot, update, user_data):
    owed = helper.loadjson("./data/owed.json")
    query = update.callback_query
    chat_id = str(query.message.chat_id)
    ower = query.data # this is the name pressed
    user_data["ower"] = ower

    try: keyboard = makeKeyboard(owed[chat_id][ower].keys(), "")
    except KeyError: keyboard = []

    reply = InlineKeyboardMarkup(keyboard)
    bot.editMessageText(text="Who does " + ower + " owe money to? type in a" \
                             + "new name to add a new owee.",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=reply)

    return OWEE

def owee_button(bot, update, user_data):
    owed = helper.loadjson("./data/owed.json")
    query = update.callback_query
    chat_id = str(query.message.chat_id)
    ower = user_data["ower"]
    owee = query.data # this is the name pressed
    user_data["owee"] = owee

    bot.editMessageText(text="How much money does " + ower + " owe to " \
                              + owee + "? Please type number.",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

    return AMOUNT

def button(bot, update):
    query = update.callback_query
    chat_id = str(query.message.chat_id)

    messageHere ="Error. Message not set after button call."
    reply_markup = None

    if query.data.startswith("owers"):
        ower = query.data[5:]
        owed = helper.loadjson("./data/owed.json")
        keyboard = makeKeyboard(owed[chat_id][ower], "owees")

        messageHere = ower + " owes money to these people:"
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif query.data.startswith("owees"):
        owed = helper.loadjson("./data/owed.json")
        ower = query.message.text.split(" ",1)[0]
        owee = query.data[5:]

        messageHere = ower + " owes " + owee + " " + currency \
                        + str(owed[chat_id][ower][owee])

    else:
        messageHere = "unrecognised callback code"

    bot.editMessageText(text=messageHere,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=reply_markup)


def main():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    if not os.path.exists("./data/"):
        os.makedirs("data")

    config = configparser.ConfigParser()
    config.read("FinanceBot.ini")

    global owner_ID
    owner_ID = int(config["OWNER"]["Telegram_ID"])

    global currency
    currency = config["SETTINGS"]["currency_code"]

    updater = Updater(config["KEYS"]["BOT_API_KEY"])
    dispatcher = updater.dispatcher

    # LINK FUNCTIONS

    iowes_ConversationHandler = ConversationHandler(
        entry_points=[CommandHandler("iowes",
                                     inlineOwes,
                                     pass_user_data=True)],

        states = {
            OWER: [MessageHandler(Filters.text,
                                      create_ower,
                                      pass_user_data=True),
                       CallbackQueryHandler(ower_button,
                                            pass_user_data=True)],

            OWEE: [MessageHandler(Filters.text,
                                      create_owee,
                                      pass_user_data=True),
                       CallbackQueryHandler(owee_button,
                                            pass_user_data=True)],

            AMOUNT: [MessageHandler(Filters.text,
                                    amount,
                                    pass_user_data=True)]
        },
        fallbacks=[CommandHandler("cancel",
                                  cancel,
                                  pass_user_data=True),
                   MessageHandler(Filters.command,
                                  unknown,
                                  pass_user_data=True)]
    )

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("clear", clear, pass_args=True))
    dispatcher.add_handler(CommandHandler("owe", owe, pass_args=True))
    dispatcher.add_handler(CommandHandler("owes", owes, pass_args=True))
    dispatcher.add_handler(CommandHandler("idme", idme))
    dispatcher.add_handler(CommandHandler("botip", getBotIp))
    dispatcher.add_handler(CommandHandler("save", saveNote, pass_args=True))
    dispatcher.add_handler(CommandHandler("get", getNote, pass_args=True))
    dispatcher.add_handler(CommandHandler("note", allNotes, pass_args=True))
    dispatcher.add_handler(CommandHandler("iowe", inlineOwe))
    dispatcher.add_handler(iowes_ConversationHandler)


    dispatcher.add_handler(CallbackQueryHandler(button))

    #unknown commands, leave last.
    dispatcher.add_handler(MessageHandler(Filters.command,
                                          unknown,
                                          pass_user_data=True))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

# run main if run as script
if __name__ == '__main__':
    main()
