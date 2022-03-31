# The `unset` command

The `unset` command does the opposite of `set` command.
It unassigns the value from a given key. It features the same sub commands as the `set` command, i.e,
- `macro`,
- `alias`,
- `option`

### SYNTAX
```
unset [sub command] [key_1] [key_2] [key_3] ... [key_N]
```

## The sub commands
The sub commands are the same as those in the `set` command, i.e,
- `macro` -> Delete a macro, can take multiple keys at once or all as a key if user needs to delete all the keys.
- `alias` -> Same as `macro` but deletes an alias.
- `option` -> Unassign the value from an `option`. It does not delete the option but sets its value to an empty string.

### EXAMPLES
- Delete a macro
```
unset macro localhost #Assuming 'localhost' was a defined macro
```

- Delete an alias
```
unset alias info #Assuming 'alias' was an existing alias
```

- Unassign an option
```
unset option thost
```

## Exit Codes
- `0` -> Command executed successfully
- `1` -> Given key was not found, or some internal fault occured
- `2` -> Invalid sub command found
- `3` -> Broken arguments found