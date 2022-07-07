# The `back` command

The `back` command allows the user to go backwards from the selected module.
It takes no additional arguments from the user.

If the currently activated module is the only one activated since the initialization of the `interpreter` then `back` would simply deactivate the module.

If multiple modules have been activated then `back` would deactivate the current module and reactivate the previously active module.

### SYNTAX
```
back
```

## Exit Codes
`back` returns exit code `0` if it executed successfully.

If no module is active then `back` returns an exit code of `1`