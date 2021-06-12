from .command import Command
import os
import subprocess

class ExecPing(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "exec_ping"
    
    def run(self, args_list):

        PING = '/usr/bin/ping'
        target_ip = ''

        if len(args_list) > 0:
            target_ip = args_list[0]
        else:
            return self._render("Unable to run test, no IP address passed (syntax : exec ping &lt;ip_address&gt;)")

        progress_msg = "Runing ping test..."
        cmd_string = "{} -c 10 -W 1 -i 0.2 {} 2>&1".format(PING, target_ip) 
        return self._render(self.run_ext_cmd(progress_msg,cmd_string))
