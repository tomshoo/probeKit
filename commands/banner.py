import pyfiglet
from random import randint
from modules.util.ReturnStructure import RetObject

def run(_arguments: list[str], ReturnObject: RetObject) -> RetObject:
    """Function to print the introductory banner"""
    paint()
    ReturnObject.exit_code = 0
    return RetObject()

def paint():
    fontlist: list = pyfiglet.FigletFont().getFonts()
    maxind: int = len(fontlist)-1
    fontstyle: str = fontlist[randint(0, maxind)]
    print(f'Using figletFont {fontstyle}')
    fig = pyfiglet.Figlet(font=fontstyle)
    print(fig.renderText('PROBEKIT ~~'))
    fontlist.clear()

    print('-- by theEndurance-del')