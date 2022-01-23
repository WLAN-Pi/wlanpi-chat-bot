import subprocess
import os

from .command import Command


class ShowEth0Vlan(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_eth0-vlan"
    
    def help(self):
        """
        Return the help page for this command
        """
        short_msg = "Show the VLAN info for eth0"
        long_msg = (
            """Shows the VLAN information for eth0
Syntax: show eth0-vlan"""
        )

        if self.display_mode == "compact":
            return short_msg
        
        return long_msg

    def run(self, args_list):

        # Taken from FPMS...

        '''
        Display untagged VLAN number on eth0
        Todo: Add tagged VLAN info
        '''
        LLDPNEIGH_FILE = '/tmp/lldpneigh.txt'
        CDPNEIGH_FILE = '/tmp/cdpneigh.txt'

        vlan_info = []

        vlan_cmd = "sudo grep -a VLAN " + LLDPNEIGH_FILE + " || grep -a VLAN " + CDPNEIGH_FILE

        if os.path.exists(LLDPNEIGH_FILE):

            try:
                vlan_output = subprocess.check_output(vlan_cmd, shell=True).decode()
                vlan_info = vlan_output.split('\n')

                if len(vlan_info) == 0:
                    vlan_info.append("No VLAN found")

            except:
                vlan_info = ["No VLAN found"]

        final_page = "Eth0 IP VLAN:\n\n"

        final_page += "\n".join(vlan_info)

        return self._render(final_page)
