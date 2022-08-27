# The `do` command

The `do` command is a simple utility command directly integrated with the `interpreter`. It provides a simple functionality to execute commands multiple times without having to retype them.

It takes two arguments:
- `-t` -> The number of times a command is supposed to be executed
- `-n` -> Should the actual exit code of the command be returned or not.

### SYNTAX
```
do {command to execute} [arguments]
```

### EXAMPLE
```
do {back} -t 3 -n
```

## Exit codes
This command generally return the exit code returned by the command it was supposed to execute.

If the `-n` argument is passed then it will always return the value of `0` as the exit code.