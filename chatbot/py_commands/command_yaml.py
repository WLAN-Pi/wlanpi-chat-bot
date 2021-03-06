import subprocess

import chatbot.utils.emojis


class YamlCommand:
    """
    Class to run commands derived from a simple YAML file definition
    """

    def __init__(self, telegram_object, conf_obj):

        self.command_name = "show_misc"
        self.help_short = "Short help string"
        self.help_long = (
            "A much longer help string which might span several lines....who knows?"
        )
        self.exec = "echo No command passed to obj"
        self.progress_msg = "In progress..."
        self.emoji = ""

        self.conf_obj = conf_obj
        self.display_mode = self.conf_obj.config["telegram"]["display_mode"]
        self.display_width = self.conf_obj.config["telegram"]["display_width"]
        self.telegram_object = telegram_object

    def _refresh_config(self):
        self.conf_obj.read_config()
        self.display_mode = self.conf_obj.config["telegram"]["display_mode"]
        self.display_width = self.conf_obj.config["telegram"]["display_width"]

    def _render_compact(self):
        """
        Render data in compact format to fit smaller display devices
        """

        data = self.help_short

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

    def run(self, args):

        cmd_string = self.exec

        # add in args passed to the cmd
        arg_str = "".join(args)

        if "$args" in cmd_string:
            # substitute args in to command
            cmd_string = cmd_string.replace("$args$", arg_str)
            # else just append to command
        else:
            cmd_string += arg_str

        progress_msg = self.progress_msg

        # send status msg
        if progress_msg:
            if self.emoji:
                emoji = eval("chatbot.utils.emojis." + self.emoji + "()")
                progress_msg = emoji + progress_msg

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
            if output:
                error = "Err: {}".format(output)
                # self.telegram_object.send_msg(error, chat_id)
                return self._render(chatbot.utils.emojis.bad() + error)
            else:
                return self._render(chatbot.utils.emojis.bad() + str(exc))
        except Exception as err:
            return self._render(
                chatbot.utils.emojis.bad()
                + f"problem getting output from '{cmd_string}'"
            )

        if len(cmd_info) == 0:
            cmd_info.append("No output sorry")

        return self._render([chatbot.utils.emojis.good() + " OK"] + cmd_info)

    def help(self):
        """
        Return the help page for this command
        """
        short_msg = self.help_short
        long_msg = self.help_long

        if self.display_mode == "compact":
            return short_msg
        else:
            return chatbot.utils.emojis.help() + " " + long_msg
