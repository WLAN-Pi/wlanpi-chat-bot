from chatbot.utils.emojis import cats, cool


def hello():
    return "Hi, glad to see you looking so good today!"


def hi():
    return "Hi you!!! {}".format(cool())


cmds = {"cats": cats, "hello": hello, "hi": hi}


def help():
    return """
============================
===== WLAN PI CHAT BOT =====
============================ 

For a complete of available
commands please enter: ?

Commands have a general format
of:

  {verb} [noun]

Some commands require no noun
(e.g. speedtest).

Commands may be entered in 
full text format e.g.

   show cdp

Or, they may be entered in 
their shortest unique form
e.g.

   sh cd

To receive help on a specific
command, please enter 'help'
before the required command
e.g.

   help show uptime
   help sh up

View the full chat-bot user 
guide here:
https://github.com/WLAN-Pi/wlanpi-chat-bot/blob/main/docs/USERGUIDE.md
"""
