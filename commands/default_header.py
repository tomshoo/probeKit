from config import default_command_dict
from modules.util.CommandUtils.ReturnStructure import RetObject

def run(_: list[str], ReturnObject: RetObject):
    for command in default_command_dict:
        print(f'\t- {default_command_dict[command][0]}')
    ReturnObject.exit_code = 0
    return ReturnObject