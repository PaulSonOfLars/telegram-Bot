#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import os
import configparser
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler
from modules import finance, misc, strings, notes


# initialise globals
CONFIG = configparser.ConfigParser()
CONFIG.read("FinanceBot.ini")

global OWNER_ID
OWNER_ID = int(CONFIG["OWNER"]["Telegram_ID"])

global CURRENCY
CURRENCY = CONFIG["SETTINGS"]["CURRENCY_code"]

global KEY
KEY = CONFIG["KEYS"]["BOT_API_KEY"]

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

OWER, OWEE, AMOUNT = range(3)


def error(bot, update, error):
    LOGGER.warn('Update "%s" caused error "%s"' % (update, error))
    update.message.reply_text(strings.errUnknown)


def __repr__(self):
    return str(self)


def unknown(bot, update, user_data):
    if update.message.text == "/iowes":
        user_data.pop("ower")
        user_data.pop("owee")
        update.message.reply_text(strings.errCommandStillRunning)
        return ConversationHandler.END
    else:
        update.message.reply_text(strings.errUnknownCommand)


def main():
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
                                    finance.amount,
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

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

# run main if run as script
if __name__ == '__main__':
    main()
