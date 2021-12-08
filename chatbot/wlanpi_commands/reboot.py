import os

import chatbot.utils.emojis

from .command import Command


class Reboot(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "reboot"

    def run(self, args_list):

        os.system("(sync; sleep 2; systemctl reboot) &")
        restart_emoji = chatbot.utils.emojis.restart()
        return self._render(f"{restart_emoji} Rebooting....please wait {restart_emoji}")

    def help(self):
        """
        Return the help page for this command
        """
        short_msg = "reboot: Reboot the probe"
        long_msg = """reboot: 

Reboot the probe

syntax: reboot"""

        if self.display_mode == "compact":
            return short_msg
        else:
            return chatbot.utils.emojis.help() + " " + long_msg
