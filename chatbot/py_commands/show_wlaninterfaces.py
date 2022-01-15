import socket
import subprocess
import re

from .command import Command


class ShowWlanInterfaces(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_wlan-interfaces"
    
    def channel_lookup(self, freq_mhz):
        '''
        Converts frequency (MHz) to channel number
        '''
        if freq_mhz == 2484:
            return 14
        elif freq_mhz >= 2412 and freq_mhz <= 2484:
            return int(((freq_mhz - 2412) / 5) + 1)
        elif freq_mhz >= 5160 and freq_mhz <= 5885:
            return int(((freq_mhz - 5180) / 5) + 36)
        elif freq_mhz >= 5955 and freq_mhz <= 7115:
            return int(((freq_mhz - 5955) / 5) + 1)

        return None

    def run(self, args_list):

        # Taken from FPMS...

        '''
        Create pages to summarise WLAN interface info
        '''
        IWCONFIG_FILE = "/usr/sbin/iwconfig"
        IW_FILE = "/usr/sbin/iw"
        ETHTOOL_FILE = "/usr/sbin/ethtool"

        interfaces = []
        pages = []

        try:
            interfaces = subprocess.check_output(f"{IWCONFIG_FILE} 2>&1 | grep 802.11" + "| awk '{ print $1 }'", shell=True).decode().strip().split()
        except Exception as e:
            print(e)

        for interface in interfaces:
            page = []
            page.append(f"Interface: {interface}")

            # Driver
            try:
                ethtool_output = subprocess.check_output(f"{ETHTOOL_FILE} -i {interface}", shell=True).decode().strip()
                driver = re.search(".*driver:\s+(.*)", ethtool_output).group(1)
                page.append(f"Driver: {driver}")
            except subprocess.CalledProcessError as exc:
                output = exc.ethtool_output.decode()
                print(output)

            # Addr, SSID, Mode, Channel
            try:
                iw_output = subprocess.check_output(f"{IW_FILE} {interface} info", shell=True).decode().strip()
            except subprocess.CalledProcessError as exc:
                output = exc.iw_output.decode()
                print(output)

            # Addr
            try:
                addr = re.search(".*addr\s+(.*)", iw_output).group(1).replace(":", "").upper()
                page.append(f"Addr: {addr}")
            except Exception:
                pass

            # Mode
            try:
                mode = re.search(".*type\s+(.*)", iw_output).group(1)
                page.append(f"Mode: {mode.capitalize() if not mode.isupper() else mode}")
            except Exception:
                pass

            # SSID
            try:
                ssid = re.search(".*ssid\s+(.*)", iw_output).group(1)
                page.append(f"SSID: {ssid}")
            except Exception:
                pass

            # Frequency
            try:
                freq = int(re.search(".*\(([0-9]+)\s+MHz\).*", iw_output).group(1))
                channel = self.channel_lookup(freq)
                page.append(f"Freq (MHz): {freq}")
                page.append(f"Channel: {channel}")
            except Exception:
                pass

            pages.append(page)

        final_page = "WLAN Interfaces:\n\n"

        for page in pages:
            final_page += "\n".join(page) + "\n\n"

        return self._render(final_page)
