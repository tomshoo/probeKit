# The `set` command

The `set` command provides with the ability to assign `macros`, `aliases` and required module `options` to work with the toolkit.

### SYNTAX
```
set [sub-command] [key_1]=[value_1] [key_2]=[value_2] ... [key_N]=[value_N]
```

### Sub Commands
The sub commands for this command are:
- `macro` -> Create a new macro or update an existing one
- `alias` -> Create a new alias or update the existing one
- `option` -> Assign a value to a module option

#### MACRO
The `macro` sub command allows the user to create a new macro.
It takes only one set of key value pairs unlike other sub commands which take multiple key value pairs for assignment

##### EXAMPLE
```
set macro localhost=127.0.0.1
```

#### ALIAS
The `alias` sub command allows the use to create or update an alias. It can take multiple key value pairs from the user.
Aliases behave as smaller substitute commands for much larger and complex commands

##### EXAMPLE
```
set alias info='show info'
```

#### OPTION
The `option` sub command provides with the utility to change the options required by the modules.
These options can be treated as some predefined **un-expandable** variables. Unlike the other sub commands, the values can only be update, no new keys can be created (hence the **un-expandable** part).

##### EXAMPLE
```
set option thost=0.0.0.0
```

## Exit Codes
- `0` -> Successfull execution of command
- `1` -> Unsuccessfull execution of command due to failure in assigning or updating values
- `2` -> Unknown sub command
- `3` -> Un-acceptable number of arguments or broken arguments