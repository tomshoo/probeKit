import subprocess

from . import Runnable


class ChangeDirWin(Runnable):
    def run(self):
        self.retobj.exit_code = subprocess.run(
            ['dir']+self.args,
            shell=True
        ).returncode
        return self.retobj
