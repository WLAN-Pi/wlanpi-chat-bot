from .command import Command
import os
import subprocess

class ExecSpeedtest(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "exec_speedtest"
    
    def run(self, args_list):

        # send status msg  
        chat_id = self.telegram_object.chat_id
        self.telegram_object.send_msg("Running speedtest...please wait", chat_id)

        # perform speedtest
        speedtest_info = []
        speedtest_cmd = "speedtest | egrep -w \"Testing from|Download|Upload\" | sed -r 's/Testing from.*?\(/My IP: /g; s/\)\.\.\.//g; s/Download/D/g; s/Upload/U/g; s/bit\/s/bps/g'"

        try:
            speedtest_output = subprocess.check_output(speedtest_cmd, shell=True).decode().strip()
            speedtest_info = speedtest_output.split('\n')
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error = ["Err: Speedtest error", output]
            print(error)
            return False

        if len(speedtest_info) == 0:
            speedtest_info.append("No output sorry")

        return self._render(speedtest_info)