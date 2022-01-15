import socket
import subprocess
import re

from .command import Command


class ShowInterfaces(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_interfaces"
    

    def run(self, args_list):

        # Taken from FPMS...

        '''
        Return the list of network interfaces with IP address (if available)
        '''
        IFCONFIG_FILE = "/usr/sbin/ifconfig"
        IW_FILE = "/usr/sbin/iw"

        try:
            ifconfig_info = subprocess.check_output(f"{IFCONFIG_FILE} -a", shell=True).decode()
        except Exception as ex:
            print("Err: ifconfig error", str(ex))
            return

        # Extract interface info with a bit of regex magic
        interface_re = re.findall(
            r'^(\w+?)\: flags(.*?)RX packets', ifconfig_info, re.DOTALL | re.MULTILINE)
        if interface_re is None:
            # Something broke is our regex - report an issue
            print("Error: match error")
        else:
            interfaces = []
            for result in interface_re:

                # save the interface name
                interface_name = result[0]

                # look at the rest of the interface info & extract IP if available
                interface_info = result[1]

                # determine interface status
                status = "▲" if re.search("UP", interface_info, re.MULTILINE) is not None else "▽"

                # determine IP address
                inet_search = re.search(
                    "inet (.+?) ", interface_info, re.MULTILINE)
                if inet_search is None:
                    ip_address = "-"

                    # do check if this is an interface in monitor mode
                    if (re.search(r"(wlan\d+)|(mon\d+)", interface_name, re.MULTILINE)):

                        # fire up 'iw' for this interface (hmmm..is this a bit of an un-necessary ovehead?)
                        try:
                            iw_info = subprocess.check_output('{} {} info'.format(IW_FILE, interface_name), shell=True).decode()

                            if re.search("type monitor", iw_info, re.MULTILINE):
                                ip_address = "Monitor"
                        except:
                            ip_address = "-"
                else:
                    ip_address = inet_search.group(1)

                # format interface info
                interfaces.append('{}  {} : {}'.format(status, interface_name, ip_address))

        final_page = "Interfaces:\n\n"

        final_page += "\n".join(interfaces)

        return self._render(final_page)
