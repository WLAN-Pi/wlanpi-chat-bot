from .command import Command
from utils.config import Config

class SetDisplayWidth(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "set_display_width"
    
    def run(self, args_list):

        # check we have an arg to specify "compact" or "full"
        if not len(args_list) > 0:
            return self._render("Missing argument - specify number chars required")
        
        display_width = int(args_list[0])

        # TODO: check is an integer
        if not display_width:
            return self._render("incorrect argument - specify number chars required")
        
        # read in config
        conf_obj = Config()
        if not conf_obj.read_config():
            return self._render("Config file read error.")

        conf_obj.config['telegram']['display_width'] =  int(display_width)

        if not conf_obj.update_config():
            return self._render("Config file write error.")

        return self._render("Config updated.")

