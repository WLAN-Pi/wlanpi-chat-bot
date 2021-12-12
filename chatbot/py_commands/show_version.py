import os

import chatbot.utils.emojis
from chatbot.__version__ import __version__

from .command import Command


class ShowVersion(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_ver"

    def run(self, args_list):

        WLANPI_IMAGE_FILE = "/etc/wlanpi-release"

        version_string = ""

        if os.path.isfile(WLANPI_IMAGE_FILE):
            with open(WLANPI_IMAGE_FILE, "r") as f:
                lines = f.readlines()

            # pull out the version number
            for line in lines:
                (name, value) = line.split("=")
                if name == "VERSION":
                    version = value.strip()
                    version_string = "WLAN Pi: " + version[1:-1]
                    break
        else:
            version_string = "WLAN Pi: unknown"

        version_string += "\nBot: " + __version__

        return self._render(version_string)

    def help(self):
        """
        Return the help page for this command
        """
        short_msg = "show ver: Show the probe software version"
        long_msg = """show ver: 

Show the probe software version

syntax: show ver"""

        if self.display_mode == "compact":
            return short_msg
        else:
            return chatbot.utils.emojis.help() + " " + long_msg
