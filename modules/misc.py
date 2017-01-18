#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

from telegram.ext import Updater
import subprocess
from modules import helper, strings
import FinanceBot

def start(bot, update):
    update.message.reply_text(strings.msgStart)


def help(bot, update):
    update.message.reply_text(strings.msgHelp)


def idme(bot, update):
    update.message.reply_text("Your ID is: " \
                               + str(update.message.from_user.id))


def getBotIp(bot, update):
    sender = update.message.from_user
    if sender.id == FinanceBot.owner_ID:
        msgToSend = ""
        try:
            ip_string = subprocess.check_output(["curl", "ipinfo.io/ip"],
                                                 universal_newlines=True,
                                                 timeout=5)
            msgToSend = strings.msgIpAddress + ip_string
        except CalledProcessError: msgToSend = strings.errUnknown
        except TimeoutExpired: msgToSend = strings.errTimeout
        update.message.reply_text(msgToSend)
