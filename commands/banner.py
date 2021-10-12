import pyfiglet
from random import randint

def run():
    """Function to print the introductory banner"""
    fontstyle: str = pyfiglet.FigletFont.getFonts()[randint(0,425)]
    print(f'Using figletFont {fontstyle}')
    fig = pyfiglet.Figlet(font=fontstyle)
    print(fig.renderText('PROBEKIT ~~'))

    print('-- by theEndurance-del')

    return 0