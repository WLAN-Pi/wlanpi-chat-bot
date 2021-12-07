import glob
import os
import subprocess

import yaml

import chatbot.utils.emojis


class Command:
    """
    Bare-bones class definition for commands to subclass
    """

    def __init__(self, telegram_object, conf_obj):

        self.conf_obj = conf_obj
        self.command_name = "show_misc"
        self.display_mode = self.conf_obj.config["telegram"]["display_mode"]
        self.display_width = self.conf_obj.config["telegram"]["display_width"]
        self.telegram_object = telegram_object

    def _refresh_config(self):
        self.conf_obj.read_config()
        self.display_mode = self.conf_obj.config["telegram"]["display_mode"]
        self.display_width = self.conf_obj.config["telegram"]["display_width"]

    def _read_file(self, filename):

        if os.path.exists(filename):
            file_content = []

            try:
                with open(filename, "r") as f:
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
            return data[: self.display_width]
        elif isinstance(data, list):
            return [w[: self.display_width] for w in data]
        else:
            raise ValueError(
                "Unsupported data type passed to _render_compact: {}".format(type(data))
            )

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
            raise ValueError(
                "Unsupported data type passed to _render_compact: {}".format(type(data))
            )

    def run_ext_cmd(self, progress_msg, cmd_string):

        # send status msg
        chat_id = self.telegram_object.chat_id
        self.telegram_object.send_msg(progress_msg, chat_id)

        # perform test
        cmd_info = []

        try:
            cmd_output = (
                subprocess.check_output(cmd_string, shell=True).decode().strip()
            )
            cmd_info = cmd_output.split("\n")
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error = "Err: cmd error : {}".format(output)
            # self.telegram_object.send_msg(error, chat_id)
            return error

        if len(cmd_info) == 0:
            cmd_info.append("No output sorry")

        return cmd_info

    def run(self, data="", args_list=[]):

        # perform some operation
        result = "This is useful data"

        return result

    def help(self):
        """
        Return the help page for this command
        """
        short_msg = "Short default help msg"
        long_msg = (
            "Help: If you see this help message, Nigel and Jiri haven't yet defined a help msg for this command.\n Drop them a note to tell them to stop drinking beer/coffee and get coding..! "
            + chatbot.utils.emojis.coffee()
        )

        if self.display_mode == "compact":
            return short_msg
        else:
            return long_msg


from .iperf import Iperf
from .iperf3 import Iperf3
from .ping import Ping
from .reboot import Reboot

# import our commands
from .set_display_mode import SetDisplayMode
from .set_display_width import SetDisplayWidth
from .show_mode import ShowMode
from .show_status import ShowStatus
from .show_summary import ShowSummary
from .show_time import ShowTime
from .show_uptime import ShowUptime
from .show_version import ShowVersion
from .speedtest import Speedtest


def register_commands(telegram_object, conf_obj):
    # Register all of our class-based commands
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

    # register all of our YAML based commands
    # (each of the files are read and a new object created using the data in the YAML file)

    # Read all available command files
    yaml_files = glob.glob("{}/*.yml".format(conf_obj.config["telegram"]["yaml_cmds"]))

    # import yaml command object
    from .command_yaml import YamlCommand

    # Create object & add obj params (exec, help, name etc.)
    for yaml_file in yaml_files:

        with open(yaml_file, "r") as stream:

            # read in yaml file & parse in to dict
            try:
                cmd_values = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print("YAML file read error : {}".format(exc))
                continue

            # create a new object and add values from the YAML file
            yaml_cmd_obj = YamlCommand(telegram_object, conf_obj)

            # assign the values from the yaml command file to the new obj
            yaml_cmd_obj.command_name = cmd_values["command"]
            yaml_cmd_obj.help_short = cmd_values["help_short"]
            yaml_cmd_obj.help_long = cmd_values["help_long"]
            yaml_cmd_obj.exec = cmd_values["exec"]
            yaml_cmd_obj.progress_msg = cmd_values["progress_msg"]
            yaml_cmd_obj.emoji = cmd_values["emoji"]

            # add the new command to the global command dict
            GLOBAL_CMD_DICT[yaml_cmd_obj.command_name] = yaml_cmd_obj

    return GLOBAL_CMD_DICT
