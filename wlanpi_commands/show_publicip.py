from .command import Command

class ShowPublicip(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_publicip"
       
    def run(self, args_list):      

        progress_msg = "Getting Public IP..."
        cmd_string = "/usr/share/fpms/BakeBit/Software/Python/scripts/networkinfo/publicip.sh"
        return self._render(self.run_ext_cmd(progress_msg,cmd_string))
