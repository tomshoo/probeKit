from config import default_command_dict
from . import Runnable


class Default(Runnable):
    def run(self):
        for command in default_command_dict:
            print(f"\t- {default_command_dict[command][0]}")
        self.retobj.exit_code = 0
        return self.retobj
