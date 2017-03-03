#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

from telegram.ext import (ConversationHandler, MessageHandler, CommandHandler,
                          Filters, CallbackQueryHandler)
from telegram import InlineKeyboardMarkup, ReplyKeyboardRemove
from modules import helper
import Bot

""" This is the custom commands module, taking care of adding user defined
commands, often as a joke

Command data is found in data/user_cmds.json.
"""

def add_command(bot, update, args):
    cmds = helper.loadjson(loc_cmdsjson)
    chat_id = str(update.message.chat_id)

    try:
        cmds[chat_id]
    except KeyError:
        return

    if len(args) == 1:
        update.message.reply_text(no_cmd_text_given)
    elif len(args) >= 2:
        # add command to command repo
        cmd_name = "/" + args[0]
        del args[0]
        cmd_data = " ".join(args)
        cmds[chat_id][cmd_name] = cmd_data
        print("Added new cmd \"" + cmd_name + "\" with content \"" \
                + cmd_data + "\".")
    else:
        update.message.reply_text(errBadFormat)

    helper.dumpjson(loc_cmdsjson, cmds)

def rm_command(bot, update, args):
        cmds = helper.loadjson(loc_cmdsjson)
        chat_id = str(update.message.chat_id)

        if len(args) == 1:
            # remove command from command repo
            cmd_name = "/" + args[0]
            try:
                del cmds[chat_id][cmd_name]
                print("removed command \"" + cmd_name + "\".")
            except KeyError:
                return

def handle_user_command(bot, update):
    cmds = helper.loadjson(loc_cmdsjson)
    chat_id = str(update.message.chat_id)
    command_text = update.message.text
    command_list = command_text.split()

    if len(command_list) >= 1:
        try:
            cmd_name = command_list[0]
            del command_list[0]
            no_first_elem = " ".join(command_list)
            msg = cmds[chat_id][cmd_name] + " " + no_first_elem
            update.message.reply_text(msg)
        except KeyError:
            # default to unknown commands handler
            Bot.unknown(bot, update)

    else:
        update.message.reply_text(errBadFormat)


set_user_command_handler = CommandHandler("cmd", add_command, pass_args=True)
rm_user_command_handler = CommandHandler("rmcmd", rm_command, pass_args=True)
user_command_handler = MessageHandler(Filters.command, handle_user_command)


loc_cmdsjson="./data/user_cmds.json"
no_cmd_text_given="No command text given!"
errBadFormat="Invalid format"
