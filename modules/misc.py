#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
""" This is the miscellaneous commands module.

It is full of small, helpful functions that don't quite need a full module
and that a user might use for information.
"""
from telegram.ext import CommandHandler
from subprocess import check_output, CalledProcessError, TimeoutExpired
from modules import strings
import Bot


def start(bot, update):
    """ First command a bot receives."""
    update.message.reply_text(msgStart)


def helpme(bot, update):
    """ Prints help message. """
    update.message.reply_text(msgHelp)


def idme(bot, update):
    """ Sends user's telegram ID. """
    update.message.reply_text("Your ID is: " + str(update.message.from_user.id))


def get_bot_ip(bot, update):
    """ Sends the bot's IP address, so as to be able to ssh in if necessary.
        OWNER ONLY.
    """
    sender = update.message.from_user
    if sender.id == Bot.OWNER_ID:
        msg_to_send = ""
        try:
            ip_string = check_output(["curl", "ipinfo.io/ip"],
                                     universal_newlines=True,
                                     timeout=5)
            msg_to_send = msgIpAddress + ip_string
        except CalledProcessError:
            msg_to_send = strings.errUnknown
        except TimeoutExpired:
            msg_to_send = strings.errTimeout
        update.message.reply_text(msg_to_send)


start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", helpme)
idme_handler = CommandHandler("idme", idme)
botip_handler = CommandHandler("botip", get_bot_ip)

msgHelp = """Hi! This bot is currently WIP. I'm working on it!
current commands are:
- /start the bot introduces itself.
- /help prints this message.
- /idme returns your telegram ID.
- /save <notename> <message> saves the message.
- /get <notename> gets the message related to that notename.
- /note returns the list of notes for this chat.
- /owe opens a keayboard of people owing money that can be selected to see individual debts.
- /owe `all` prints a list of all people owing money.
- /owe <ower> prints list of debts for that person.
- /owes opens up a list of people currently owing money. Type a name to add new people.
- /owes <ower> <owee> <sum> tells you ower owes X to owee.
- /cmd <cmdname> <bot answer> sets cmdname to a hotword that the bot replies to

Admin only:
- /clear `all` clears the entire database of owed money.
- /clear <ower> `all` clears everything the ower owes.
- /clear <ower> <owee> clears the debt of ower towards owee.

Note: some commands are WIP and so aren't shown here. Feel free to use them,\
but keep in mind they might change in the future."""
msgStart = "This is PolBot! Just a modular bot made in python. Currently allows for custom " \
           "message in response to commands in group chats. Promote to admin to keep it from " \
           "missing messages! Try /cmd and /rmcmd to add commands :) "

msgIpAddress = "The bot's IP address is: "
