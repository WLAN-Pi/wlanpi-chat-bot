from .command import Command

class ShowLLDP(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_lldp"
    
    def run(self, args_list):
        
        # read in CDP data is available
        cdp_data = self._read_file('/tmp/lldpneigh.txt')

        if not cdp_data:
            cdp_data = "No LLDP data found"

        return self._render(cdp_data)