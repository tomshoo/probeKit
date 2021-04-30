#! /usr/bin/env python3

class moduleHelp():

	modules = ['probe']

	def __init__(self, MODULE):
		self.module = MODULE

	def listmodules(self):
		if self.module != '':
			print(f'Currently activated module: [{self.module}]')

		print('Available modules are:')
		for x in modules:
			print("\t", x)

		print('type: about [Module] for more information')

	def aboutModule(self, moduleName):
		if moduleName == 'probe':
			print(f'\nName:\t\t{moduleName}')
			print('Type:\t\tRecon')
			print('Description:\tThis module is meant to perform a basic port scan on the specidied host.\n')
			print('Available options:\n')
			print('\tLHOST => IPv4 address or domain name of the target host')
			print('\t\t Can be called LHOST or lhost\n')
			print('\tLPORT => ports to be scanned')
			print('\t\t Can be called LPORT or lport')
			print('\t\t Specify single port as `set lport [portnumber]`')
			print('\t\t or set multiple ports by `set lport [startPort]/[endPort]`\n')
			print('\tTMOUT => timeout duration while awaiting connection')
			print('\t\t Can be called TMOUT or timeout')
			print('\t\t Defaults to 1 second duration\n')