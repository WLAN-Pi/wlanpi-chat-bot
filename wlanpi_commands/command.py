import os
import subprocess
import textwrap

class Command():
    """
    Bare-bones class definition for commands to subclass
    """

    def __init__(self, telegram_object, conf_obj):

        self.conf_obj =  conf_obj
        self.command_name = "show_misc"
        self.display_mode = self.conf_obj.config['telegram']['display_mode']
        self.display_width = self.conf_obj.config['telegram']['display_width']
        self.telegram_object = telegram_object
    
    def _refresh_config(self):
        self.conf_obj.read_config()
        self.display_mode = self.conf_obj.config['telegram']['display_mode']
        self.display_width = self.conf_obj.config['telegram']['display_width']
    
    def _read_file(self, filename):

        if os.path.exists(filename):
            file_content = []

            try:
                with open(filename, 'r') as f:
                    for line in f:
                        file_content.append(line.strip())
                return file_content
            except Exception as ex:
                print("Issue reading lock file: {}, exiting...".format(ex))
                
        return False

    def _render_compact(self, data):
        """
        Render data in compact format to fit smaller display devices
        """

        if isinstance(data, str):
            return data[:self.display_width]
        elif isinstance(data, list):
           return  [w[:self.display_width] for w in data]
        else:
            raise ValueError("Unsupported data type passed to _render_compact: {}".format(type(data)))

    def _render(self, data):
        """
        Render data based on display preferences
        """
        # re-read config for display preferences in case changed
        self._refresh_config()

        if self.display_mode == "compact":
            return self._render_compact(data)
        
        
        if isinstance(data, str):
            return data
        elif isinstance(data, list):
           return data
        else:
            raise ValueError("Unsupported data type passed to _render_compact: {}".format(type(data)))
        

    def run_ext_cmd(self, progress_msg, cmd_string):

        # send status msg  
        chat_id = self.telegram_object.chat_id
        self.telegram_object.send_msg(progress_msg, chat_id)

        # perform test
        cmd_info = []

        try:
            cmd_output = subprocess.check_output(cmd_string, shell=True).decode().strip()
            cmd_info = cmd_output.split('\n')
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error = "Err: cmd error : {}".format(output)
            #self.telegram_object.send_msg(error, chat_id)
            return error

        if len(cmd_info) == 0:
            cmd_info.append("No output sorry")

        return cmd_info

    def run(self, data='', args_list=[]):

        # perform some operation
        result  = "This is useful data"

        return result


    def help_message(self):
        """
        Return the help page for this command
        """
        short_msg = "Help message short"
        long_msg = "A long message that could perhaps span a few lines...\n Who knows..?"

        if self.display_mode == "compact":
            return short_msg
        else:
            return long_msg

# import our commands
from .set_display_mode import SetDisplayMode
from .set_display_width import SetDisplayWidth
from .show_time import ShowTime
from .show_cdp import ShowCDP
from .show_publicip import ShowPublicip
from .show_reachability import ShowReachability
from .show_lldp import ShowLLDP
from .show_summary import ShowSummary
from .show_mode import ShowMode
from .exec_reboot import ExecReboot
from .exec_iperf import ExecIperf
from .exec_iperf3 import ExecIperf3
from .exec_ping import ExecPing
from .exec_speedtest import ExecSpeedtest
from .show_status import ShowStatus
from .show_version import ShowVersion


def register_commands(telegram_object, conf_obj):
    # Register all of our commands
    command_objects = []
    global_objs = list(globals().items())

    for name, obj in global_objs:
        if obj is not Command and isinstance(obj, type) and issubclass(obj, Command):
            command_objects.append(obj(telegram_object, conf_obj))

    # populate global command dictionary
    GLOBAL_CMD_DICT = {}
    for command_obj in command_objects:

        command_name = command_obj.command_name
        GLOBAL_CMD_DICT[command_name] = command_obj

    return GLOBAL_CMD_DICT