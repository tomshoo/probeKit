# The `use` command

The use command takes a module name as an argument and returns it back with an exit code of `0` if it is a valid module name, else it simply returns an empty string with an exit code of `1`.

### SYNTAX
``` text
use [module name]
```
---
The use command takes only one single argument and if not imput is provided it return the previous selected module with an exit status of `2`. If more than required arguments are provided the it returns with an exit status of `3`

### Example of `use` command
- If an invalid module name is given
``` text
[probkit]: 0$> use not_a_valid_module
Error: Invalid module 'not_a_valid_module'
*Hint: Refer to command `show modules` for a list of available modules
[probkit]: 1$>
```

- If a valid module name is given
```
[probkit]: 0$> use ports
MODULE => ports
[probeKit]: (ports): 0$>
```

- If more than one arguments is given
```
[probkit]: 0$> use multiple arguments as modules
Alert: too many arguments
[probkit]: 3$>
```