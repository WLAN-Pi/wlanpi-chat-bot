from .command import Command
import os

class ShowVersion(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_ver"
    
    def run(self, args_list):
        
        WLANPI_IMAGE_FILE = '/etc/wlanpi-release'
        BOT_VER_FILE = '/opt/wlanpi-chat-bot/version.txt'

        version_string = ""
        
        if os.path.isfile(WLANPI_IMAGE_FILE):
            with open(WLANPI_IMAGE_FILE, 'r') as f:
                lines = f.readlines()
            
            # pull out the version number
            for line in lines:
                (name, value) = line.split("=")
                if name=="VERSION":
                    version = value.strip()
                    version_string = "WLAN Pi: " + version[1:-1]
                    break
        else: 
            version_string = "WLAN Pi: unknown"         

        if os.path.isfile(BOT_VER_FILE):
            with open(BOT_VER_FILE, 'r') as botf:
                # version file is singe line
                version = botf.readline()
            
            if version:
                version = version.strip()
                version_string += "\nBot: " + version
        else:
            version_string += "\nBot: unknown"
 
        return self._render(version_string)