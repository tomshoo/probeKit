# Macros

## Description
Macros are more advanced form of aliasing. Macros unlike aliases can be used anywhere in the command. New macros can be created using the `set` command.

### EXAMPLE
```
set macro lcl=0.0.0.0
```

To define permanent macros the user needs to configure the `UserConfig.py` locate in the project root.

The default provided macros are:
```json
{
    "localhost": "127.0.0.1",
    "example": "https://www.example.com",
}
```

## Usage
Macros though are advanced when compared to aliases they also require certain aditional steps to use.

To use any macro in the command the user can call it by `$(macro_name)` or `$macro_name`

> If called via `$(macro_name)` then if the macro is not found then its value is substituted by the macro name.

> If called via `$macro_name` then if no macro with that name is found then an empty string is substituted for the macro

### EXAMPLE
- If an existing macro named `lcl` exists with a value of `0.0.0.0`
```
> set option thost=$lcl
> set option thost=$(lcl)
# Both methods would provide the same command i.e 'set option thost=0.0.0.0'
```

- If no macro named `localhost` exists (Using `$localhost`)
```
> set option thost=$localhost
# Command gets translated to 'set option='
```

- If no macro named `localhost` exists (Using `$(localhost)`)
```
> set option thost=$(localhost)
# Command gets translated to 'set option=localhost'
```