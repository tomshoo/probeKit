from typing import Any
from types import FunctionType
from modules.util.CommandUtils._Commands import Commands
from modules.util.CommandUtils.ReturnStructure import RetObject


# fmt: off
class CreateCommand:
    """
    Required Keyword Arguments:
    - arguments             -> list[str]
    - option_dict           -> dict[str]
    - aliases               -> dict[str]
    - macros                -> dict[str]
    - activated_module_list -> list[str] #list of active modules activated by the use command
    - module                -> str currently activated module
    - histfile              -> location of history file
    """

    def __init__(self, **kwargs) -> None:
        self.arguments: list[str]                 = kwargs['arguments']
        self.option_dict: dict[str, Any]          = kwargs['option_dict']
        self.aliases: dict[str, tuple[str, bool]] = kwargs['aliases']
        self.macros: dict[str, str]               = kwargs['macros']
        self.activated_module_list: list[str]     = kwargs['activated_module_list']
        self.module: str                          = kwargs['module']
        self.histfile: str                        = kwargs['histfile']

    def create_struct(self) -> RetObject:
        cmdclass: RetObject            = RetObject()
        cmdclass.option_dict           = self.option_dict
        cmdclass.aliases               = self.aliases
        cmdclass.macros                = self.macros
        cmdclass.activated_module_list = self.activated_module_list
        cmdclass.module                = self.module
        cmdclass.histfile              = self.histfile
        return cmdclass

    def run(self, command: str) -> RetObject:
        if (cmd := Commands.get(command)):
            retobj = _RunCommand(cmd)(
                self.arguments, self.create_struct())
            retobj.command_found = True
            return retobj
        else:
            retobj = RetObject()
            retobj.command_found = False
            retobj.exit_code = 1
            return retobj


# fmt: on
class _RunCommand:
    def __init__(self, command: Any):
        self.command = command

    def __call__(self, arguments: list[str], ReturnObject: RetObject) -> RetObject:
        command = self.command
        if isinstance(command, FunctionType):
            return command(arguments, ReturnObject)
        else:
            command_object = command(arguments, ReturnObject)
            return command_object.run()
