#! /usr/bin/env python3

# This is the data-information module which will print help for the interpreter and information about selected module

# This class prints help for the interpreter
class Help():
	def __init__(self, MODULE):
		self.module = MODULE

	def showHelp(self):
		module = self.module
		
		# Checks whether the shell is module interpreter or module selector session
		if module == '':
			print('\nUsage: [verb] [options]')
			print('Available verbs are: use, help, exit, terminate, clear\n')
			print('\t use\t\t specify a module to use\n\t\t\t usage: use [module]\n')
			print('\t help\t\t prints this help message\n')
			print('\tlist\t\t prints available modules')
			print('\tabout\t\t prints details about specified module\n\t\t\t Usage: about [moduleName]\n')
			print('\t exit\t\t exits the interpreter\n')
			print('\t terminate\t alias for exit\n')
			print('\t clear\t\t clears screen\n\t\t usage: clear [option]\n\t\t\tavailable options are: exit, terminate\n')

		else:
			print('\nUsage: [verb] [options]')
			print('Available verbs are: set, help, exit, back, info, options, clear, getstat, run\n')
			print('\t options\t lists available options to configure\n')
			print('\t info\t\t shows values assigned to each option\n')
			print('\t set\t\t assignes values to available options\n\t\t\t usage: set [option] [value]\n')
			print('\t help\t\t prints this help message\n')
			print('\t exit\t\t exits the whole interpreter\n')
			print('\t back\t\t moves back to the module selector\n')
			print('\t getstat\t prints the status of previous verb\n')
			print('\t clear\t\t clears screen\n')
			print('\t run\t\t runs the selected module\n')

# List available options for a selected module
class Options():
	def __init__(self, MODULE):
		self.module = MODULE

	def showOptions(self):
		module = self.module

		if module == 'probe':
			print(f'\n\tLHOST => hosts ip4 address(required)(LHOST => lhost)')
			print(f'\tLPORT => ports to scan on host(required)(LPORT => lport)')
			print(f'\tPROTO => protocol to use for scanning(required)(PROTO => protocol)')
			print(f'\tTMOUT => time to wait for incomming packet in seconds(set to \'1\' by default)(TMOUT => timeout)\n')

		else:
			raise Exception('Error: Invalid module')

# List values assigned to various options of the module
class Info():
	def __init__(self, MODULE, LHOST, LPORT, PROTOCOL, TIMEOUT):
		self.module  = MODULE
		self.lhost   = LHOST
		self.lport   = LPORT
		self.proto   = PROTOCOL
		self.timeout = TIMEOUT

	def showInfo(self):
		if self.module == 'probe':
			print(f'\n\tLHOST => {self.lhost}')
			print(f'\tLPORT => {self.lport}')
			print(f'\tPROTO => {self.proto}')
			print(f'\tTMOUT => {self.timeout}\n')

		else:
			raise Exception('Error: Invalid module')