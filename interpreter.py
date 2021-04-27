#! /usr/bin/env python3

# This is a module selector and doesn't use many commands as it is used to only select module

import sys
import mod_interpreter as modinterpreter
import modules.data.OptInfHelp as data

oneliners = ["help", "exit", "terminate", None, '']
exitStatus = 0

# All available module
MODULE = ['probe']

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

		if value not in oneliners:
			commandSplit = value.split()
			if commandSplit[0] == "clear":
				print(chr(27)+'2[j')
				print('\033c')
				print('\x1bc')
				exitStatus = 0
				def termFunc():
					try:
						if commandSplit[1] == "exit" or commandSplit[1] == "terminate": return True
						else:
							print('Error: Unknown Syntax')
							return False
					except:
						return False

				if termFunc(): sys.exit()

			elif commandSplit[0] == "use":
				try:
					if commandSplit[1] in MODULE:

						# Call the module interpreter session
						modinterpreter.interpreter(str(commandSplit[1]))

					else:
						print('Error: Unknown Module')
				except Exception as e:
					print(e)

			else:
				print('Error: Invalid Syntax')

except:
	print(f'\nprobKit: exit status: {exitStatus}')
