# probeKit
A simple tool written in Python for basic reconnaissance

# Requirements:

Python: `3.x`, Python `3.x` compatible pip, nmap, python-scapy, python-nmap, readline

OS: Unix based operating system(macOS, Linux, etc.)

Not supported on DOS based platforms.

# Installation
This toolkit does not require any extra configurations as it is a basic plug'n'play toolkit.

## Debian/Ubuntu ##

``` bash
sudo apt install nmap
git clone https://github.com/theEndurance-del/probeKit.git
pip install -r requirements.txt
```

## ArchLinux ##

``` bash
sudo pacman -Sy nmap
git clone https://github.com/theEndurance-del/probeKit.git
pip install -r requirements.txt
```

# Customization

This toolkit has it's own default set of colors.

```
red => Alerts or critical points
yellow => warnings or significant changes
green => successfull result or helpful text
blue => default prompt color
```

Also there is an option to provide default values to options.

Please edit `config.py` file to change color settings or option settings.

# Usage:
Start the interpreter by typing the following in your terminal:
`python3 ./probeKit/interpreter.py`

To use a module simply type:
`use [module]`

Once into the module's interpreter the shell will display the module's name.

To know about the options available with the module simply type `options` in the interpreter shell.

To know about the configured options for a module or to check assigned values to available options type `info` in the interpreter

To assign value to an available option:
`set [OPTION] [VALUE]`

To run the module simply type `run`

*Note: This project is still not completed as a whole and still requires a lot of rewriting any suggestions for improvement are kindly accepted but may require some time to be worked upon*

## Thank You!! ##
