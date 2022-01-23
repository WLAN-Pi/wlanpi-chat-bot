import os

from chatbot.utils.node_data_snapshot import DataSnapshot

from .command import Command


class ShowStatus(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_status"
    
    def help(self):
        """
        Return the help page for this command
        """
        short_msg = "Show a summary of the  WLAN Pi operational status"
        long_msg = (
            """Shows a summary of the  WLAN Pi operational status including hostname, uptime and interface IP addreses
Syntax: show status"""
        )

        if self.display_mode == "compact":
            return short_msg
        
        return long_msg

    def run(self, args_list):

        # remove snapshot file & re-init snapshot
        snapshot = DataSnapshot()
        os.remove(snapshot.local_file)
        status_update = snapshot.node_status()

        return self._render(status_update)
