#! /usr/bin/env python3

# This is a module selector and doesn't use many commands as it is used to only select module

import sys
import mod_interpreter as modinterpreter
import modules.data.OptInfHelp as data
import modules.data.AboutList as Module
from config import colors, aliases

FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FNORMAL = colors.FNORMAL
FURGENT = colors.FURGENT

banner = modinterpreter.banner()
Mod = Module.moduleHelp('')

exitStatus = FSUCCESS+'0'

try:
    while True:
        inputval = input(FNORMAL+'[probkit]:'+f' {exitStatus}'+FNORMAL+'$> ')

        if '#' in inputval:
            if inputval[0] == '#':
                pass
            else:
                inputval = inputval[:inputval.index('#'):]

        if inputval[len(inputval)-1::] != ';':
            valsplit = list(inputval)
            valsplit.append(';')
            inputval = ''.join(valsplit)

        valuesplit = inputval.split(';')
        valuesplit.pop(len(valuesplit)-1)
        for value in valuesplit:

            value = modinterpreter.trim(value)

            if value in aliases:
                value = aliases[value]

            commandSplit = value.split()

            if value in [None, '']:
                exitStatus = FURGENT+"idle"

            elif value == 'exit':
                sys.exit()

            elif value == "help":
                exitStatus = FSUCCESS+'0'
                Data = data.Help('')
                Data.showHelp()

            elif value == "list":
                exitStatus = FSUCCESS+'0'
                Mod.listmodules()

            elif value == "banner":
                modinterpreter.banner()

            elif modinterpreter.__returnval(commandSplit, 0) == 'clear':
                print(chr(27)+'2[j')
                print('\x33c')
                print('\x1bc')
                exitStatus = FSUCCESS+'0'
                if modinterpreter.__returnval(commandSplit, 1) in ['exit', 'terminate']:
                    sys.exit()

            elif modinterpreter.__returnval(commandSplit, 0) == 'use':
                if modinterpreter.__returnval(commandSplit, 1) in Module.moduleHelp.modules:
                    exitStatus = FSUCCESS+'0'
                    modinterpreter.interpreter(modinterpreter.__returnval(commandSplit, 1))
                elif not modinterpreter.__returnval(commandSplit, 1):
                    print(FALERT+'Error: no module specified')
                    exitStatus = FALERT+'1'
                else:
                    print(f'{FALERT}Error: Invalid module specified: \'{modinterpreter.__returnval(commandSplit, 1)}\'')
                    exitStatus = FALERT+'1'

            elif modinterpreter.__returnval(commandSplit, 0) == 'about':
                if modinterpreter.__returnval(commandSplit, 1):
                    mod = modinterpreter.__returnval(commandSplit, 1)
                    Module.moduleHelp(mod).aboutModule(mod)
                    exitStatus = FSUCCESS+'0'
                else :
                    print(FALERT+'Error: No module specified')
                    exitStatus = FALERT+'1'


            elif modinterpreter.__returnval(commandSplit, 0) == 'alias':
                try:
                    if not modinterpreter.__returnval(commandSplit, 1):
                        for x in aliases:
                            print(x,":",aliases[x])
                
                    else:
                        splitCommand = value.split('=')
                        assignedCommand = splitCommand[1]
                        if not assignedCommand or assignedCommand == '':
                            print(f'{FALERT}Error: please provide a command to alias')
                        else:
                            alias = splitCommand[0].split()[1]
                            print(alias, "=>",assignedCommand)
                            aliases[alias]=assignedCommand
        
                except Exception as e:
                    print(e)
                    pass

            elif modinterpreter.__returnval(commandSplit, 0) == 'unalias':
                if modinterpreter.__returnval(commandSplit, 1) and modinterpreter.__returnval(commandSplit, 1) in aliases:
                    del aliases[modinterpreter.__returnval(commandSplit, 1)]
                else:
                    print(f'{FALERT}[-] Error: no such alias \'{FURGENT}{modinterpreter.__returnval(commandSplit, 1)}{FALERT}\' exists')

            else:
                print(FALERT+'Error: Invalid Syntax')
                exitStatus = FALERT+'1'

except EOFError:
    print(FALERT+f'\nprobKit: exiting session')
