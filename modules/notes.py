#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

from modules import helper, strings
from telegram.ext import Updater


def saveNote(bot, update, args):
    notes = helper.loadjson(strings.loc_notesjson)
    chat_id = str(update.message.chat_id)

    try: notes[chat_id]
    except KeyError: notes[chat_id] = {}

    if len(args) >= 2:
        # add note to note repo
        notename = args[0]
        del args[0]
        noteData = " ".join(args)
        notes[chat_id][notename]= noteData
        print("Added new note \"" + notename + "\" with content \"" \
                + noteData + "\"." )
    else:
        update.message.reply_text(strings.errBadFormat)

    helper.dumpjson(strings.loc_notesjson, notes)


def getNote(bot, update, args):
    notes = helper.loadjson(strings.loc_notesjson)
    chat_id = str(update.message.chat_id)

    try: notes[chat_id]
    except KeyError: notes[chat_id] = {}

    if len(args) == 1:
        msg = ""
        try:
            msg = notes[chat_id][args[0]]

        except KeyError:
            msg = strings.errNoNoteFound + args[0]

        update.message.reply_text(msg)
    else:
        update.message.reply_text(strings.errBadFormat)


def allNotes(bot, update, args):
    notes = helper.loadjson(strings.loc_notesjson)
    chat_id = str(update.message.chat_id)

    try: notes[chat_id]
    except KeyError: notes[chat_id] = {}
    msg = "No notes in this chat."
    if len(notes[chat_id]) > 0:
        msg = strings.msgNotesForChat
        for note in notes[chat_id]:
            msg += "\n" + note

    update.message.reply_text(msg)
