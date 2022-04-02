from platform import platform
from os import system, path
from modules.util.extra import args
from modules.util.ReturnStructure import RetObject
import readline
from sys import exit

def run(arg: list, ReturnObject: RetObject) -> RetObject:
    if args(arg, 0) and args(arg, 0) in ['-h', '--history']:
        readline.clear_history()

        if ReturnObject.histfile:
            if path.exists(ReturnObject.histfile):
                with open(ReturnObject.histfile, 'w') as hist_cls:
                    hist_cls.write('#Clear\n')


    if 'Windows' in platform(): system('cls')
    
    else:
        print(chr(27)+'2[j')
        print('\033c')
        print('\x1bc')

    if args(arg, 0) and args(arg, 0) == '-e': exit(ReturnObject.exit_code)

    ReturnObject.exit_code = 0
    return ReturnObject