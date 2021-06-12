from .command import Command
from utils.config import Config

class SetDisplayMode(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "set_display_mode"
    
    def run(self, args_list):

        # check we have an arg to specify "compact" or "full"
        if not len(args_list) > 0:
            return self._render("Missing argument - specify 'full' or 'compact'")
        
        display_mode = args_list[0]

        if (display_mode != 'full') and (display_mode != 'compact'):
            return self._render("incorrect argument - specify 'full' or 'compact'")
        
        # read in config
        conf_obj = Config()
        if not conf_obj.read_config():
            return self._render("Config file read error.")

        conf_obj.config['telegram']['display_mode'] =  display_mode

        if not conf_obj.update_config():
            return self._render("Config file write error.")

        return self._render("Config updated.")

