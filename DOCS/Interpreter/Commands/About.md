# The `about` command

The `about` command provides breif information about the provided argument.
It takes a single arguments as the module name, If multiple arguments are provided then it will discard all other arguments except the first one.

If no argument is given then it will lookup in the `interpreter` for currently activated module.

### SYNTAX
```
about [module name]
```

## Exit Codes
- `0` -> Successfull command execution
- `1` -> Module not found or no module provided