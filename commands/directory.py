import subprocess
from modules.util.CommandUtils.ReturnStructure import RetObject

def run(arguments: list[str], ReturnObject: RetObject) -> RetObject:
    ReturnObject.exit_code = subprocess.run(
        ['dir']+arguments,
        shell=True
    ).returncode
    return ReturnObject