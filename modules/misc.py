#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
""" This is the miscellaneous commands module.

It is full of small, helpful functions that don't quite need a full module
and that a user might use for information.
"""
from subprocess import check_output, CalledProcessError, TimeoutExpired
from modules import strings
import FinanceBot

def start(bot, update):
    """ First command a bot receives."""
    update.message.reply_text(strings.msgStart)


def helpme(bot, update):
    """ Prints help message. """
    update.message.reply_text(strings.msgHelp)


def idme(bot, update):
    """ Sends user's telegram ID. """
    update.message.reply_text("Your ID is: " \
                              + str(update.message.from_user.id))


def get_bot_ip(bot, update):
    """ Sends the bot's IP address, so as to be able to ssh in if necessary.
        OWNER ONLY.
    """
    sender = update.message.from_user
    if sender.id == FinanceBot.OWNER_ID:
        msg_to_send = ""
        try:
            ip_string = check_output(["curl", "ipinfo.io/ip"],
                                     universal_newlines=True,
                                     timeout=5)
            msg_to_send = strings.msgIpAddress + ip_string
        except CalledProcessError:
            msg_to_send = strings.errUnknown
        except TimeoutExpired:
            msg_to_send = strings.errTimeout
        update.message.reply_text(msg_to_send)
