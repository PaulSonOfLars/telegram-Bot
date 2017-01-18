#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

from telegram.ext import ConversationHandler
from telegram import InlineKeyboardMarkup, ReplyKeyboardRemove
from modules import helper, strings
import FinanceBot


def owe(bot, update, args):
    owed = helper.loadjson(strings.loc_owedjson)
    chat_id = str(update.message.chat_id)

    try:
        owed[chat_id]
    except KeyError:
        owed[chat_id] = {}

    res = strings.msgNoDebts
    if len(args) == 0:
        if len(owed[chat_id]) == 0:
            res = strings.msgNoDebts
        else:
            res = strings.msgListMoneyOwed
            for ower in owed[chat_id]:
                res = helper.print_owed(owed, chat_id, ower, res)

    elif len(args) == 1:
        try:
            res = strings.msgListMoneyOwedIndiv.format(args[0])
            res = helper.print_owed(owed, chat_id, args[0], res)
        except KeyError:
            res = args[0] + " has no debts!"
    else:
        res = strings.errBadFormat
    update.message.reply_text(res)


def clear(bot, update, args):
    owed = helper.loadjson(strings.loc_owedjson)
    chat_id = str(update.message.chat_id)
    sender = update.message.from_user

    try:
        owed[chat_id]
    except KeyError:
        owed[chat_id] = {}

    if sender.id != FinanceBot.OWNER_ID:
        update.message.reply_text(strings.errNotAdmin)
        print(strings.errUnauthCommand.format(sender.username))
        return

    if len(args) == 1 and args[0] == "all":
        helper.dumpjson(strings.loc_bckpjson, owed)
        owed.pop(chat_id)
        update.message.reply_text(strings.msgAllDebtsCleared)
        print(strings.msgAllDebtsClearedTerm)

    elif len(args) == 2:
        try:
            owed[chat_id][args[0]]
        except KeyError:
            update.message.reply_text(strings.errNoOwer + args[0])
            return

        if args[1] == "all":
            owed[chat_id].pop(args[0])
            print(strings.msgDebtsOfCleared.format(args[0]))

        else:
            owed[chat_id][args[0]].pop(args[1])
            update.message.reply_text(
                strings.msgDebtsOfToCleared.format(args[0], args[1]))

            # remove from database if no debts
            if owed[chat_id] == {}:
                owed.pop(chat_id)
            elif owed[chat_id][args[0]] == {}:
                owed[chat_id].pop(args[0])

    else:
        update.message.reply_text(strings.errBadFormat)

    helper.dumpjson(strings.loc_owedjson, owed)


def owes_helper(owed, chat_id, ower, owee, amount):

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

        try:
            owes_helper(owed, chat_id, args[0], args[1], args[2])
        except ValueError:
            update.message.reply_text(strings.errNotInt)

    else:
        update.message.reply_text(strings.errBadFormat)

    helper.dumpjson(strings.loc_owedjson, owed)


def inline_owe(bot, update):
    owed = helper.loadjson(strings.loc_owedjson)
    chat_id = str(update.message.chat_id)

    try:
        keyboard = helper.make_keyboard(owed[chat_id].keys(), "owers")
        reply = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(strings.msgListMoneyOwed,
                                  reply_markup=reply)
    except KeyError:
        update.message.reply_text(strings.msgNoDebts)


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
    update.message.reply_text(strings.msgNewOwer.format(ower, ower))
    return FinanceBot.OWEE


def create_owee(bot, update, user_data):
    owee = update.message.text
    ower = user_data["ower"]
    user_data["owee"] = owee
    update.message.reply_text(strings.msgNewOwee.format(owee, ower, ower, owee))
    return FinanceBot.AMOUNT


def amount_owed(bot, update, user_data):
    owed = helper.loadjson(strings.loc_owedjson)
    chat_id = str(update.message.chat_id)
    ower = user_data["ower"]
    owee = user_data["owee"]
    amount = update.message.text

    msg = ower + " now owes " + owee + " " + FinanceBot.CURRENCY + amount + " more."
    try:
        owes_helper(owed, chat_id, ower, owee, amount) # save
    except ValueError:
        msg = strings.errNotInt

    update.message.reply_text(msg)

    helper.dumpjson(strings.loc_owedjson, owed)
    user_data.clear()
    return ConversationHandler.END


def inline_owes(bot, update):
    owed = helper.loadjson(strings.loc_owedjson)
    chat_id = str(update.message.chat_id)
    try:
        keyboard = helper.make_keyboard(owed[chat_id].keys(), "")
    except KeyError:
        keyboard = []

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(strings.msgCurrentOwers,
                              reply_markup=reply_markup)
    return FinanceBot.OWER


def ower_button(bot, update, user_data):
    owed = helper.loadjson(strings.loc_owedjson)
    query = update.callback_query
    chat_id = str(query.message.chat_id)
    ower = query.data # this is the name pressed
    user_data["ower"] = ower

    try:
        keyboard = helper.make_keyboard(owed[chat_id][ower].keys(), "")
    except KeyError:
        keyboard = []

    reply = InlineKeyboardMarkup(keyboard)
    bot.editMessageText(text=strings.msgWhoOwedTo.format(ower),
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=reply)

    return FinanceBot.OWEE


def owee_button(bot, update, user_data):
    query = update.callback_query
    ower = user_data["ower"]
    owee = query.data # this is the name pressed
    user_data["owee"] = owee

    bot.editMessageText(text=strings.msgHowMuch.format(ower, owee),
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

    return FinanceBot.AMOUNT


def owebutton(bot, update, user_data):
    query = update.callback_query
    chat_id = str(query.message.chat_id)

    message_here = strings.errButtonMsg
    reply_markup = None

    if query.data.startswith("owers"):
        ower = query.data[5:]
        user_data["oweower"] = ower
        owed = helper.loadjson(strings.loc_owedjson)
        keyboard = helper.make_keyboard(owed[chat_id][ower].keys(), "owees")

        message_here = strings.msgListMoneyOwedIndiv.format(ower)
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif query.data.startswith("owees"):
        owed = helper.loadjson(strings.loc_owedjson)
        ower = user_data["oweower"]
        owee = query.data[5:]

        message_here = ower + " owes " + owee + " " + FinanceBot.CURRENCY \
                        + str(owed[chat_id][ower][owee])
        user_data.pop("oweower") # cleanup
    else:
        message_here = strings.errUnknownCallback

    bot.editMessageText(text=message_here,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=reply_markup)
