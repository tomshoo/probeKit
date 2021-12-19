"""
This file contains all the necessary utilities required for other
programs or modules.

If you want to create some other utility please create it in this
file and later import it from here.
"""

# Imports
from datetime import datetime
import time
import ctypes
import sys
from os import path, getuid
from multipledispatch import dispatch
from rich import traceback
from collections import namedtuple
traceback.install()

# Named tuple containing all available commands for both `interpreter`, `probekit`
completer = namedtuple("Completers", ['interpreter', 'led'])
completers = completer(
    [
        "use", 
        "show", 
        "set", 
        "help", 
        "exit", 
        "back", 
        "clear", 
        "run", 
        "about", 
        "list", 
        "banner", 
        "alias", 
        "unalias", 
        "unset"
    ],
    [
        "i", "insert",
        "w", "write",
        "c", "change",
        "p", "print",
        "n", "lineprint",
        "q", "quit",
    ]
)

class splitters:
    @staticmethod
    def bracket(string: str, bropen: str = '('):
        openbr: str = '({[<'
        closebr: str = ')}]>'
        if bropen in openbr: brclose = closebr[openbr.find(bropen)]
        else:
            print("Not a valid bracket...")
            return None
        str_container: list = []
        form_string: str = ''
        check: int = 0
        nbuff: int = 0
        for ch in string:
            if check == 1: form_string+=ch
            if ch == bropen:
                check = 1
                nbuff+=1
            if ch == brclose:
                nbuff-=1
                if nbuff == 0: check = 0
                if nbuff < 0:
                    print("Extra closing bracket found. Qutting...")
                    check = 1
                    break
            if check == 0:
                if form_string:
                    uneeded = list(form_string)
                    uneeded.pop()
                    form_string=''.join(uneeded)
                    del(uneeded)
                    str_container.append(form_string)
                    form_string = ''
        if check == 0: return str_container
        else:
            if nbuff >= 0: print("Extra opening bracket found. Quitting...")
            return None

    # @staticmethod
    # def quote(key: str, quotekey: str, string: str) -> list:
    #     for l in csv.reader([string], delimiter=key, quotechar=quotekey): split_quoted = l
    #     return split_quoted

    @staticmethod
    def quote(string: str, delimiter: str = ' ') -> list:
        if delimiter.isalnum(): raise ValueError('delimiter cannot be an alpha-numeric character')
        form_string: str = ''
        str_container: list = []
        quote_string: str = ''
        check: int = 0
        previous_state: int = 0
        for ch in string:
            previous_state = check
            if ch == '\'':
                if check == 2:
                    pass
                elif check == 1:
                    check = 0
                elif check == 0:
                    check = 1
            if ch == '"':
                if check == 2:
                    check = 0
                elif check == 1:
                    pass
                elif check == 0:
                    check = 2
            if check == 0:
                if previous_state != check:
                    str_container.append(quote_string)
                    quote_string = ''
                elif ch != delimiter and previous_state == check:
                    form_string+=ch
                else:
                    if form_string:
                        str_container.append(form_string)
                        form_string=''
            else:
                if form_string: str_container.append(form_string); form_string=''
                if check == 2 and ch == '"': pass
                elif check == 1 and ch == '\'': pass
                else: quote_string+=ch
        if form_string:
            str_container.append(form_string)
        del(form_string)
        return str_container

def args(value: list, pos: int) -> str:
    """
    A simple function to return values in a list and raise exception
    in such a way that the interpreter doesn't break
    """

    try: return str(value[int(pos)])
    except Exception: return ''

class completer:
    """tab completion class(experimental)"""
    def __init__(self, commands): self.commands = commands
    def completion(self, text: str, state: int):
        """return valid commands from the list of commands provided"""
        commands = self.commands
        options = [i for i in commands if i.startswith(text.lower())]
        if state < len(options): return options[state]
        else: return None

class string(str):
    def isfloat(self)->bool:
        ssplit = self.split('.')
        length: int = len(ssplit)
        FloatList: list = []
        if 0 < length <= 2:
            for x in ssplit:
                FloatList.append(x.isdecimal())
            if False in FloatList: return False
            else: return True
        else: return False

def trim(string: str) -> str:
    """Function to remove extra white spaces from the string"""

    strsplit : list = string.split()
    return ' '.join(strsplit)

class ExitException(Exception):
    """Custom "dummy" exception to exit the session"""
    pass

def datevalue() -> str:
    """Function to get immediate time at a point"""

    return datetime.now().strftime('%a %Y-%m-%d %H:%M:%S')

@dispatch(int)
def Exit(exitStatus: int): sys.exit(exitStatus)

@dispatch(int, str)
def Exit(exitStatus: int, histfile: str):
    """End the session and append the date and time to the end of the history file."""

    with open(histfile, 'a') as fp:
        fp.write('# session ended at: ' + datevalue() + ' # \n')
        pass
    sys.exit(exitStatus)

def isAdmin() -> bool:
    try: return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError: return getuid() == 0

def timestamp() -> float:
    """To get total time taken by things to load and run"""

    return time.perf_counter()

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
                    fp.write(self.command + f' # {datevalue()} \n')
                    pass
            else:
                with open(histfile, 'w') as fp:
                    fp.write(self.command + f' # {datevalue()} \n')
                    pass

class optionsparser:
    """
    Parse the dictionary read from `config.json`
    Assign desired values to the value key for each value
    """
    def __init__(self, option_dict: dict) -> None:
        self.option_dict = option_dict


    def __typeset(self, dtype: str):
        """
        Return the type object required as per the `dtype` key found in the scheme
        """
        dtype = dtype.lower()
        if dtype == "str": return str
        elif dtype == "int": return int
        elif dtype == "float": return float
        elif dtype == "bool": return bool
        else: raise Exception(f"Invalid dtype value \'{dtype}\'")

    def __dictparser(self, data: str) -> None:
        """
        Parse the value where type of value is specified as a dictionary
        If type is mentioned as dictionary, the value is a dictionary containing two values:
         - value: containing the value that needs to be sent to module
         - type: the type of value,
           - This key would not hold the data-type of the value,
           - It hold the type mentioned in the module, for example:
             module: probe, option: tport, (value: 1/8000, type: range)/(value: 1,8000, type: group)
        """
        option_dict: dict = self.option_dict
        data_value: dict  = option_dict[data]['value']
        data_rules: dict = option_dict[data]['typerules']
        if type(data_value['value']) is str:
            for scheme in data_rules:
                rule: dict = data_rules.get(scheme)
                identifier: str = rule.get('identifier')
                if identifier:
                    if identifier in data_value['value']: 
                        if rule.get('type') == "list":
                            data_value['type'] = scheme
                            if rule.get('delimeter'):
                                data_value['value'] = data_value['value'].split(rule.get('delimeter'))
                                break
                            else: print('Err: no delimeter found... cannot split.')
                        else:
                            dtype = rule.get('dtype')
                            _type = rule.get('type')
                            dtype = self.__typeset(dtype)
                            data_value['value'] = dtype(data_value['value'])
                            data_value['type'] = scheme
                            break
                else:
                    dtype = self.__typeset(rule.get("dtype"))
                    data_value['value'] = '' if not data_value.get('value') and type(data_value.get('value')) is str else dtype(data_value.get('value'))
                    data_value['type'] = scheme
        self.option_dict = option_dict

    def parse(self) -> dict:
        """
        Parse the option dictionary assigning appropriate values for the options
        """
        option_dict = self.option_dict
        for data in option_dict:
            if option_dict[data].get('value') is None:
                if option_dict[data].get('type') == "dict":
                    option_dict[data]['value'] = {
                        'value': '',
                        'type': ''
                    }
                else: option_dict[data]['value'] = ''

            if option_dict[data].get('type'):
                if option_dict[data]['type'] == "dict":
                    if not option_dict[data].get('typerules'): print('Err: No type rule found... skipping value')
                    else:
                        if type(option_dict[data]['typerules']) is not dict: print('Invalid type rule scheme... skipping value')
                        else:
                            try: self.__dictparser(data)
                            except TypeError as e: print(f'Something went wrong... => {e}')
                    pass

                elif option_dict[data]['type'] == "int": 
                    if type(option_dict[data]['value']) is not int:
                        if option_dict[data]['value'].isdecimal(): option_dict[data]['value'] = int(option_dict[data]['value'])
                        else: option_dict[data]['value'] = ""
                    else: pass

                elif option_dict[data]['type'] == "float": 
                    if type(option_dict[data]['value']) is not float:
                        if string(option_dict[data]['value']).isfloat(): option_dict[data]['value'] = float(option_dict[data]['value'])
                        else: option_dict[data]['value'] = ""
                    else: pass

                elif option_dict[data]['type'] == "bool":
                    if type(option_dict[data]['value']) is not bool:
                        if option_dict[data]['value'].lower() in ['true', 'false']:
                            if option_dict[data]['value'].lower() == "true": option_dict[data]['value'] = True
                            else: option_dict[data]['value'] = False
                        else: option_dict[data]['value'] = ""
                    else: pass

                elif option_dict[data]['type'] == "str": pass

                else:
                    _type = option_dict[data]['type']
                    print(f'Error: Invalid type: {_type}')
                    delete(_type)
                    sys.exit(1)

        return option_dict
