from .command import Command

class ShowTime(Command):
    
    def __init__(self, telegram_object, conf_obj):
        super().__init__(telegram_object, conf_obj)

        self.command_name = "show_time"
    
    def run(self, args_list):
        import time
        return self._render(time.ctime())

