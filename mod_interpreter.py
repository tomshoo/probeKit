#! /usr/bin/env python3

# This session will be called by the actual interpreter(also known as module selector) to run modules

import sys
import modules.probe.ports as ports
import modules.data.OptInfHelp as data

# Calls the function based on the selected module
def __run(lhost, lport, timeout, protocol, module):
	if lhost == '' or lport == '':
		raise Exception('Error: invalid arguments provided')
	try:
		if module == 'probe':
			ports.scanner(lhost, lport, timeout, protocol)
	except Exception as e:
		print(e)

# Just a simple function to return values in a list and raise exception in such a way that the prog. doesn't break
def __returnval(value, pos):
	try:
		return value[int(pos)]
	except Exception as e:
		print(e)

oneliners = ['info', 'options', 'exit', 'back', 'help', None, '', 'clear', 'getstat', 'run']

# Module interpreter function called by the actual interpreter
def interpreter(MODULE):

	# Variables also known as options to the user
	LHOST = ''
	LPORT = ''
	PROTOCOL = ''
	TIMEOUT = '1'
	exitStatus = 0

	try:
		while (True):

			commands = input(f'probeKit:[{MODULE}] $> ')

			if commands == None or commands == '':
				exitStatus = 'idle'

			if commands == 'help':
				Data = data.Help(MODULE)
				Data.showHelp()

			if commands == 'options':
				Option = data.Options(MODULE)
				try:
					Option.showOptions()
				except Exception as e:
					print(e)

				exitStatus = 0

			if commands == 'info':
				Info = data.Info(MODULE, LHOST, LPORT, PROTOCOL,TIMEOUT)
				try:
					Info.showInfo()
				except Exception as e:
					print(e)
				
				exitStatus = 0

			if commands == 'back':
				break

			if commands == 'exit':
				sys.exit()

			if commands == 'clear':
				print(chr(27)+'2[j')
				print('\033c')
				print('\x1bc')
				exitStatus = 0

			if commands == 'getstat':
				print(f'status: {exitStatus}')

			if commands == 'run':
				try:
					__run(LHOST, LPORT, TIMEOUT, PROTOCOL, MODULE)
				except Exception as e:
					print(e)

			if commands not in oneliners:
				cmdSplit = commands.split()
				verb = cmdSplit[0]

				# Verb(or command) to set options
				if verb == 'set':
					if __returnval(cmdSplit, 1) == 'LHOST' or __returnval(cmdSplit, 1) == 'lhost':
						LHOST = __returnval(cmdSplit, 2)

					elif __returnval(cmdSplit, 1) == 'LPORT' or __returnval(cmdSplit, 1) == 'lport':
						if '/' in __returnval(cmdSplit, 2):
							LPORT = __returnval(cmdSplit, 2).split('/')
						
						else:
							LPORT = __returnval(cmdSplit, 2)

					elif __returnval(cmdSplit, 1) == 'PROTO' or __returnval(cmdSplit, 1) == 'protocol':
						PROTOCOL = __returnval(cmdSplit, 2)

					elif __returnval(cmdSplit ,1) == 'TMOUT' or __returnval(cmdSplit, 1) == 'timeout':
						TIMEOUT = __returnval(cmdSplit, 2)

					else:
						print('Error: Invalid option')

				# Verb(or command) to unset options
				if verb == 'unset':
					if __returnval(cmdSplit, 1) == 'LHOST' or __returnval(cmdSplit, 1) == 'lhost':
						LHOST = ''

					elif __returnval(cmdSplit, 1) == 'LPORT' or __returnval(cmdSplit, 1) == 'lport':
						LPORT = ''

					elif __returnval(cmdSplit, 1) == 'PROTO' or __returnval(cmdSplit, 1) == 'protocol':
						PROTOCOL = ''

					elif __returnval(cmdSplit, 1) == 'TMOUT' or __returnval(cmdSplit, 1) == 'timeout':
						TIMEOUT = '1'

					elif __returnval(cmdSplit, 1) == 'all':
						LHOST = ''
						LPORT = ''
						PROTOCOL = ''
						TIMEOUT = '1'

					else:
						print('Error: Invalid option')

	except Exception as e:
		print(e)
		sys.exit()