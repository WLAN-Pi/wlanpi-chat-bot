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
import logging
import os
import sys
import time
from os.path import exists

import chatbot.utils.useful

from .transports.telegram_comms import TelegramComms
from .utils.check_telegram_available import CheckTelegram
from .utils.config import Config
from .utils.node_data_snapshot import DataSnapshot
from .utils.parser import parse_cmd
from .utils.status import get_status
from .wlanpi_commands.command import Command, register_commands

logging.basicConfig(level=logging.INFO)
script_logger = logging.getLogger("TelegramAlert")
# script_logger.setLevel(logging.DEBUG)

script_logger.debug("********* Starting chat bot *************")

long_polling_timeout = 100

# read in local node config info
conf_obj = Config()
conf_obj.read_config()

# Telegram info
if not conf_obj.config.get("telegram", None):
    conf_obj.config["telegram"] = {}
    conf_obj.config["telegram"]["bot_token"] = ""
    conf_obj.config["telegram"]["chat_id"] = ""
    conf_obj.config["telegram"]["display_mode"] = "full"
    conf_obj.config["telegram"]["display_width"] = "30"
    conf_obj.config["telegram"]["yaml_cmds"] = "/etc/wlanpi-chat-bot/commands"

api_key = conf_obj.config["telegram"]["bot_token"]
chat_id = False  # we may not know our chat_id initially...

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

t = TelegramComms(api_key)

# Create Telegram network connection checker
tc = CheckTelegram()

# register all commands ready to use later
GLOBAL_CMD_DICT = register_commands(t, conf_obj)

if "chat_id" in conf_obj.config["telegram"].keys():
    chat_id = conf_obj.config["telegram"]["chat_id"]


def main():
    last_update_id = None
    online = False  # start assuming offline

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
            try:
                script_logger.debug("Checking for messages (long poll start).")
                updates = t.get_updates(last_update_id)
            except:
                script_logger.debug(
                    "Long poll timed out (maybe network changed?), restarting poll cycle."
                )
                continue

            # if we have a message to process, lets take action
            if updates and (len(updates["result"]) > 0):

                script_logger.debug("Processing message.")
                last_update_id = t.get_last_update_id(updates) + 1

                # slice out the last msg (in the case of multipe msgs being sent)
                update = updates["result"][-1]

                # extract the message text
                if "message" in update.keys():
                    text = str(update["message"]["text"]).strip()
                else:
                    continue

                # extract the chat ID for our response
                chat = update["message"]["chat"]["id"]

                # if we don't have a global chat_id already, write it to the config file
                if not chat_id:
                    script_logger.debug("Writing chat ID to config file.")
                    conf_obj.config["telegram"]["chat_id"] = chat
                    conf_obj.update_config()

                # normalize text case  - note removed as breakin case-sensitive args
                # text = text.lower()
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
                [command, args_list] = parse_cmd(text, command_list)

                msg = "blank"
                encode = True

                script_logger.debug("Process command.")
                if help.startswith("help"):
                    # provide help method from command class
                    if command:
                        msg = GLOBAL_CMD_DICT[command].help()
                    else:
                        msg = "Unknown command.  Try '?' "

                elif text == "?" or text == "help":
                    # provide list of all commands
                    msg = ["Available commands:\n"]
                    fixed_command_list = [e.replace("_", " ") for e in command_list]
                    msg = (
                        msg
                        + fixed_command_list
                        + ['(Type "info" for startup status msg)']
                    )

                # open those easter eggs kids!
                elif text in utils.useful.cmds.keys():
                    msg = utils.useful.cmds[text]()

                elif text in ["in", "inf", "info"]:
                    # show boot msg
                    msg = get_status()
                    encode = False

                elif command in command_list:
                    script_logger.debug(f"Command sent: {command}, (args: {args_list})")
                    msg = GLOBAL_CMD_DICT[command].run(args_list)

                else:
                    msg = 'Unknown command (try "help" or "?" command)'

                script_logger.debug("Send msg to Telegram ({})".format(msg))
                t.send_msg(msg, chat, encode=encode)
        else:
            # we likely had a connectivity issue of some type....lets sleep
            script_logger.info("We appear to be offline, sleeping before next loop.")
            script_logger.error(
                "We have a network connectivity issue. Sleeping before we try again."
            )
            online = False
            time.sleep(30)

        script_logger.debug("Poll cycle complete.")


if __name__ == "__main__":
    main()
