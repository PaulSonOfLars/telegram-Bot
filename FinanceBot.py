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
    owed = helper.loadjson(strings.loc_owedjson)
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
            res = strings.msgListMoneyOwedIndiv.format(args[0])
            res = helper.print_owed(owed, chat_id, args[0], res, currency)
        except KeyError:
            res = args[0] + " has no debts!"
    else:
        res = strings.errBadFormat
    update.message.reply_text(res)


def clear(bot, update, args):
    owed = helper.loadjson(strings.loc_owedjson)
    chat_id = str(update.message.chat_id)
    sender = update.message.from_user

    try: owed[chat_id]
    except KeyError: owed[chat_id] = {}

    if sender.id != owner_ID:
        update.message.reply_text(strings.errNotAdmin)
        print (strings.errUnauthCommand.format(sender.username))
        return

    if len(args) == 1 and args[0] == "all":
            helper.dumpjson(strings.loc_bckpjson, owed)
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
            print(strings.msgDebtsOfCleared.format(args[0]))

        else:
            owed[chat_id][args[0]].pop(args[1])
            update.message.reply_text(msgDebtsOfToCleared.format(args[0],
                                                                 args[1]))

            # remove from database if no debts
            if owed[chat_id] == {}:
                owed.pop(chat_id)
            elif owed[chat_id][args[0]] == {}:
                owed[chat_id].pop(args[0])

    else:
        update.message.reply_text(strings.errBadFormat)

    helper.dumpjson(strings.loc_owedjson, owed)


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
    owed = helper.loadjson(strings.loc_owedjson)
    chat_id = str(update.message.chat_id)

    if len(args) == 3:

        if args[0] == "all" or args[1] == "all":
            update.message.reply_text(strings.errAllName)
            return

        try: owesHelper(owed, chat_id, args[0], args[1], args[2])
        except ValueError: update.message.reply_text(strings.errNotInt)

    else:
        update.message.reply_text(strings.errBadFormat)

    helper.dumpjson(strings.loc_owedjson, owed)


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
    notes = helper.loadjson(strings.loc_notesjson)
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

    helper.dumpjson(strings.loc_notesjson, notes)


def getNote(bot, update, args):
    notes = helper.loadjson(strings.loc_notesjson)
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
    notes = helper.loadjson(strings.loc_notesjson)
    chat_id = str(update.message.chat_id)

    print(notes)

    try: notes[chat_id]
    except KeyError: notes[chat_id] = {}
    msg = "No notes in this chat."
    if len(notes[chat_id]) > 0:
        msg = strings.msgNotesForChat
        for note in notes[chat_id]:
            msg += "\n" + note

    update.message.reply_text(msg)


def unknown(bot, update, user_data):
    if update.message.text == "/iowes" :
        user_data.pop("ower")
        user_data.pop("owee")
        update.message.reply_text(strings.errCommandStillRunning)
        return ConversationHandler.END
    else:
        update.message.reply_text(strings.errUnknownCommand)


def inlineOwe(bot,update):
    owed = helper.loadjson(strings.loc_owedjson)
    chat_id = str(update.message.chat_id)

    try:
        keyboard = helper.makeKeyboard(owed[chat_id].keys(), "owers")
        reply = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(strings.msgListMoneyOwed,
                                  reply_markup=reply)
    except KeyError:
        update.message.reply_text(strings.msgNoDebts)


def cancel(bot,update, user_data):
    user_data.pop("ower")
    user_data.pop("owee")
    update.message.reply_text("Command cancelled",
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def create_ower(bot, update, user_data):
    ower = update.message.text
    user_data["ower"] = ower
    update.message.reply_text(strings.msgNewOwer.format(ower, ower))
    return OWEE


def create_owee(bot, update, user_data):
    owee = update.message.text
    ower = user_data["ower"]
    user_data["owee"] = owee
    update.message.reply_text(strings.msgNewOwee.format(owee,ower,ower,owee))
    return AMOUNT


def amount(bot,update, user_data):
    owed = helper.loadjson(strings.loc_owedjson)
    chat_id = str(update.message.chat_id)
    ower = user_data["ower"]
    owee = user_data["owee"]
    amount = update.message.text

    msg = ower + " now owes " + owee + " " + currency + amount + " more."
    try: owesHelper(owed, chat_id, ower, owee, amount) # save
    except ValueError: msg = strings.errNotInt

    update.message.reply_text(msg)

    helper.dumpjson(strings.loc_owedjson, owed)
    user_data.clear()
    return ConversationHandler.END


def inlineOwes(bot,update, user_data):
    owed = helper.loadjson(strings.loc_owedjson)
    chat_id = str(update.message.chat_id)
    try: keyboard = helper.makeKeyboard(owed[chat_id].keys(), "")
    except KeyError: keyboard = []

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(strings.msgCurrentOwers,
                              reply_markup=reply_markup)
    return OWER


def ower_button(bot, update, user_data):
    owed = helper.loadjson(strings.loc_owedjson)
    query = update.callback_query
    chat_id = str(query.message.chat_id)
    ower = query.data # this is the name pressed
    user_data["ower"] = ower

    try: keyboard = helper.makeKeyboard(owed[chat_id][ower].keys(), "")
    except KeyError: keyboard = []

    reply = InlineKeyboardMarkup(keyboard)
    bot.editMessageText(text=msgWhoOwedTo.format(ower),
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=reply)

    return OWEE


def owee_button(bot, update, user_data):
    owed = helper.loadjson(strings.loc_owedjson)
    query = update.callback_query
    chat_id = str(query.message.chat_id)
    ower = user_data["ower"]
    owee = query.data # this is the name pressed
    user_data["owee"] = owee

    bot.editMessageText(text=strings.msgHowMuch.format(ower,owee),
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

    return AMOUNT


def button(bot, update, user_data):
    query = update.callback_query
    chat_id = str(query.message.chat_id)

    messageHere = strings.errButtonMsg
    reply_markup = None

    if query.data.startswith("owers"):
        ower = query.data[5:]
        user_data["oweower"] = ower
        owed = helper.loadjson(strings.loc_owedjson)
        keyboard = helper.makeKeyboard(owed[chat_id][ower].keys(), "owees")

        messageHere = strings.msgListMoneyOwedIndiv.format(ower)
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif query.data.startswith("owees"):
        owed = helper.loadjson(strings.loc_owedjson)
        ower = user_data["oweower"]
        owee = query.data[5:]

        messageHere = ower + " owes " + owee + " " + currency \
                        + str(owed[chat_id][ower][owee])
        user_data.pop("oweower") # cleanup
    else:
        messageHere = strings.errUnknownCallback

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


    dispatcher.add_handler(CallbackQueryHandler(button, pass_user_data=True))

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
