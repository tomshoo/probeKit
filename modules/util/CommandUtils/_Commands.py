# from commands import (
#     run, banner, clear, show,
#     doc, set, unset, use,
#     help, back
# )

from platform import platform

from commands import *
from config import default_command_header

# import commands
Commands: dict = {
    # Command Name                     |Function or Object Name
    #==========================================================
    f'{default_command_header}.run':    run.run,
    f'{default_command_header}.banner': banner.run,
    f'{default_command_header}.clear': clear.run,
    f'{default_command_header}.show': show.run,
    f'{default_command_header}.doc': doc.Docs,
    f'{default_command_header}.set': set.Set,
    f'{default_command_header}.unset': unset.unset_val,
    f'{default_command_header}.use': use.use,
    f'{default_command_header}.help': help.run,
    f'{default_command_header}.back': back.run,
    f'{default_command_header}': default_header.run,
    f'{default_command_header}.cd':  cd.run
}

if 'Windows' in platform():
    Commands['dir'] = directory.run
