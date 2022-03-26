from typing import Union
from types import FunctionType
from modules.util._Commands import Commands
from config import valid_modules
from modules.util.ReturnStructure import RetObject
class CreateCommand:
    """
    Required Keyword Arguments:
    - argumnets
    - option_dict -> dict[str]
    - aliases -> dict[str]
    - macros -> dict[str]
    - activated_module_list -> list[str] #list of active modules activated by the use command
    """
    def __init__(self, **kwargs) -> None:
        self.arguments = kwargs['arguments']
        self.option_dict = kwargs['option_dict']
        self.modules = [module for module in valid_modules]
        self.aliases = kwargs['aliases']
        self.macros = kwargs['macros']
        self.activated_module_list = kwargs['activated_module_list']
        self.module = kwargs['module']
        self.histfile = kwargs['histfile']

    def create_struct(self) -> RetObject:
        Struct: RetObject = RetObject()
        Struct.option_dict = self.option_dict
        Struct.aliases = self.aliases
        Struct.macros = self.macros
        Struct.activated_module_list = self.activated_module_list
        Struct.module = self.module
        Struct.histfile = self.histfile
        return Struct
    
    def run(self, command: str) -> Union[RetObject, None]:
        if command in Commands:
            ReturnObject = _RunCommand(command)(self.arguments, self.create_struct())
            ReturnObject.command_found = True
            return ReturnObject
        else:
            ReturnObject = RetObject()
            ReturnObject.command_found = False
            ReturnObject.exit_code = 1
            return ReturnObject


class _RunCommand:
    def __init__(self, command: str):
        self.command = command
    
    def __call__(self, arguments: list[str], ReturnObject: RetObject) -> RetObject:
        command = Commands.get(self.command)
        if isinstance(command, FunctionType):
            return command(arguments, ReturnObject)
        else:
            command_object = command(arguments, ReturnObject)
            return command_object.run()