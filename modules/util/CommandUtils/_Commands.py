#fmt: off
from commands import (Runnable, run, banner, clear, show, doc, set,
                      unset, use, help, back, directory, default_header, cd)
from typing import Type
from config import default_command_header

from platform import platform

# from commands import *

Commands: dict[str, Type[Runnable]] = {
    # Command Name                     | Function or Object Name
    # ==========================================================
    f'{default_command_header}.run'    : run.RunModule,
    f'{default_command_header}.banner' : banner.Banner,
    f'{default_command_header}.clear'  : clear.ClearScreen,
    f'{default_command_header}.show'   : show.ShowVars,
    f'{default_command_header}.doc'    : doc.Docs,
    f'{default_command_header}.set'    : set.Set,
    f'{default_command_header}.unset'  : unset.Unset,
    f'{default_command_header}.use'    : use.UseModule,
    f'{default_command_header}.help'   : help.Help,
    f'{default_command_header}.back'   : back.MoveBack,
    f'{default_command_header}'        : default_header.Default,
    f'{default_command_header}.cd'     : cd.ChangeDir
}

if 'Windows' in platform():
    Commands['dir'] = directory.ChangeDirWin
