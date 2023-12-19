# Python command tool

## Require
+ python3.5 +

## Description
`
It is used to run your Python code as a command line .
It only works on class methods .
Add as_cmder decorator on your class method and create command class in command file directory .
In your project root directory, create a pycmd.py file and import everything under the bdpycmd.pycmd module .
Add initialization code and execution entry to your pycmd.py .
Open the command line interface, go to your project root directory (the same level as your pycmd.py file), and run python pycmd.py .
`
## Use the example project url
<https://github.com/biandoucheng/open-example/tree/main/bdpycmd-example>

## Source Codd url
<https://github.com/biandoucheng/bd-py-cmd>

## Annotation Specification
`
When adding comments to the command method, the following rules must be followed, otherwise the command parameters will not be parsed correctly

@base.BaseCommand.as_cmder
def your_func(p1,p2):
    """
    your function`s description

    :param p1: type #describe
    :param p2: type #describe
    :return: type
    """
    your_func_content ...
`
## New features
`
2023.06.13
1. Support command keyword retrieval:
    No content input, press Enter directly to reality the next command
    Enter the command number or any range, and relevant commands will be queried based on the provided content
    Enter the '/' symbol to exit the help prompt

2. Support executable methods for directly querying commands during command queries
    Enter the '.' symbol to exit the help prompt
    Enter '/' to query the executable method of the selected command

3. Fix Bugs
    Fix the issue of execution errors caused by the 'None' parameter in the run dictionary and optimize information output

2023.06.14
1. Support direct execution of methods when querying command executable methods
    Enter the '.' symbol to exit the help prompt
    Enter '/' to executable the selected method of the selected command
2. Fix Bug
    Fix 'm' parameter error in command method help
3. Fix Bug
    Fix the issue of command generation assistant generating command errors
4. Perf
    Optimize the command generation assistant to make the parameters of the command generation method clearer and easier to use
5. Perf
    When using the command assistant to generate commands, it supports forcibly overwriting the parameter 'abs' of existing command files

2023.06.15
1. Fix
    Fix errors in keyword retrieval methods

2023.06.20
1. Feat assistant
    Optimizing the Naming of Command File Names. Allow the parameter cmd to be passed in as the name of the command and command file.

2023.07.06
1. Feat cmder list
    Optimized command recognition speed. Dynamically determine whether to import command implementation classes based on whether command methods need to be executed, in order to significantly reduce the number of modules that need to be loaded when listing commands, thereby accelerating the display of command lists

2023.07.10
1. Fix command module import error
    Fix command execution error `run command failed: module 'cmder.***' has no attribute 'Command' ` caused by delayed loading of command implementation module .

2023.12.07
1. Fix the error where carriage return causes the command or method to be directly selected for execution when there is only one command or method .

2023.12.19
1. Fix the issue where functions marked as commands cannot be executed directly through function calls with incomplete parameter input
`