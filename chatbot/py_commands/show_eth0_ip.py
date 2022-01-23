import socket
import subprocess
import re

from .command import Command


class ShowEth0Ip(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_eth0-ip"
    
    def help(self):
        """
        Return the help page for this command
        """
        short_msg = "Show the IP and duplex/speed for eth0"
        long_msg = (
            """show eth0-ip: This command shows the IP, subnet mask, DNS servers, DHCP server and duplex/speed information for eth0"""
        )

        if self.display_mode == "compact":
            return short_msg
        
        return long_msg
    

    def run(self, args_list):

        # Taken from FPMS...

        '''
        Return IP configuration of eth0 including IP, default gateway, DNS servers
        '''
        IPCONFIG_FILE = "/usr/bin/ipconfig"

        eth0_ipconfig_info = []

        try:
            ipconfig_output = subprocess.check_output(IPCONFIG_FILE, shell=True).decode().strip()
            ipconfig_info = ipconfig_output.split('\n')
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            print("Err: ipconfig command error", output)
            return

        for n in ipconfig_info:
            # do some cleanup
            n = n.replace("DHCP server name", "DHCP")
            n = n.replace("DHCP server address", "DHCP IP")
            eth0_ipconfig_info.append(n)

        if len(ipconfig_info) <= 1:
            eth0_ipconfig_info = ["Eth0 is down or not connected."]

        final_page = "Eth0 IP Config:\n\n"

        final_page += "\n".join(eth0_ipconfig_info)

        return self._render(final_page)
