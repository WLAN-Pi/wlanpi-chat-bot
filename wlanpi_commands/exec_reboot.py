from .command import Command
import os

class ExecReboot(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "exec_reboot"
    
    def run(self, args_list):        
        os.system('shutdown -r')
        return self._render("Attempting reboot in 1 minute...")