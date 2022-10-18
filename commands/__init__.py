# from . import (
#     back, banner, clear, doc,
#     help, clear, set, run,
#     show, unset, use, directory, default_header,
#     cd
# )

from modules.util.CommandUtils.ReturnStructure import RetObject
from . import *
from abc import ABC, abstractmethod


class Runnable(ABC):
    __slots__ = 'args', 'retobj'

    def __init__(self, args: list[str], retobj: RetObject):
        self.args = args
        self.retobj = retobj

    @abstractmethod
    def run(self) -> RetObject: ...
