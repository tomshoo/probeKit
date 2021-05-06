#! /usr/bin/env python3

# This is a module selector and doesn't use many commands as it is used to only select module

import sys
from colorama import Fore, Back, init
import mod_interpreter as modinterpreter
import modules.data.OptInfHelp as data
import modules.data.AboutList as Module

FGREEN = Fore.GREEN
FRED = Fore.RED
FWHITE = Fore.WHITE
FYELLOW = Fore.YELLOW

def __returnval(value, pos):
	try:
		return value[int(pos)]
	except Exception as e:
		pass

Module = Module.moduleHelp('')

exitStatus = FGREEN+'0'

try:
	while(True):
		value = input(FWHITE+'[probkit]:'+f' {exitStatus}'+FWHITE+'$> ')

		commandSplit = value.split()

		if value == None or value == '':
			exitStatus = FYELLOW+"idle"

		elif value == "exit" or value == "terminate":
			sys.exit()

		elif value == "help":
			exitStatus = FGREEN+'0'
			Data = data.Help('')
			Data.showHelp()

		elif value == "list":
			exitStatus = FGREEN+'0'
			Module.listmodules()

		elif __returnval(commandSplit, 0) == 'clear':
			print(chr(27)+'2[j')
			print('\x33c')
			print('\x1bc')
			exitStatus = FGREEN+'0'
			if __returnval(commandSplit, 1) == 'exit' or __returnval(commandSplit, 1) == 'terminate':
				sys.exit()

		elif __returnval(commandSplit, 0) == 'use':
			if __returnval(commandSplit, 1) in Module.modules:
				exitStatus = FGREEN+'0'
				modinterpreter.interpreter(__returnval(commandSplit, 1))
			elif not __returnval(commandSplit, 1):
				print(FRED+'Error: Invalid no module specified')
				exitStatus = FRED+'1'
			else:
				print(FRED+'Error: Invalid module specified')
				exitStatus = FRED+'1'

		elif __returnval(commandSplit, 0) == 'about':
			if __returnval(commandSplit, 1):
				Module.aboutModule(__returnval(commandSplit, 1))
				exitStatus = FGREEN+'0'
			else :
				print(FRED+'Error: No module specified')
				exitStatus = FRED+'1'

		else:
			print(FRED+'Error: Invalid Syntax')
			exitStatus = FRED+'1'

except:
	print(FRED+f'\nprobKit: exiting session')