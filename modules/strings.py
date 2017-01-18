#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

# this file declares all strings

# messages
msgHelp = """Hi! This bot is currently WIP. I'm working on it!
current commands are:
- /start the bot introduces itself.
- /help prints this message.
- /owes <ower> <owee> <sum> tells you ower owes X to owee.
- /owe prints a list of all people owing money.
- /owe <ower> prints a list of all people being owed money to.
- /clear `all` clears the entire database of owed money.
- /clear <ower> `all` clears everything the ower owes.
- /clear <ower> <owee> clears the debt of ower towards owee.
- /idme returns your telegram ID.

Note: some commands are WIP and so aren't shown here. Feel free to use them,\
but keep in mind they might change in the future."""
msgStart = "This is FinanceBot! He can help you take care of your house finances. Use /help for more info."

msgNoMoneyOwed = "Lucky... that person doesn't owe anything!"
msgListMoneyOwed = "Here is a list of people owing money:\n"
msgListMoneyOwedIndiv = "Here is a list of everyone {} owes money to: \n"

msgHowMuch = "How much does {} owe {}? Please type a number."
msgNewOwer = "{} was saved as a new ower. Please input the name of the person that {} owes money to."
msgNewOwee = "{} was saved as a new owee for {}." + msgHowMuch
msgCurrentOwers = "Here is the current list of people who owe money. Please select one, or reply with a new name to add a new ower."
msgWhoOwedTo = "Who does {} owe money to? Type in a new name to add a new owee."

msgNoDebts = "Wow... there are no debts here!"
msgAllDebtsCleared = "All debts cleared!"
msgAllDebtsClearedTerm = msgAllDebtsCleared + " A backup file can be found in bckp.json."
msgDebtsOfCleared = "{} had all debts cleared by the owner."
msgDebtsOfToCleared = "{}'s debts to {} were cleared."

msgIpAddress = "The bot's IP address is: "

msgNotesForChat = "These are the notes i have saved for this chat: \n"


# file locations
loc_owedjson = "./data/owed.json"
loc_bckpjson = "./data/bckp.json"
loc_notesjson = "./data/notes.json"


# error strings
errNoFile = "Either file is missing or is not readable. Creating."
errBadFormat = "Command badly formatted. Use /help for help."
errNotInt = "You gave me an invalid sum! Please only use numbers/decimals (ie, dont specify the currency, this is specified by the owner.)"
errNotAdmin = "You are not admin! You can't run this command."
errNoOwer = "There is no-one here with this name: "
errAllName = "\"all\" cannot be used as a name!"
errUnknown = "An error has occured."
errTimeout = "A timeout error has occured."
errNoNoteFound = "No note found by the name of "
errUnknownCommand = "Hey, I haven't been taught how that command works yet!"
errCommandStillRunning = "Sorry, I realised I was still running that. Please try again, it should work!"
errUnauthCommand = "User {} tried to issue an owner command."
errButtonMsg = "Error. Message not set after button call."
errUnknownCallback = "Err: unrecognised callback code."
errNothingToCancel = "Nothing to cancel!"
