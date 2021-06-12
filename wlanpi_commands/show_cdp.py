from .command import Command

class ShowCDP(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_cdp"
    
    def run(self, args_list):
        
        # read in CDP data is available
        cdp_data = self._read_file('/tmp/cdpneigh.txt')

        if not cdp_data:
            cdp_data = "No CDP data found"

        return self._render(cdp_data)