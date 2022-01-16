import subprocess
import os

from .command import Command


class ShowEth0Vlan(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_eth0-vlan"
    

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
