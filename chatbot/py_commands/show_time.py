from .command import Command


class ShowTime(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_time"
    
    def help(self):
        """
        Return the help page for this command
        """
        short_msg = "Show local time on the WLAN Pi"
        long_msg = (
            """Shows the current local time on the WLAN Pi
Syntax: show time"""
        )

        if self.display_mode == "compact":
            return short_msg
        
        return long_msg

    def run(self, args_list):
        import time

        return self._render(time.ctime())
