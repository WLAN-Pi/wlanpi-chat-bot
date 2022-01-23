from .command import Command


class ShowMode(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_mode"

    def help(self):
        """
        Return the help page for this command
        """
        short_msg = "Show current WLAN Pi mode"
        long_msg = (
            """Shows the current WLAN Pi mode (e.g. hotspot mode, classic mode) 
Syntax: show mode"""
        )

        if self.display_mode == "compact":
            return short_msg
        
        return long_msg

    def run(self, args_list):
        STATUS_FILE = "/etc/wlanpi-state"
        status = "WLAN Pi mode: {}".format(self._read_file(STATUS_FILE)[0])
        return self._render(status.strip())
