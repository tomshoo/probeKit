# probeKit

A simple tool written in Python for basic reconnaissance

## Requirements

Python: `3.6>=x<10`, Python `3.6>=x<10` compatible pip, nmap, python-scapy, python-nmap, readline

OS: Unix based operating system(macOS, Linux, etc.), Windows 10.

- note: install [npcap](https://nmap.org/npcap/#download) before using this tool on Windows
    - Also powershell commands feature would not work in windows

---

## Installation

### Debian/Ubuntu

``` bash
git clone https://github.com/theEndurance-del/probeKit.git && cd ./probeKit
sudo apt install nmap python-pip python3-wheel python3-dev
pip install -r requirements.txt
```

### Arch based distributions

``` bash
git clone https://github.com/theEndurance-del/probeKit.git && cd ./probeKit
sudo pacman -Syu nmap python-pip
pip install -r requirements.txt
```
 *Note: If possible try installing the dependencies listed in `requirements.txt` via `pacman`, since installing it via pip might break future pacman installations.*

---

###  Windows 10/11

- Install `nmap` and `npcap` from the [official](https://nmap.org/download.html) website.
- Install `python3.6>=x<10` from python's [official](https://www.python.org/downloads/) or from Micrsoft store.
- Then copy and paste the following commands in windows powershell,

``` pwsh
git clone https://github.com/theEndurance-del/probeKit.git
set-location .\probeKit\
python -m pip install -r .\requirements.txt
```
---

## Usage

Start the interpreter by typing the following in your terminal:
`python3 ./probeKit/interpreter.py`

Show help by using the `help` command.

This is the help shown:

``` text

Usage: [verb] [options]
Available verbs are: set, help, exit, back, clear, run

    use         use an available module(*)
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

---

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

The config also provides a `powershell` and a `nonpowershell` theme (use the powershell theme if using `windows powershell`, not required in windows 11).