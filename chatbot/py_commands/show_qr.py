from PIL import Image
import os
import qrcode
import hashlib
import subprocess
from .command import Command
import chatbot.utils.emojis


class ShowQr(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_qr"
    
    
    def get_wifi_qrcode(self, ssid, passphrase):
        qrcode_spec = "WIFI:S:{};T:WPA;P:{};;".format(ssid, passphrase)
        qrcode_hash = hashlib.sha1(qrcode_spec.encode()).hexdigest()
        qrcode_path = "/tmp/{}.png".format(qrcode_hash)

        if not os.path.exists(qrcode_path):
            qr = qrcode.QRCode(box_size=2, border=3, error_correction=qrcode.constants.ERROR_CORRECT_M)
            qr.add_data(qrcode_spec)
            qr.make(fit=False)
            qr.make_image().save(qrcode_path)

        return qrcode_path
    

    def get_wifi_qrcode_for_hostapd(self):
        '''
        Generates and returns the path to a WiFi QR code for the current Hostapd config.
        '''
        hostapd_cfg_file = "/etc/hostapd/hostapd.conf"

        # check we have a config file (i.e. are we in right mode?)
        if not os.path.exists(hostapd_cfg_file):
            return None
        
        cmd = f"grep -E '^ssid|^wpa_passphrase' {hostapd_cfg_file} | cut -d '=' -f2"

        try:
            ssid, passphrase = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip().split("\n")
            return self.get_wifi_qrcode(ssid, passphrase)

        except Exception as e:
            print(e)
            pass

        return None
    
    def help(self):
        """
        Return the help page for this command
        """
        short_msg = "Show the QR code for SSID in the current mode"
        long_msg = (
            """This command shows a QR code that can be scanned with a smartphone (or similar) to connect to the SSID that is currently being broadcast. 
    
The availability of the SSID is dependant on the current mode of the WLAN Pi."""
        )

        if self.display_mode == "compact":
            return short_msg
        else:
            return long_msg


    def run(self, args_list):

        # get the QR code file name
        qr_file = self.get_wifi_qrcode_for_hostapd()

        status_update = chatbot.utils.emojis.bad() + """ Unable to create QR code.

Is the WLAN Pi in the correct mode? (must be in mode which uses the AP feature such as hotspot mode)"""

        # read in the file as binary
        if qr_file:
            # return as dict to signa non-std data type (not str or list)
            status_update = { "type": "image", "filename": qr_file, "caption": "Wi-Fi QR Code"}

        return self._render(status_update)
