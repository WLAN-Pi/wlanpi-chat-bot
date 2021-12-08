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

  {verb} [noun] [arg1 .. argN]

Some commands require no noun
(e.g. ping).

Arguments vary with the 
requirements of each command. 

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

Visit http://wlanpi.com for
more details.
"""