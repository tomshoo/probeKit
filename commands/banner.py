import pyfiglet
from random import randint
from modules.util.CommandUtils.ReturnStructure import RetObject

from . import Runnable


class Banner(Runnable):
    def run(self) -> RetObject:
        """Function to print the introductory banner"""
        paint()
        self.retobj.exit_code = 0
        return RetObject()


def paint():
    fontlist: list = pyfiglet.FigletFont().getFonts()
    maxind: int = len(fontlist)-1
    fontstyle: str = fontlist[randint(0, maxind)]
    print(f'Using figletFont {fontstyle}')
    fig = pyfiglet.Figlet(font=fontstyle)
    print(fig.renderText('PROBEKIT ~~'))
    fontlist.clear()

    print('-- by tomshoo')
