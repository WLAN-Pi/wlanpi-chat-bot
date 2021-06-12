from .command import Command
import socket
import subprocess

class ShowSummary(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_summary"
    
    def run(self, args_list):
        
        # Taken from FPMS...

        # figure out our IP
        IP = ''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        
        # determine CPU load
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        try:
            CPU = subprocess.check_output(cmd, shell=True).decode()
        except:
            CPU = "unknown"

        # determine mem useage
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        try:
            MemUsage = subprocess.check_output(cmd, shell=True).decode()
        except:
            MemUsage = "unknown"

        # determine disk util
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        try:
            Disk = subprocess.check_output(cmd, shell=True).decode()
        except:
            Disk = "unknown"

        # determine temp
        try:
            tempI = int(open('/sys/class/thermal/thermal_zone0/temp').read())
        except:
            tempI = "unknown"

        if tempI > 1000:
            tempI = tempI/1000
        tempStr = "CPU TEMP: %sC" % str(tempI)

        results = [
            "System Summary Info:",
            "IP: {}".format(IP),
            str(CPU),
            str(MemUsage),
            str(Disk),
            tempStr
        ]

        return self._render(results)