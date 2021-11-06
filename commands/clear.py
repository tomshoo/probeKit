from platform import platform
from os import system
from modules.util.utils import args
from sys import exit

def run(arg: list, exit_code: int) -> int:
    if args(arg, 0) and args(arg, 0) == '-e':
        exit(exit_code)

    if 'Windows' in platform():
        system('cls')
    
    else:
        print(chr(27)+'2[j')
        print('\033c')
        print('\x1bc')

    return 0