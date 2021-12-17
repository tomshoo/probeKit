from platform import platform
from os import system, path
from modules.util.utils import args
import readline
from sys import exit

def run(arg: list, exit_code: int, histfile: str = None) -> int:
    if args(arg, 0) and args(arg, 0) == '-e': exit(exit_code)

    if args(arg, 0) and args(arg, 0) in ['-h', '--history']:
        readline.clear_history()

        if histfile:
            if path.exists(histfile):
                with open(histfile, 'w') as hist_cls:
                    hist_cls.write('#Clear\n')


    if 'Windows' in platform(): system('cls')
    
    else:
        print(chr(27)+'2[j')
        print('\033c')
        print('\x1bc')

    return 0