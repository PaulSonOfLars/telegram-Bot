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
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler
from modules import finance, misc, strings, notes

# initialise globals
# load config file
CONFIG = configparser.ConfigParser()
CONFIG.read("FinanceBot.ini")

OWNER_ID = int(CONFIG["OWNER"]["Telegram_ID"])

CURRENCY = CONFIG["SETTINGS"]["currency_code"]

KEY = CONFIG["KEYS"]["BOT_API_KEY"]

# give numbers for the ConversationHandler buttons used in /iowes
OWER, OWEE, AMOUNT = range(3)

def unknown(bot, update, user_data):
    """Used to respond to unknown command inputs, and deal with edge cases."""

    if update.message.text == "/iowes":
        try:
            user_data.pop("ower")
            user_data.pop("owee")
        except KeyError:
            pass
        update.message.reply_text(strings.errCommandStillRunning)
        return ConversationHandler.END

    elif update.message.text == "/cancel":
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

    iowes_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("iowes",
                                     finance.inline_owes)],

        states={
            OWER: [MessageHandler(Filters.text,
                                  finance.create_ower,
                                  pass_user_data=True),
                   CallbackQueryHandler(finance.ower_button,
                                        pass_user_data=True)],

            OWEE: [MessageHandler(Filters.text,
                                  finance.create_owee,
                                  pass_user_data=True),
                   CallbackQueryHandler(finance.owee_button,
                                        pass_user_data=True)],

            AMOUNT: [MessageHandler(Filters.text,
                                    finance.amount_owed,
                                    pass_user_data=True)]
        },
        fallbacks=[CommandHandler("cancel",
                                  finance.cancel,
                                  pass_user_data=True),
                   MessageHandler(Filters.command,
                                  unknown,
                                  pass_user_data=True)]
    )

    dispatcher.add_handler(CommandHandler("start", misc.start))
    dispatcher.add_handler(CommandHandler("help", misc.helpme))
    dispatcher.add_handler(CommandHandler("clear", finance.clear, pass_args=True))
    dispatcher.add_handler(CommandHandler("owe", finance.owe, pass_args=True))
    dispatcher.add_handler(CommandHandler("owes", finance.owes, pass_args=True))
    dispatcher.add_handler(CommandHandler("idme", misc.idme))
    dispatcher.add_handler(CommandHandler("botip", misc.get_bot_ip))
    dispatcher.add_handler(CommandHandler("save", notes.save_note, pass_args=True))
    dispatcher.add_handler(CommandHandler("get", notes.get_note, pass_args=True))
    dispatcher.add_handler(CommandHandler("note", notes.all_notes, pass_args=True))

    dispatcher.add_handler(CommandHandler("iowe", finance.inline_owe))
    dispatcher.add_handler(iowes_conversation_handler)


    dispatcher.add_handler(CallbackQueryHandler(finance.owebutton, pass_user_data=True))

    #unknown commands, leave last.
    dispatcher.add_handler(MessageHandler(Filters.command,
                                          unknown,
                                          pass_user_data=True))

    updater.start_polling()
    updater.idle()

# run main if run as script
if __name__ == '__main__':
    main()
