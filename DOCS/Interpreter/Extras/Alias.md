# Aliases

## Description
Aliases are substitutes that can be used instead of bigger and complex commands.
They behave just like the aliases in shells like `bash`, `zsh`, etc...

New aliases can be created via the `set` command.
### Example of creating a new alias
```
set alias option='set option'
set alias back='do {back} -n -t'
```

Default aliases can be assigned by editing the `aliases` dictionary in the `UserConfig.py` file present in the project root directory.

Some default aliases are:
``` json
{
    "execute": "run",
    "info": "show info",
    "options": "show options"
}
```

Any new alias created by using the `set` command will not persist through every session. To make permanent aliases you need to edit the configuration file.

### EXAMPLE OF USAGE
```
> info #Itself it is an invalid command
> set alias info='show info' #Create a new alias named info
> info #Execute the 'info' aliased to 'show info'
```