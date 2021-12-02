from .command import Command
from utils.node_data_snapshot import DataSnapshot
import os

class ShowStatus(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_status"
    
    def run(self, args_list):

        # remove snapshot file & re-init snapshot
        snapshot = DataSnapshot()
        os.remove(snapshot.local_file)
        status_update = snapshot.node_status()

        return self._render(status_update)