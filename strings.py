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
- /idme returns your telegram ID."""
msgStart = "This is FinanceBot! He can help you take care of your house finances. Use /help for more info."
msgNoMoneyOwed = "Lucky... that person doesn't owe anything!"
msgListMoneyOwed = "Here is a list of people owing money:\n"
msgNoDebts = "Wow... there are no debts here!"
msgAllDebtsCleared = "All debts cleared!"
msgAllDebtsClearedTerm = msgAllDebtsCleared + " A backup file can be found in bckp.json."

# error strings
errNoFile = "Either file is missing or is not readable. Creating."
errBadFormat = "Command badly formatted. Use /help for help."
errNotInt = "You gave me an invalid sum! Please only use numbers/decimals (ie, dont specify the currency, this is specified by the owner.)"
errNotAdmin = "You are not admin! You can't run this command."
errNoOwer = "There is no-one here with this name: "
errAllName = "\"all\" cannot be used as a name!"
