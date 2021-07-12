#! /usr/bin/env python3

# This session will be called by the actual interpreter(also known as module selector) to run modules

import sys
import modules.probe.ports as ports
import modules.data.OptInfHelp as data
import modules.data.AboutList as aboutList
import modules.probe.osprobe as osprobe
import readline
from config import colors, variables, aliases

FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FNORMAL = colors.FNORMAL
FURGENT = colors.FURGENT
FSTYLE = colors.FPROMPT

def trim(string):
    strsplit = string.split()
    return ' '.join(strsplit)

def banner():
    print('''
                          *               *    *          *
                          *               *   *     *     *
                          *               *  *            *
    * ***   * **   ****   * ***    ****   * *      **    ****
    **   *   *    *    *  **   *  *    *  **        *     *
    *    *   *    *    *  *    *  ******  * *       *     *
    **   *   *    *    *  *    *  *       *  *      *     *
    * ***    *    *    *  **   *  *    *  *   *     *     *  *
    *        *     ****   * ***    ****   *    *  *****    **
    *
    *

    -- by theEndurance-del
    ''')



# Calls the function based on the selected module
def __run(module, options):
    try:
        lhost    = options[0]
        lport    = options[1]
        protocol = options[2]
        timeout  = options[3]
        tryct    = options[4]
        nmap     = options[5]
        verbose  = options[6]
        try:
            if lhost == '':
                print(FALERT+'Error: Invalid value for LHOST')
            else:
                if module == 'probe':
                    if lport == '':
                        raise Exception(FALERT+'Error: value for LPORT')

                    ports.scanner(lhost, lport, timeout, protocol, tryct, verbose)

                elif module == 'osprobe':
                    osprobe.checkOS(lhost, tryct, nmap).scanner()

        except Exception as e:
            print(e)

    except KeyboardInterrupt as key:
        print(FALERT+'\nalert: KeyboardInterrupt detected\n')

# Just a simple function to return values in a list and raise exception 
# in such a way that the prog. doesn't break
def __returnval(value, pos):
    try:
        return value[int(pos)]
    except Exception as e:
        pass

# Module interpreter function called by the actual interpreter
def interpreter(MODULE):

    # Variables also known as options to the user
    OPTIONS = [variables.LHOST
    , variables.LPORT
    , variables.PROTOCOL
    , variables.TIMEOUT
    , variables.TRYCT
    , variables.NMAP
    , variables.VERBOSE
    ]
    exitStatus = 0

    try:
        while (True):

            if MODULE == '':
                break
            elif MODULE == 'test':
                inputval = input(FALERT+f'probeKit:[*{MODULE}*] $> '+FNORMAL)
            else:
                inputval = input(FNORMAL+'probeKit:'+FSTYLE+f'[{MODULE}]'+FSUCCESS+' $> '+FNORMAL)
    
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
            for commands in valuesplit:

                commands = trim(commands)

                if commands in aliases:
                    commands = aliases[commands]
                    print(commands)
            
                if commands != None or commands != '':
                    cmdSplit = commands.split()
                    verb = __returnval(cmdSplit, 0)

                if commands == None or commands == '':
                    exitStatus = 'idle'

                elif commands == "banner":
                    banner()

                elif verb == 'help':
                    Data = data.Help(MODULE)
                    Data.showHelp()

                elif verb == 'list':
                    aboutList.moduleHelp(MODULE).listmodules()

                elif verb == 'show':
                    if __returnval(cmdSplit, 1):
                        if __returnval(cmdSplit, 1) == 'info':
                            Info = data.Info(MODULE, OPTIONS)
                            try:
                                Info.showInfo()
                            except Exception as e:
                                print(e)

                            exitStatus = 0

                        elif __returnval(cmdSplit, 1) == 'options':
                            Option = data.Options(MODULE)
                            try:
                                Option.showOptions()
                            except Exception as e:
                                print(e)

                        elif __returnval(cmdSplit, 1) == 'status':
                            print(exitStatus)
                            exitStatus = 0

                        else:
                            print(f'{FALERT}[-] Error: Invalid argument provided')
                            exitStatus = 1
                    else:
                        print(f'{FALERT}[-] Error: no argument provided')
                        exitStatus = 1

                elif verb == 'back':
                    MODULE = ''

                elif verb == 'exit':
                    sys.exit(0)

                elif verb == 'clear':
                    print(chr(27)+'2[j')
                    print('\033c')
                    print('\x1bc')
                    exitStatus = 0

                elif verb == 'run':
                    try:
                        __run(MODULE, OPTIONS)
                    except Exception as e:
                        print(e)

                # Verb(or command) to set options
                elif verb == 'set':
                    if __returnval(cmdSplit, 2) and __returnval(cmdSplit, 1) != 'all':
                        if __returnval(cmdSplit, 1) in ['LHOST', 'lhost']:
                            print(f'LHOST => {__returnval(cmdSplit, 2)}')
                            OPTIONS[0] = __returnval(cmdSplit, 2)

                        elif __returnval(cmdSplit, 1) in ['LPORT', 'lport']:
                            if '/' in __returnval(cmdSplit, 2):
                                OPTIONS[1] = __returnval(cmdSplit, 2).split('/')
                                print(f'LPORT => {OPTIONS[1]}')

                            else:
                                print(f'LPORT => {__returnval(cmdSplit, 2)}')
                                OPTIONS[1] = __returnval(cmdSplit, 2)

                        elif __returnval(cmdSplit, 1) in ['PROTO', 'proto']:
                            print(f'PROTO => {__returnval(cmdSplit, 2)}')
                            OPTIONS[2] = __returnval(cmdSplit, 2)

                        elif __returnval(cmdSplit ,1) in ['TMOUT', 'tmout']:
                            print(f'TMOUT => {__returnval(cmdSplit, 2)}')
                            OPTIONS[3] = __returnval(cmdSplit, 2)

                        elif __returnval(cmdSplit, 1) in ['TRYCT', 'tryct']:
                            print(f'TRYCT => {__returnval(cmdSplit, 2)}')
                            OPTIONS[4] = int(__returnval(cmdSplit, 2))

                        elif __returnval(cmdSplit, 1) in ['NMAP', 'nmap']:
                            print(f'NMAP  => {__returnval(cmdSplit, 2)}')
                            OPTIONS[5] = int(__returnval(cmdSplit, 2))

                        elif __returnval(cmdSplit, 1) in ['VERBOSE', 'verbose']:
                            if __returnval(cmdSplit, 2) not in ['true', 'false']:
                                print(FALERT+'Error: Invalid value provided')
                            elif __returnval(cmdSplit, 2) == 'true':
                                OPTIONS[6] = True
                                print(f'VERBOSE => {OPTIONS[6]}')
                            elif __returnval(cmdSplit, 2) == 'false':
                                OPTIONS[6] = False
                                print(f'VERBOSE => {OPTIONS[6]}')

                        else:
                            print(FALERT+'[-] Error: Invalid option')

                    elif __returnval(cmdSplit, 1) == 'all':
                        OPTIONS[0] = variables.LHOST
                        OPTIONS[1] = variables.LPORT
                        OPTIONS[2] = variables.PROTOCOL
                        OPTIONS[3] = variables.TIMEOUT
                        OPTIONS[4] = variables.TRYCT
                        OPTIONS[5] = variables.NMAP
                        OPTIONS[6] = variables.VERBOSE

                    elif not __returnval(cmdSplit, 2):
                        print(f'{FALERT}[-] Error: no value provided to option')

                    else:
                        print(f"{FALERT}[-] Error: Invalid value provided to option")

                # Verb(or command) to unset options
                elif verb == 'unset':
                    if __returnval(cmdSplit, 1) in ['LHOST', 'lhost']:
                        print(f'{FALERT}unset LHOST')
                        OPTIONS[0] = ''

                    elif __returnval(cmdSplit, 1) in ['LPORT', 'lport']:
                        print(f'{FALERT}unset LPORT')
                        OPTIONS[1] = ''

                    elif __returnval(cmdSplit, 1) in ['PROTO', 'proto']:
                        print(f'{FALERT}unset PROTO')
                        OPTIONS[2] = ''

                    elif __returnval(cmdSplit, 1) in ['TMOUT', 'tmout']:
                        print(f'{FALERT}unset TMOUT')
                        OPTIONS[3] = '1'

                    elif __returnval(cmdSplit, 1) in ['TRYCT', 'tryct']:
                        print(f'{FALERT}unset TRYCT')
                        OPTIONS[4] = 1

                    elif __returnval(cmdSplit, 1) in ['NMAP', 'nmap']:
                        print(f'{FALERT}unset NMAP')
                        OPTIONS[5] = 0

                    elif __returnval(cmdSplit, 2) in ['VERBOSE', 'verbose']:
                        print(f'{FALERT}unset VERBOSE')
                        OPTIONS[6] = ''

                    elif __returnval(cmdSplit, 1) == 'all':
                        OPTIONS[0] = ''
                        OPTIONS[1] = ''
                        OPTIONS[2] = ''
                        OPTIONS[3] = 1
                        OPTIONS[4] = 1
                        OPTIONS[5] = 0
                        OPTIONS[6] = ''
                    else:
                        print(FALERT+'Error: Invalid option')

                elif verb == 'use':
                    if __returnval(cmdSplit, 1):
                        if __returnval(cmdSplit, 1) in aboutList.moduleHelp.modules:
                            MODULE = __returnval(cmdSplit, 1)
                            print(FURGENT+f'MODULE => {MODULE}')
                        else:
                            print(f'{FALERT}Error: Invalid module specified: \'{__returnval(cmdSplit, 1)}\'')
                    else:
                        print(FALERT+'Error: No module specified')

                elif verb == 'about':
                    if __returnval(cmdSplit, 1):
                        mod = __returnval(cmdSplit, 1)
                        aboutList.moduleHelp(mod).aboutModule(mod)
                    else:
                        aboutList.moduleHelp(MODULE).aboutModule(MODULE)

                elif verb == 'alias':
                    try:
                        if not __returnval(cmdSplit, 1):
                            for x in aliases:
                                print(x,":",aliases[x])
                
                        else:
                            splitCommand = commands.split('=')
                            assignedCommand = splitCommand[1]
                            alias = splitCommand[0].split()[1]
                            if not assignedCommand or assignedCommand == '':
                                print(f'{FALERT}[-] Error: please provide a command to alias')
                            else:
                                print(alias, "=>",assignedCommand)
                                aliases[alias]=assignedCommand

                    except Exception as e:
                        print(e)
                        pass

                elif verb == 'unalias':
                    if __returnval(cmdSplit, 1) and __returnval(cmdSplit, 1) in aliases:
                        del aliases[__returnval(cmdSplit, 1)]
                    else:
                        print(f'{FALERT}[-] Error: no such alias \'{FURGENT}{__returnval(cmdSplit, 1)}{FALERT}\' exists')

                else:
                    print(FALERT+'Error: Invalid syntax'+FNORMAL)

    except EOFError as E:
        sys.exit()

    except Exception as e:
        print(e)