#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, ConversationHandler, Filters
import logging
import os
import configparser
from modules import finance, helper, misc, strings, notes


# initialise globals
config = configparser.ConfigParser()
config.read("FinanceBot.ini")

global owner_ID
owner_ID = int(config["OWNER"]["Telegram_ID"])

global currency
currency = config["SETTINGS"]["currency_code"]

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


def unknown(bot, update, user_data):
    if update.message.text == "/iowes" :
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

    updater = Updater(config["KEYS"]["BOT_API_KEY"])
    dispatcher = updater.dispatcher

    # LINK FUNCTIONS

    iowes_ConversationHandler = ConversationHandler(
        entry_points=[CommandHandler("iowes",
                                     finance.inlineOwes,
                                     pass_user_data=True)],

        states = {
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
    dispatcher.add_handler(CommandHandler("help", misc.help))
    dispatcher.add_handler(CommandHandler("clear", finance.clear, pass_args=True))
    dispatcher.add_handler(CommandHandler("owe", finance.owe, pass_args=True))
    dispatcher.add_handler(CommandHandler("owes", finance.owes, pass_args=True))
    dispatcher.add_handler(CommandHandler("idme", misc.idme))
    dispatcher.add_handler(CommandHandler("botip", misc.getBotIp))
    dispatcher.add_handler(CommandHandler("save", notes.saveNote, pass_args=True))
    dispatcher.add_handler(CommandHandler("get", notes.getNote, pass_args=True))
    dispatcher.add_handler(CommandHandler("note", notes.allNotes, pass_args=True))

    dispatcher.add_handler(CommandHandler("iowe", finance.inlineOwe))
    dispatcher.add_handler(iowes_ConversationHandler)


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
