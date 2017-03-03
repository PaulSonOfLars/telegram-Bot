#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

""" This is the note module, taking care of all note related functions.

Note data is found in data/notes.json.
"""

from telegram.ext import CommandHandler
from modules import helper, strings

def save_note(bot, update, args):
    notes = helper.loadjson(loc_notesjson)
    chat_id = str(update.message.chat_id)

    try:
        notes[chat_id]
    except KeyError:
        notes[chat_id] = {}

    if len(args) >= 2:
        # add note to note repo
        notename = args[0]
        del args[0]
        note_data = " ".join(args)
        notes[chat_id][notename] = note_data
        print("Added new note \"" + notename + "\" with content \"" \
                + note_data + "\".")
    else:
        update.message.reply_text(strings.errBadFormat)

    helper.dumpjson(loc_notesjson, notes)


def get_note(bot, update, args):
    notes = helper.loadjson(loc_notesjson)
    chat_id = str(update.message.chat_id)

    try:
        notes[chat_id]
    except KeyError:
        notes[chat_id] = {}

    if len(args) == 1:
        msg = ""
        try:
            msg = notes[chat_id][args[0]]
        except KeyError:
            msg = errNoNoteFound + args[0]

        update.message.reply_text(msg)
    else:
        update.message.reply_text(strings.errBadFormat)


def all_notes(bot, update, args):
    notes = helper.loadjson(loc_notesjson)
    chat_id = str(update.message.chat_id)

    try:
        notes[chat_id]
    except KeyError:
        notes[chat_id] = {}

    msg = "No notes in this chat."
    if len(notes[chat_id]) > 0:
        msg = msgNotesForChat
        for note in notes[chat_id]:
            msg += "\n" + note

    update.message.reply_text(msg)


save_handler = CommandHandler("save", save_note, pass_args=True)
get_handler = CommandHandler("get", get_note, pass_args=True)
note_handler = CommandHandler("note", all_notes, pass_args=True)

loc_notesjson = "./data/notes.json"

msgNotesForChat = "These are the notes i have saved for this chat: \n"

errNoNoteFound = "No note found by the name of "
