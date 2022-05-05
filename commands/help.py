from modules.util.extra import args
from modules.data.Help import Help
from modules.util.CommandUtils.ReturnStructure import RetObject

def run(arguments: list[str], ReturnObject: RetObject):
    arguments = [x for x in arguments if x]
    if not arguments:
        ReturnObject.exit_code = Help().showHelp()
    else:
        for command in arguments:
            print(f'---------------------{command}----------------------')
            ReturnObject.exit_code = Help(command).showHelp()
            if ReturnObject.exit_code:
                break
    return ReturnObject