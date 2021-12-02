from .command import Command

class ShowMode(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_mode"
    
    def run(self, args_list):
        STATUS_FILE="/etc/wlanpi-state"
        status = "WLAN Pi mode: {}".format(self._read_file( STATUS_FILE)[0])
        return self._render(status.strip())

