#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
""" This is the main file for the FinanceBot telegram bot.

Here, the main function is the main element, which adds a series of handlers to
describe how respond to the input given to the telegram bot by a user.

The bot is then set to wait until input is received.

For ease of use, the bot is split into multiple modules, found in the modules
directory; this allows modules to be added or removed in a simpler fashion.

"""

import os
import configparser
import logging
from telegram.ext import Updater, MessageHandler, Filters
from modules import finance, misc, strings, notes, customcmds


# if __name__ == '__main___':
#     from modules import finance, misc, strings, notes
# else:
#     from .modules import finance, misc, strings, notes


# initialise globals
# load config file
CONFIG = configparser.ConfigParser()
CONFIG.read("Bot.ini")

OWNER_ID = int(CONFIG["OWNER"]["Telegram_ID"])

CURRENCY = CONFIG["SETTINGS"]["currency_code"]

KEY = CONFIG["KEYS"]["BOT_API_KEY"]


# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

def unknown(bot, update):
    """Used to respond to unknown command inputs, and deal with edge cases."""

    if update.message.text == "/cancel":
        update.message.reply_text(strings.errNothingToCancel)

    else:
        update.message.reply_text(strings.errUnknownCommand)

def main():
    """ The main section of the file. Checks the data dir, loads the
    BOT_API_KEY, adds the appropriate handlers, and then awaits input from
    telegram.
    """
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    if not os.path.exists("./data/"):
        os.makedirs("data")

    updater = Updater(KEY)
    dispatcher = updater.dispatcher

    # LINK FUNCTIONS

    # misc module
    dispatcher.add_handler(misc.start_handler)
    # dispatcher.add_handler(misc.help_handler)
    dispatcher.add_handler(misc.idme_handler)
    dispatcher.add_handler(misc.botip_handler)

    # notes module
    # dispatcher.add_handler(notes.save_handler)
    # dispatcher.add_handler(notes.get_handler)
    # dispatcher.add_handler(notes.note_handler)

    # finance module
    # dispatcher.add_handler(finance.clear_handler)
    # dispatcher.add_handler(finance.owe_handler)
    # dispatcher.add_handler(finance.owes_handler)
    # dispatcher.add_handler(finance.owes_buttons_handler) # not a cmd.

    # customcmds module (calls unknown command handler if unable to handle)
    dispatcher.add_handler(customcmds.set_user_command_handler)
    dispatcher.add_handler(customcmds.user_command_handler)

    # unknown commands, leave last.
    dispatcher.add_handler(MessageHandler(Filters.command,
                                          unknown))

    updater.start_polling()
    updater.idle()

# run main if run as script
if __name__ == '__main__':
    main()
