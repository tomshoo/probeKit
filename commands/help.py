from modules.data.Help import Help as _Help

from . import Runnable


class Help(Runnable):
    def run(self):
        self.args = [x for x in self.args if x]
        if not self.args:
            self.retobj.exit_code = _Help('').showHelp()
        else:
            for command in self.args:
                print(f"---------------------{command}----------------------")
                self.retobj.exit_code = _Help(command).showHelp()
                if self.retobj.exit_code:
                    break
        return self.retobj
