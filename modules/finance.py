#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

""" This is the finance module, controlling all the money commands.

The data is stored in data/owed.json, which is loaded using some of the helper
functions.
"""

from telegram.ext import (ConversationHandler, MessageHandler, CommandHandler,
                          Filters, CallbackQueryHandler)
from telegram import InlineKeyboardMarkup, ReplyKeyboardRemove
from modules import helper, strings
import Bot

# give numbers for the ConversationHandler buttons used in /iowes
OWER, OWEE, AMOUNT = range(3)


def list_owed(bot, update, args):
    owed = helper.loadjson(loc_owedjson)
    chat_id = str(update.message.chat_id)
    reply_markup = None

    try:
        owed[chat_id]
    except KeyError:
        owed[chat_id] = {}

    if len(args) == 0:
        keyboard = helper.make_keyboard(owed[chat_id].keys(), "owers")
        reply_markup = InlineKeyboardMarkup(keyboard)
        res = msgListMoneyOwed

    elif len(args) == 1:
        if args[0] == "all": # if arg1 is "all", print all debts
            if len(owed[chat_id]) == 0:
                res = msgNoDebts
            else:
                res = msgListMoneyOwed
                for ower in owed[chat_id]:
                    res += helper.print_owed(owed, chat_id, ower)
        else: # else, print debts of name
            try:
                res = msgListMoneyOwedIndiv.format(args[0])
                res += helper.print_owed(owed, chat_id, args[0])
            except KeyError:
                res = args[0] + " has no debts!"

    else:
        res = strings.errBadFormat

    update.message.reply_text(res, reply_markup=reply_markup)


def clear(bot, update, args):
    owed = helper.loadjson(loc_owedjson)
    chat_id = str(update.message.chat_id)
    sender = update.message.from_user

    try:
        owed[chat_id]
    except KeyError:
        owed[chat_id] = {}

    if sender.id != Bot.OWNER_ID:
        update.message.reply_text(strings.errNotAdmin)
        print(strings.errUnauthCommand.format(sender.username))
        return

    if len(args) == 1 and args[0] == "all":
        helper.dumpjson(loc_bckpjson, owed)
        owed.pop(chat_id)
        update.message.reply_text(msgAllDebtsCleared)
        print(msgAllDebtsClearedTerm)

    elif len(args) == 2:
        try:
            owed[chat_id][args[0]]
        except KeyError:
            update.message.reply_text(strings.errNoOwer + args[0])
            return

        if args[1] == "all":
            owed[chat_id].pop(args[0])
            print(msgDebtsOfCleared.format(args[0]))

        else:
            owed[chat_id][args[0]].pop(args[1])
            update.message.reply_text(
                msgDebtsOfToCleared.format(args[0], args[1]))

            # remove from database if no debts
            if owed[chat_id] == {}:
                owed.pop(chat_id)
            elif owed[chat_id][args[0]] == {}:
                owed[chat_id].pop(args[0])

    else:
        update.message.reply_text(strings.errBadFormat)

    helper.dumpjson(loc_owedjson, owed)


def owes_helper(chat_id, ower, owee, amount):
    owed = helper.loadjson(loc_owedjson)

    try:
        owed[chat_id]
    except KeyError:
        owed[chat_id] = {}

    try:
        owed[chat_id][ower]
    except KeyError:
        owed[chat_id][ower] = {}
        print("Added new ower: " + ower + ".")

    try:
        owed[chat_id][ower][owee]
    except KeyError:
        owed[chat_id][ower][owee] = 0
        print("Added new owee for ower " + ower + ".")

    owed[chat_id][ower][owee] += float(amount)
    result = owed[chat_id][ower][owee]

    # check whether owed sum is now 0 and removes if necessary
    if owed[chat_id][ower][owee] == 0:
        owed[chat_id][ower].pop(owee)
        if owed[chat_id][ower] == {}:
            owed[chat_id].pop(ower)
            if owed[chat_id] == {}:
                owed.pop(chat_id)

    helper.dumpjson(loc_owedjson, owed)
    return result


def inline_owes(bot, update, args, user_data):
    owed = helper.loadjson(loc_owedjson)
    chat_id = str(update.message.chat_id)
    res = ""

    if len(args) == 0:
        try:
            keyboard = helper.make_keyboard(owed[chat_id].keys(), "")
            res = msgCurrentOwers
        except KeyError:
            res = msgNoDebts
            keyboard = []

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(res, reply_markup=reply_markup)
        return OWER

    elif len(args) == 1:
        if args[0] == "all":
            update.message.reply_text(strings.errAllName)
            return ConversationHandler.END

        try:
            res = msgWhoOwedTo.format(args[0])
            keyboard = helper.make_keyboard(owed[chat_id][args[0]].keys(), "")
        except KeyError:
            keyboard = []

        user_data["ower"] = args[0]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(res, reply_markup=reply_markup)
        return OWEE

    elif len(args) == 2:
        if args[0] == "all" or args[1] == "all":
            update.message.reply_text(strings.errAllName)
            return ConversationHandler.END
        user_data["ower"] = args[0]
        user_data["owee"] = args[1]
        update.message.reply_text(msgHowMuch.format(args[0], args[1]))
        return AMOUNT

    elif len(args) == 3:
        if args[0] == "all" or args[1] == "all":
            update.message.reply_text(strings.errAllName)
        else:
            try:
                amount = owes_helper(chat_id, args[0], args[1], args[2])
                update.message.reply_text(args[0] + " now owes " + args[1] + " " + \
                                          Bot.CURRENCY + str(amount) + ".")
            except ValueError:
                update.message.reply_text(strings.errNotInt)

    else:
        update.message.reply_text(strings.errBadFormat)

    return ConversationHandler.END



def cancel(bot, update, user_data):
    try:
        user_data.pop("ower")
        user_data.pop("owee")
    except KeyError:
        pass
    update.message.reply_text("Command cancelled",
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def create_ower(bot, update, user_data):
    ower = update.message.text
    user_data["ower"] = ower
    update.message.reply_text(msgNewOwer.format(ower, ower))
    return OWEE


def create_owee(bot, update, user_data):
    owee = update.message.text
    ower = user_data["ower"]
    user_data["owee"] = owee
    update.message.reply_text(msgNewOwee.format(owee, ower, ower, owee))
    return AMOUNT


def amount_owed(bot, update, user_data):
    chat_id = str(update.message.chat_id)
    ower = user_data["ower"]
    owee = user_data["owee"]
    amount = update.message.text

    try:
        amount = owes_helper(chat_id, ower, owee, amount) # save
        msg = ower + " now owes " + owee + " " + Bot.CURRENCY + str(amount) + "."
    except ValueError:
        msg = strings.errNotInt

    update.message.reply_text(msg)

    user_data.pop("ower")
    user_data.pop("owee")
    return ConversationHandler.END


def ower_button(bot, update, user_data):
    owed = helper.loadjson(loc_owedjson)
    query = update.callback_query
    chat_id = str(query.message.chat_id)
    ower = query.data # this is the name pressed
    user_data["ower"] = ower

    try:
        keyboard = helper.make_keyboard(owed[chat_id][ower].keys(), "")
    except KeyError:
        keyboard = []

    reply = InlineKeyboardMarkup(keyboard)
    bot.editMessageText(text=msgWhoOwedTo.format(ower),
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=reply)

    return OWEE


def owee_button(bot, update, user_data):
    query = update.callback_query
    ower = user_data["ower"]
    owee = query.data # this is the name pressed
    user_data["owee"] = owee

    bot.editMessageText(text=msgHowMuch.format(ower, owee),
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

    return AMOUNT


def list_owed_button(bot, update, user_data):
    query = update.callback_query
    chat_id = str(query.message.chat_id)

    message_here = strings.errButtonMsg
    reply_markup = None

    if query.data.startswith("owers"):
        ower = query.data[5:]
        user_data["oweower"] = ower
        owed = helper.loadjson(loc_owedjson)
        keyboard = helper.make_keyboard(owed[chat_id][ower].keys(), "owees")

        message_here = msgListMoneyOwedIndiv.format(ower)
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif query.data.startswith("owees"):
        owed = helper.loadjson(loc_owedjson)
        ower = user_data["oweower"]
        owee = query.data[5:]

        message_here = ower + " owes " + owee + " " + Bot.CURRENCY \
                        + str(owed[chat_id][ower][owee])
        user_data.pop("oweower") # cleanup
    else:
        message_here = strings.errUnknownCallback

    bot.editMessageText(text=message_here,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=reply_markup)


def reset_owes(bot, update, user_data):
    try:
        user_data.pop("ower")
        user_data.pop("owee")
    except KeyError:
        pass
    update.message.reply_text(strings.errCommandStillRunning,
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# define handlers
clear_handler = CommandHandler("clear", clear, pass_args=True)
owe_handler = CommandHandler("owe", list_owed, pass_args=True)
owes_buttons_handler = CallbackQueryHandler(list_owed_button, pass_user_data=True)
owes_handler = ConversationHandler(
    entry_points=[CommandHandler("owes",
                                 inline_owes,
                                 pass_args=True,
                                 pass_user_data=True)],

    states={
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
                                amount_owed,
                                pass_user_data=True)]
    },
    fallbacks=[CommandHandler("cancel",
                              cancel,
                              pass_user_data=True),
               CommandHandler("owes",
                              reset_owes,
                              pass_user_data=True)]
)

loc_owedjson = "./data/owed.json"
loc_bckpjson = "./data/bckp.json"

msgNoMoneyOwed = "Lucky... that person doesn't owe anything!"
msgListMoneyOwed = "Here is a list of people owing money:\n"
msgListMoneyOwedIndiv = "Here is a list of everyone {} owes money to: \n"

msgHowMuch = "How much does {} owe {}? Please type a number."
msgNewOwer = "{} was saved as a new ower. Please input the name of the person that {} owes money to."
msgNewOwee = "{} was saved as a new owee for {}. " + msgHowMuch
msgCurrentOwers = "Here is the current list of people who owe money. Please select one, or reply with a new name to add a new ower."
msgWhoOwedTo = "Who does {} owe money to? Type in a new name to add a new owee."

msgNoDebts = "Wow... there are no debts here!"
msgAllDebtsCleared = "All debts cleared!"
msgAllDebtsClearedTerm = msgAllDebtsCleared + " A backup file can be found in bckp.json."
msgDebtsOfCleared = "{} had all debts cleared by the owner."
msgDebtsOfToCleared = "{}'s debts to {} were cleared."
