#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import subprocess
from modules import strings
import FinanceBot

def start(bot, update):
    update.message.reply_text(strings.msgStart)


def helpme(bot, update):
    update.message.reply_text(strings.msgHelp)


def idme(bot, update):
    update.message.reply_text("Your ID is: " \
                              + str(update.message.from_user.id))


def get_bot_ip(bot, update):
    sender = update.message.from_user
    if sender.id == FinanceBot.OWNER_ID:
        msg_to_send = ""
        try:
            ip_string = subprocess.check_output(["curl", "ipinfo.io/ip"],
                                                universal_newlines=True,
                                                timeout=5)
            msg_to_send = strings.msgIpAddress + ip_string
        except CalledProcessError:
            msg_to_send = strings.errUnknown
        except TimeoutExpired:
            msg_to_send = strings.errTimeout
        update.message.reply_text(msg_to_send)
