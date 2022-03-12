# The `show` command

The `command` provides the user with the ability to lookup some important information on `module`, `aliase`, etc...
It takes in the name of information the user wants to extract and then dispays the data. The available parameters are:
- `modules`
- `info`
- `options`
- `aliases`
- `macros`

### SYNTAX
```
show [parameter] [optional parameter if supported]
```

## The Parameters
### Modules
- This parameter lists all the available modules provided by the toolkit.
- It looks up for the list of available modules in the `config.py` from the project root.
- It also looks for the currently active module from withing the `interpreter` and marks it as `(in use)` if active.

### Info
- This parameter returns the list of all available options related to the currently active module.
- It also provides an in hand description of each option and what possible values the option can hold.

### Options
- This parameter lists all the available options for a given module along with their assigned values and a short description related to each option.
- If no module is provided as an argument it looks up for the current active module from the `interpreter`,
    - If still no module is found it displays the list of all options,
    - Else it displays the list of options for the active module.
- It also highlights each option based on its necessity and the value assigned.

### Aliases
- Lists all the active or existing aliases along with their assigned values.

### Macros
- Lists all the active or existing macros along with their assigned values.
---
### EXAMPLE
```
show options #Show options for currently active module
show options ports #Show options for the 'ports' module
```
```
show aliases
```
...

## Exit Codes
- `0` -> Successfull command execution.
- `1` -> Some internal fault occured.
- `2` -> Invalid arguments found
- `3` -> Unexpected arguments found