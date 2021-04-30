#! /usr/bin/env python3

# This is a module selector and doesn't use many commands as it is used to only select module

import sys
import mod_interpreter as modinterpreter
import modules.data.OptInfHelp as data
import modules.data.AboutList as Module

def __returnval(value, pos):
	try:
		return value[int(pos)]
	except Exception as e:
		pass

Module = Module.moduleHelp('')

oneliners = ["help", "exit", "terminate", None, '', "list"]
exitStatus = 0

try:
	while(True):
		value = input(f'[probkit]: {exitStatus}$> ')

		if value == None or value == '':
			exitStatus = "idle"

		if value == "exit" or value == "terminate":
			sys.exit()

		if value == "help":
			Data = data.Help('')
			Data.showHelp()

		if value == "list":
			Module.listmodules()

		if value not in oneliners:
			commandSplit = value.split()

			if __returnval(commandSplit, 0) == 'clear':
				print(chr(27)+'2[j')
				print('\x33c')
				print('\x1bc')
				if __returnval(commandSplit, 1) == 'exit' or __returnval(commandSplit, 1) == 'terminate':
					sys.exit()

			elif __returnval(commandSplit, 0) == 'use':
				if __returnval(commandSplit, 1) in Module.modules:
					modinterpreter.interpreter(__returnval(commandSplit, 1))

			elif __returnval(commandSplit, 0) == 'about':
				if __returnval(commandSplit, 1):
					Module.aboutModule(__returnval(commandSplit, 1))
				else :
					print('Error: No module specified')
					exitStatus = 1

			else:
				print('Error: Invalid Syntax')

except:
	print(f'\nprobKit: exit status: {exitStatus}')
