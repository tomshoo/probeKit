import pyfiglet
from random import randint

def run() -> int:
    """Function to print the introductory banner"""
    fontlist: list = pyfiglet.FigletFont().getFonts()
    maxind: int = len(fontlist)
    fontstyle: str = fontlist[randint(0, maxind)]
    print(f'Using figletFont {fontstyle}')
    fig = pyfiglet.Figlet(font=fontstyle)
    print(fig.renderText('PROBEKIT ~~'))
    fontlist.clear()

    print('-- by theEndurance-del')

    return 0