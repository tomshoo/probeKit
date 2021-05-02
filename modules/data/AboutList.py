#! /usr/bin/env python3

from colorama import Fore

FGREEN = Fore.GREEN
FRED = Fore.RED
FWHITE = Fore.WHITE

class moduleHelp():

	modules = ['probe', 'test']

	def __init__(self, MODULE):
		self.module = MODULE

	def listmodules(self):
		if self.module != '':
			print('Currently activated module: '+FRED+f'[{self.module}]')

		print(FWHITE+'Available modules are:')
		for x in self.modules:
			print(FGREEN+"\t", x)

		print(FWHITE+'type: about [Module] for more information')

	def aboutModule(self, moduleName):
		if moduleName == 'probe':
			print(FRED+f'\nName:\t\t{moduleName}')
			print('Type:\t\tRecon')
			print('Description:\tThis module is meant to perform a basic port scan on the specidied host.\n')
			print(FGREEN+'Available options:\n')
			print('\tLHOST => IPv4 address or domain name of the target host')
			print('\t\t | Can be called LHOST or lhost\n')
			print('\tLPORT => ports to be scanned')
			print('\t\t | Can be called LPORT or lport')
			print('\t\t | Specify single port as `set lport [portnumber]`')
			print('\t\t | or set multiple ports by `set lport [startPort]/[endPort]`\n')
			print('\tTMOUT => timeout duration while awaiting connection')
			print('\t\t | Can be called TMOUT or tmout')
			print('\t\t | Defaults to 1 second duration\n')

		if moduleName == 'test':
			print(FRED+'This module is strictly for debugging purposes while creating the toolkit')
			print(FRED+'Do not consider this as a usable module')