#! /usr/bin/env python3

# This session will be called by the actual interpreter(also known as module selector) to run modules

import sys
import modules.probe.ports as ports
import modules.data.OptInfHelp as data
import modules.data.AboutList as aboutList
import modules.probe.osprobe as osprobe
import colors as color

FSUCCESS = color.FSUCCESS
FALERT = color.FALERT
FNORMAL = color.FNORMAL
FURGENT = color.FURGENT
FSTYLE = color.FPROMPT

# Calls the function based on the selected module
def __run(lhost, lport, timeout, tryct, nmap, protocol, module):
	try:
		try:
			if lhost == '':
				print(FALERT+'Error: Invalid value for LHOST')
			else:
				if module == 'probe':
					if lport == '':
						raise Exception(FALERT+'Error: value for LPORT')
				
					ports.scanner(lhost, lport, timeout, protocol, tryct)
		
				elif module == 'osprobe':
					osprobe.checkOS(lhost, tryct, nmap).scanner()

		except Exception as e:
			print(e)

	except KeyboardInterrupt as key:
		print(FALERT+'\nalert: KeyboardInterrupt detected\n')

# Just a simple function to return values in a list and raise exception in such a way that the prog. doesn't break
def __returnval(value, pos):
	try:
		return value[int(pos)]
	except Exception as e:
		pass

# Module interpreter function called by the actual interpreter
def interpreter(MODULE):

	# Variables also known as options to the user
	LHOST = ''
	LPORT = ''
	PROTOCOL = ''
	TIMEOUT = '1'
	TRYCT = 1
	NMAP = 0
	exitStatus = 0

	try:
		while (True):

			if MODULE == 'test':
				commands = input(FALERT+f'probeKit:[*{MODULE}*] $> '+FNORMAL)
			else:
				commands = input(FNORMAL+'probeKit:'+FSTYLE+f'[{MODULE}]'+FSUCCESS+' $> '+FWHITE)

			if commands != None or commands != '':
				cmdSplit = commands.split()
				verb = __returnval(cmdSplit, 0)

			if commands == None or commands == '':
				exitStatus = 'idle'

			elif verb == 'help':
				Data = data.Help(MODULE)
				Data.showHelp()

			elif verb == 'options':
				Option = data.Options(MODULE)
				try:
					Option.showOptions()
				except Exception as e:
					print(e)

				exitStatus = 0

			elif verb == 'info':
				Info = data.Info(MODULE, LHOST, LPORT, PROTOCOL, TIMEOUT, TRYCT, NMAP)
				try:
					Info.showInfo()
				except Exception as e:
					print(e)
				
				exitStatus = 0

			elif verb == 'list':
				aboutList.moduleHelp(MODULE).listmodules()

			elif verb == 'back':
				break

			elif verb == 'exit':
				sys.exit(0)

			elif verb == 'clear':
				print(chr(27)+'2[j')
				print('\033c')
				print('\x1bc')
				exitStatus = 0

			elif verb == 'getstat':
				print('status: '+FSUCCESS+f'{exitStatus}')

			elif verb == 'run':
				try:
					__run(LHOST, LPORT, TIMEOUT, TRYCT, NMAP, PROTOCOL, MODULE)
				except Exception as e:
					print(e)


			# Verb(or command) to set options
			elif verb == 'set':
				if __returnval(cmdSplit, 1) == 'LHOST' or __returnval(cmdSplit, 1) == 'lhost':
					print(f'LHOST => {__returnval(cmdSplit, 2)}')
					LHOST = __returnval(cmdSplit, 2)

				elif __returnval(cmdSplit, 1) == 'LPORT' or __returnval(cmdSplit, 1) == 'lport':
					if '/' in __returnval(cmdSplit, 2):
						LPORT = __returnval(cmdSplit, 2).split('/')
						print(f'LPORT => {LPORT}')
						
					else:
						print(f'LPORT => {__returnval(cmdSplit, 2)}')
						LPORT = __returnval(cmdSplit, 2)

				elif __returnval(cmdSplit, 1) == 'PROTO' or __returnval(cmdSplit, 1) == 'proto':
					print(f'PROTO => {__returnval(cmdSplit, 2)}')
					PROTOCOL = __returnval(cmdSplit, 2)

				elif __returnval(cmdSplit ,1) == 'TMOUT' or __returnval(cmdSplit, 1) == 'tmout':
					print(f'TMOUT => {__returnval(cmdSplit, 2)}')
					TIMEOUT = __returnval(cmdSplit, 2)

				elif __returnval(cmdSplit, 1) == 'TRYCT' or __returnval(cmdSplit, 1) == 'tryct':
					print(f'TRYCT => {__returnval(cmdSplit, 2)}')
					TRYCT = int(__returnval(cmdSplit, 2))

				elif __returnval(cmdSplit, 1) == 'NMAP' or __returnval(cmdSplit, 1) == 'nmap':
					print(f'NMAP  => {__returnval(cmdSplit, 2)}')
					NMAP = int(__returnval(cmdSplit, 2))

				else:
					print(FALERT+'Error: Invalid option')

			# Verb(or command) to unset options
			elif verb == 'unset':
				if __returnval(cmdSplit, 1) == 'LHOST' or __returnval(cmdSplit, 1) == 'lhost':
					LHOST = ''

				elif __returnval(cmdSplit, 1) == 'LPORT' or __returnval(cmdSplit, 1) == 'lport':
					LPORT = ''

				elif __returnval(cmdSplit, 1) == 'PROTO' or __returnval(cmdSplit, 1) == 'proto':
					PROTOCOL = ''

				elif __returnval(cmdSplit, 1) == 'TMOUT' or __returnval(cmdSplit, 1) == 'tmout':
					TIMEOUT = '1'

				elif __returnval(cmdSplit, 1) == 'TRYCT' or __returnval(cmdSplit, 1) == 'tryct':
					TRYCT = 1
				elif __returnval(cmdSplit, 1) == 'NMAP' or __returnval(cmdSplit, 1) == 'nmap':
					NMAP = 0

				elif __returnval(cmdSplit, 1) == 'all':
					LHOST = ''
					LPORT = ''
					PROTOCOL = ''
					TRYCT = 1
					NMAP = 0
					TIMEOUT = '1'

				else:
					print(FALERT+'Error: Invalid option')

			elif verb == 'use':
				if __returnval(cmdSplit, 1):
					if __returnval(cmdSplit, 1) in aboutList.moduleHelp.modules:
						MODULE = __returnval(cmdSplit, 1)
						print(FURGENT+f'MODULE => {MODULE}')
					else:
						print(FALERT+"Error: Invalid Module")
				else:
					print(FALERT+'Error: No module specified')

			elif verb == 'about':
				if __returnval(cmdSplit, 1):
					mod = __returnval(cmdSplit, 1)
					aboutList.moduleHelp(mod).aboutModule(mod)
				else:
					aboutList.moduleHelp(MODULE).aboutModule(MODULE)

			else:
				print(FALERT+'Error: Invalid syntax'+FNORMAL)

	except Exception as e:
		print(e)
		sys.exit()
