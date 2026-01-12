#!/usr/bin/env python3
'''
This script creates a boilerplate for a basic Nix shell with a custom Python3 interpreter. 
'''
#Import libraries and modules
import argparse
import sys
from pathlib import Path

#Define positional and optional arguments of script
parser = argparse.ArgumentParser(
    description="Creates a shell.nix boilerplate for a Python3 dev environment."
)
parser.add_argument("env", help="Absolute path of the directory of the dev environment.")
parser.add_argument("-p", "--python_packages", nargs='+', help="List additional Python 3.13 packages that should be installed onto the Python interpreter.")
parser.add_argument("-s", "--shell-packages", nargs='+', help="List additional shell packages that into the dev environment.")
args = parser.parse_args()

#Define function for displaying lists as strings
def create_display_strings(list_iterable, list_string: str, prefix: str, tab: str) -> str:
    '''
    A way of creating displayed list as string values.
    '''
    for item in list_iterable:
        list_string = f"{list_string}    {tab}{prefix}{item}\n"
    return list_string    

#Define constants
DEV_ENV_DIR = Path(args.env)
PKGS_STRING = '''    ps.python-dotenv
        ps.requests
        ps.mypy
        ps.pylint
        ps.pylsp-mypy
'''

SHELL_PKGS_STRING = '''    pythonEnv
'''

if args.python_packages:
    PKGS_LIST = args.python_packages
    PKGS_STRING = create_display_strings(
        list_iterable=PKGS_LIST, list_string=PKGS_STRING, prefix="ps.", tab='    '
    )

if args.shell_packages:
    SHELL_PKGS_LIST = args.shell_packages
    SHELL_PKGS_STRING = create_display_strings(
            list_iterable=SHELL_PKGS_LIST, list_string=SHELL_PKGS_STRING, 
            prefix='', tab='    '
        )

BOILERPLATE = f"""
with import <nixpkgs> {{}};
let
    pythonEnv = python313.withPackages(ps: [
    {PKGS_STRING}    
    ]);
in
mkShell {{
    packages = [
    {SHELL_PKGS_STRING}
    ];
}}"""



#Define functions
def create_shell_nix(new_shell_path):
    '''
    Writes a new shell.nix file with the provided file path.
    '''
    with new_shell_path.open('w') as new_shell_nix:
        new_shell_nix.write(BOILERPLATE) 

def check_for_overwrite(matches) -> bool:
    '''
    Checks to see if there's any cause for an overwrite of files.
    '''
    if not list(matches):
        return False

    matches_string = ''
    matches_string = create_display_strings(
        list_iterable=matches, list_string=matches_string, prefix='', tab=''
    )
    print(f"The following Shell.nix file already exists:\n{matches_string}")
    user_input = input("Do you want to overwrite? <y/n>\n")
    if user_input.strip().lower() in ("y", "yes"):
        for file in list(matches):
            file_path = Path(file)
            create_shell_nix(new_shell_path=file_path)
        print("Overwrite successful.")

        return True

#Main Script
files = list(DEV_ENV_DIR.rglob("shell.nix"))
should_exit = check_for_overwrite(matches=files)

if should_exit:
    sys.exit(0)
else:
    create_shell_nix(new_shell_path=DEV_ENV_DIR / "shell.nix")
    print("New shell.nix created.")

# import pdb; pdb.set_trace()
