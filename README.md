# probeKit

A simple tool written in Python for basic reconnaissance

## Requirements

Python: `3.x`, Python `3.x` compatible pip, nmap, python-scapy, python-nmap, readline

OS: Unix based operating system(macOS, Linux, etc.)
 *note: the history feature would not work as expected on macOS*

Not supported on DOS based platforms.

## Installation

### Debian/Ubuntu

``` bash
git clone https://theEndurance-del/probeKit.git && cd ./probeKit
sudo apt install nmap python-pip python3-wheel python3-dev
pip install scapy python-nmap
```

### Arch based distributions

``` bash
git clone https://theEndurance-del/probeKit.git && cd ./probeKit
sudo pacman -Syu nmap python-pip
pip install scapy python-nmap
```

## Usage

Start the interpreter by typing the following in your terminal:
`python3 ./probeKit/interpreter.py`

Show help by using the `help` command.

This is the help shown:

``` text

Usage: [verb] [options]
Available verbs are: set, help, exit, back, clear, run

    show        shows information on provided argument(*)

    set         assignes values to available options(*)

    help        prints this help message

    exit        exits the whole interpreter

    back        moves back to the module selector

    clear       clears screen

    run         runs the selected module

    about       prints details about specified module(*)

    list        prints available modules

    banner      prints an ascii banner

    alias       set an alias for a command(*)

    unalias     unset a pre-existing alias(*)

```

Run `help [command]` for more information(only the commands marked with `(*)` have a seperate help)

## Customization

This toolkit has it's own default set of colors.

``` text
red => Alerts or critical points
yellow => warnings or significant changes
green => successfull result or helpful text
blue => default prompt color
```

Also there is an option to provide default values to options.

Please edit `config.py` file to change color settings or option settings.
 *If your terminal has a light background then please change `FNORMAL = Fore.WHITE` to `FNORMAL = Fore.BLACK` in `config.py` to provide more visibility*

## Note

This project is still not completed as a whole and still requires a lot of rewriting any suggestions for improvement are kindly accepted but may require some time to be worked upon

## Thank You
