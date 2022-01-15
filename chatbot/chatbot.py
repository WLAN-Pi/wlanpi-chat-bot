#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
A chatbot to receive commands to perform various WLAN Pi operations and 
retrieve status information.

This work is based upon the excellent article and code provided by Gareth
Dwyer in his blog article "Building a Chatbot using Telegram and Python (Part 1)".

You can find the article at: 

https://www.codementor.io/@garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay

Thank you Gareth.

"""
import argparse
import logging
import logging.config
import os
from pprint import pprint
import signal
import sys
import time
from os.path import exists

import chatbot.utils.useful

from .__version__ import __version__
from .transports.telegram_comms import TelegramComms
from .utils.check_telegram_available import CheckTelegram
from .utils.config import Config
from .utils.node_data_snapshot import DataSnapshot
from .utils.parser import Parser
from .utils.status import get_status
from .py_commands.command import register_commands


def setup_logger(args) -> None:
    """Configure and set logging levels"""
    if args.debug:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    default_logging = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"}
        },
        "handlers": {
            "default": {
                "level": logging_level,
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {"": {"handlers": ["default"], "level": logging_level}},
    }
    logging.config.dictConfig(default_logging)


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="wlanpi-chat-bot is a telegram chat bot for the WLAN Pi",
)
parser.add_argument(
    "--bot_token",
    metavar="bot_token",
    dest="bot_token",
    type=str,
    help="Set the telegram bot token",
)
parser.add_argument(
    "--debug",
    dest="debug",
    action="store_true",
    default=False,
    help="enable debug logging output",
)
parser.add_argument("--version", "-V", action="version", version=f"{__version__}")
args = parser.parse_args()

setup_logger(args)

# logging.basicConfig(level=logging.INFO)

script_logger = logging.getLogger("TelegramAlert")
script_logger.debug("********* Starting chat bot *************")

LONG_POLLING_TIMEOUT = 30

# read in local node config info
conf_obj = Config()
conf_obj.read_config()

here = os.path.dirname(os.path.realpath(__file__))

# Telegram info
if not conf_obj.config.get("telegram", None):
    conf_obj.config["telegram"] = {}
    conf_obj.config["telegram"]["bot_token"] = ""
    conf_obj.config["telegram"]["chat_id"] = ""
    conf_obj.config["telegram"]["display_mode"] = "full"
    conf_obj.config["telegram"]["display_width"] = "30"

api_key = conf_obj.config["telegram"]["bot_token"]

# lets see if we can find an api key if its missing
script_logger.debug("Checking for API key...")
if not api_key:

    script_logger.debug("No API key found, trying to find one...")
    # check to see if we can find the key in the /boot folder
    key_file = "/boot/wlanpi_bot.key"

    if exists(key_file):
        script_logger.info(f"Found key file at {key_file}")

        script_logger.debug("Reading key file...")
        try:
            with open(key_file, "r") as f:
                api_key = f.readline().strip()
            script_logger.info("Key file read OK.")
        except Exception as ex:
            script_logger.error(f"Issue reading bot key file {ex}")

        if api_key:
            conf_obj.config["telegram"]["bot_token"] = api_key

        # remove the key file
        script_logger.debug("Removing key file in boot partition...")
        try:
            os.remove(key_file)
            script_logger.info("Key file removed.")
        except Exception as ex:
            script_logger.error(f"Issue removing bot key file {ex}")

        conf_obj.update_config()
else:
    script_logger.debug("API key value exists.")

if args.bot_token:
    script_logger.debug("Using bot token passed in by user")
    conf_obj.config["telegram"]["bot_token"] = args.bot_token
    api_key = args.bot_token

t = TelegramComms(api_key)

# Create Telegram network connection checker
tc = CheckTelegram()

# add path to our yaml commands to the conf_obj
conf_obj.config["telegram"]["yaml_cmds"] = os.path.join(here, "yaml_commands")

# register all commands ready to use later
GLOBAL_CMD_DICT = register_commands(t, conf_obj)

# create parser obj
parser_obj = Parser(GLOBAL_CMD_DICT, script_logger)



# handle Ctrl-C input
def handler(signal_received, frame):
    script_logger.info("Chat-bot: Ctrl-C hit.")
    sys.exit(0)


def main():

    # only true first time around
    booted = True

    signal.signal(signal.SIGINT, handler)

    last_update_id = None
    online = False  # start assuming offline

    chat_id = False
    username = False
    
    if "chat_id" in conf_obj.config["telegram"].keys():
        chat_id = conf_obj.config["telegram"]["chat_id"]

    if "username" in conf_obj.config["telegram"].keys():
        username = conf_obj.config["telegram"]["username"]

    # event loop
    script_logger.debug("Starting main event loop.")
    while True:

        # handle missing API key to save just failing the service if its missing
        if conf_obj.config["telegram"]["bot_token"] == "":

            # no API token - sleep and try again later
            script_logger.info(
                "Chatbot is missing API key configuration... unable to go online..."
            )
            time.sleep(3600)
            continue

        script_logger.debug("Poll cycle start.")

        # check we're online to Telegram
        script_logger.debug(
            "Checking we can access Telegram network port (not an auth check)."
        )

        if tc.check_telegram_available():
            script_logger.debug("We're online.")

            # if we have been offline (or this is startup) send boot status
            if online == False:
                script_logger.info("We were offline, but we're back online.")

                # send probe startup status message (as we must now be back online)
                startup_msg = get_status()

                if startup_msg:
                    script_logger.debug("Sending startup message.")
                    t.send_msg(startup_msg, chat_id, encode=False)

                online = True  # signal that we are back online

            # report on probe status if this is a reboot or something changed
            snapshot = DataSnapshot()
            status_update = snapshot.node_status()

            # send a probe status update if required (i.e. something changed)
            if status_update and chat_id:
                script_logger.debug(
                    "Looks like something changed, sending status update."
                )
                t.send_msg(status_update, chat_id)

            # get updates from the Telegram bot
            # (Note we're using long polling, which is an extended http timeout to avoid
            # use of rapid upstream polling of Telegram bot to check for new messages)
            #
            # Pass the ID of last rec'd message to ack message and stop it being sent again
            # try:
            
            flush_telegram_msgs = False
            if booted:
                t.long_polling_timeout = 1
                booted = False
                # flush out cached cmds
                flush_telegram_msgs = True
            else:
                t.long_polling_timeout = LONG_POLLING_TIMEOUT
            
            script_logger.debug("Checking for messages (long poll start).")
            updates = t.get_updates(last_update_id)

            # ignore any cached cmds if received and flush is signalled
            if flush_telegram_msgs and len(updates["result"]) > 0:
                last_update_id = t.get_last_update_id(updates) + 1
                continue

            if not updates:
                # no update received, must have timed out
                script_logger.debug(
                    "Long poll timed out (maybe network changed?), restarting poll cycle."
                )
                continue

            # if we have a message to process, lets take action
            if updates:
                if updates.get("ok") == False:
                    script_logger.error(
                        f"Problem in getUpdates: error ({updates.get('error_code')}) with description ({updates.get('description')})"
                    )
                    script_logger.error(
                        "We have reachability, but are having a problem. Is the bot token correct? Sleeping before we try again."
                    )
                    time.sleep(30)
                if updates.get("ok") == True and "result" in updates:

                    if len(updates["result"]) > 0:
                        script_logger.debug("Processing message.")
                        last_update_id = t.get_last_update_id(updates) + 1

                        # slice out the last msg (in the case of multipe msgs being sent)
                        update = updates["result"][-1]

                        script_logger.debug(f"Dump of received update: {update}")

                        # extract the message text
                        if "message" in update.keys():
                            text = str(update["message"]["text"]).strip()
                        else:
                            continue

                        # extract the chat ID for our response
                        chat_id_check = update["message"]["chat"]["id"]

                        # extract username if present
                        if "username" in update["message"]["chat"].keys():
                            username_check = update["message"]["chat"]["username"]

                        # if we don't have a global chat_id already (i.e. new chat-bot instance), write it to the config file
                        if not chat_id:
                            script_logger.debug("We don't have a chat ID yet, using details in this message to configure chat ID & username for bot.")
                            script_logger.debug("Writing chat ID to config file.")
                            conf_obj.config["telegram"]["chat_id"] = chat_id_check
                            chat_id = chat_id_check
                            conf_obj.update_config()
                        
                            # if we don't have a global username already and we found a username, write it to the config file
                            if not username:
                                script_logger.debug("Writing username to config file.")
                                conf_obj.config["telegram"]["username"] = username_check
                                username = username_check
                                conf_obj.update_config()
                            
                            # we don't want to process any commands yet, go 
                            # back to top of event loop 
                            continue
                        else:
                            # perform security checks that the command is sent by the authorised user
                            script_logger.debug("Checking received update is from authorized user.")

                            if (chat_id == chat_id_check) and (username == username_check):
                                script_logger.debug("Chat ID and username check OK.")
                            else:
                                script_logger.debug("Chat ID or username is incorrect, failed check (update not processed).")
                                continue

                        # cleanup whitespace (inc trailing & leading space)
                        text = " ".join(text.split())

                        # get list of available commands
                        script_logger.debug("Getting command list.")
                        command_list = list(GLOBAL_CMD_DICT.keys())
                        command_list.sort()

                        # if the text starts with 'help', slice off
                        # help keyword and pass remaining to parser
                        help = ""
                        if text.startswith("help") and (" " in text):
                            [help, text] = text.split(" ", 1)

                        # parse command and expand any shortening of verbs (run, show, set, exec)
                        script_logger.debug("Parse command.")
                        [command, args_list] = parser_obj.parse_cmd(text)

                        msg = "blank"
                        encode = True

                        script_logger.debug("Process command.")
                        if help.startswith("help"):
                            # provide help method from command class
                            if command:
                                msg = GLOBAL_CMD_DICT[command].help()
                            else:
                                msg = "Unknown command.  Try '?' "

                        elif text == "?":
                            # provide list of all commands
                            msg = ["Available commands:\n"]
                            fixed_command_list = [
                                e.replace("_", " ") for e in command_list
                            ]
                            msg = (
                                msg
                                + fixed_command_list
                                + ['(Type "info" for startup status msg)']
                            )

                        elif text == "help":
                            msg = chatbot.utils.useful.help()

                        # open those easter eggs kids!
                        elif text in chatbot.utils.useful.cmds.keys():
                            msg = chatbot.utils.useful.cmds[text]()

                        elif text in ["in", "inf", "info"]:
                            # show boot msg
                            msg = get_status()

                        elif command in command_list:
                            script_logger.debug(
                                f"Command sent: {command}, (args: {args_list})"
                            )
                            msg = GLOBAL_CMD_DICT[command].run(args_list)

                        else:
                            msg = 'Unknown command (try "help" or "?" command)'

                        script_logger.debug("Send msg to Telegram ({})".format(msg))
                        t.send_msg(msg, chat_id, encode=encode)

        else:
            # we likely had a connectivity issue of some type....lets sleep
            script_logger.info("We appear to be offline. Sleeping before next loop.")
            script_logger.error(
                "We have a network connectivity issue. Sleeping before we try again."
            )
            online = False
            time.sleep(30)

        script_logger.debug("Poll cycle complete.")


if __name__ == "__main__":
    main()
