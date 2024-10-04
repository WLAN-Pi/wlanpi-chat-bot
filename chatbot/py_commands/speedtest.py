import subprocess

import chatbot.utils.emojis

from .command import Command


class Speedtest(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "speedtest"

    def run(self, args_list):

        # send status msg
        chat_id = self.telegram_object.chat_id
        self.telegram_object.send_msg(
            "{} Running speedtest...please wait {}".format(
                chatbot.utils.emojis.graph(), chatbot.utils.emojis.hour_glass()
            ),
            chat_id,
        )

        # perform speedtest
        speedtest_info = []
        speedtest_cmd = "speedtest --accept-license | egrep -w \"Testing from|Download|Upload\" | sed -r 's/Testing from.*?\(/My IP: /g; s/\)\.\.\.//g; s/Download/D/g; s/Upload/U/g; s/bit\/s/bps/g'"

        try:
            speedtest_output = (
                subprocess.check_output(speedtest_cmd, shell=True).decode().strip()
            )
            speedtest_info = speedtest_output.split("\n")
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error = ["Err: Speedtest error", output]
            print(error)
            return False

        if len(speedtest_info) == 0:
            speedtest_info.append("No output sorry")

        return self._render(speedtest_info)

    def help(self):
        """
        Return the help page for this command
        """
        short_msg = "Runs an Ookla speedtest from the WLAN Pi"
        long_msg = """This command runs a speedtest to the Ookla speedtest service from the WLAN Pi.

It provides the upload and download speed from the WLAN Pi to the Internet. (This test requires your WLAN Pi to have Internet access)

Syntax: speedtest"""

        if self.display_mode == "compact":
            return short_msg
        else:
            return chatbot.utils.emojis.help() + " " + long_msg
