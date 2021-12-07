from chatbot.utils.uptime import Uptime

from .command import Command


class ShowUptime(Command):
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_uptime"

    def run(self, args_list):
        import time

        uptime_obj = Uptime()
        return self._render(uptime_obj.get_uptime())
