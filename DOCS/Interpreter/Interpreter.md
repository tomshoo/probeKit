# Introduction

The interpreter is the most crucial part of the toolkit. It provides maximum flexibility around the toolkit and the actual CLI of the toolkit uses the interpreter for executing most of the commands.

The Interpreter provides an interface to the user where they can provides the commands to execute. The key properties of the interpreter are:

- The interpreter provides with an interface to work with the toolkit
- It takes input in form of commands
- It can also perform few system based commands for further improving flexibility and providing the user with an option to not change terminal to execute a system command.
    - The interpreter can take system commands but it has some limitations, such as:
        - The tookit will try to prevent any high privileged system actions.
            - It will not execute any system commands if launched as a high privileged user (i.e `administrator` on Windows or `root` on UNIX based OS(s)).
            - If a script is to be executed by the interpreter, it would not execute the script if it requests for higher privileges by using `sudo` (on UNIX) or `gsudo` (on Windows).
            - These measures are to prevent user security if by accident someone can access this toolkit with admin rights(like giving access to user to launch the interpreter with admin privileges without asking for password)
        - The interpreter cannot use the output of a command into another command
        - Features affected by this are:
            - Command piping
            - Assigning output of a command to a variable
            - Inability to write the output of a command to a file