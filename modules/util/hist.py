from rich import traceback
from modules.util.utils import trim, timefunc
from os import path

traceback.install()

class register_history():
    """
    Class to register history,

    * Does not work in windows. *
    """

    def __init__(self, command : str):
        self.command = command
        self.histfile : str = path.join(path.expanduser('~'), '.probeKit.history')

    def __hastimestamp(self) -> bool:
        command: str = self.command
        if '#' in command:
            comment_index: str = command.index('#')
            comment = command[comment_index+1::]
            comment = trim(comment)
            try:
                time.strptime(comment, "%a %Y-%m-%d %H:%M:%S")
                return True
            except ValueError: return False
        else: return False

    def write_history(self):
        """write the history to $HOME/.probeKit.history"""
        histfile = self.histfile
        if not self.__hastimestamp():
            if path.exists(histfile):
                with open(histfile, 'a') as fp:
                    fp.write(self.command + f' # {timefunc.datevalue()} \n')
                    pass
            else:
                with open(histfile, 'w') as fp:
                    fp.write(self.command + f' # {timefunc.datevalue()} \n')
                    pass