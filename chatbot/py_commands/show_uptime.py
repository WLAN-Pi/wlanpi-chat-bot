from chatbot.utils.uptime import Uptime

from .command import Command


class ShowUptime(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_uptime"
    
    def help(self):
        """
        Return the help page for this command
        """
        short_msg = "Show how long WLAN Pi has been up"
        long_msg = (
            """Shows how long WLAN Pi has been up (i.e. time since last boot/reboot)
Syntax: show uptime"""
        )

        if self.display_mode == "compact":
            return short_msg
        
        return long_msg

    def run(self, args_list):
        import time

        uptime_obj = Uptime()
        return self._render(uptime_obj.get_uptime())
