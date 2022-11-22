"""
Generate teams randomly from a list of persons based on instructions supplied in a script.

Usage:

    $ python3 rtgen.py filename.rtgen

    where filename is the name of script with instructions to be consumed by rtgen.py
    filename must end with the extension .rtgen

    Example of instructions in filename.rtgen:

    ------------ filename.rtgen -------------
    1. LOAD names.txt # loads the names of persons in names.txt into a list
    2. SET NO_PER_T 4 # set the number of members per team
    3. SET NO_OF_T 5 # set the number of teams to be generated as 5
    4. COMBINE names1.txt # combines the list of names in names1.txt to the list in names.txt
    5. SET T_DESC teams_desc.txt # set teams descriptions where each line is a team's description
    6. GENERATE -quiet # generate teams randomly using set options. -quiet means that no output would be seen
    7. PRINT output.txt # outputs result to output.txt
    --------- END OF filename.rtgen ---------

    $ python3 rtgen.py --help # display help message
"""
import sys

from utilities import validate_option, does_file_exist
from variables import history
from scanner import scan_inst
from parser import parse_tokens


def process_instruction(inst: str) -> bool:
    """
    Process given instruction and determine if instruction is valid or not.

    :param inst: (str) the instruction set provided

    :returns: (bool) True on success, otherwise false
    """
    tokens = scan_inst(inst)
    if not tokens:
        return True

    command_set = parse_tokens(tokens)

    if command_set:
        return command_set[0](*command_set[1])
    return False


def run(filename: str) -> None:
    """Run the logic of the script."""
    if not filename.endswith('.rtgen'):
        if filename.startswith('--'):
            print(validate_option(filename[2:]))
        else:
            print(
                'Error: filename extension must be ".rtgen" e.g script.rtgen',
                file=sys.stderr
            )
        return

    if not does_file_exist(filename):
        print('Error: file does not exist!', file=sys.stderr)
    else:
        with open(filename, 'r') as file:
            for instruction in file.readlines():
                inst_status = process_instruction(instruction)
                if inst_status:
                    history.append(instruction)
                else:
                    break

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python main.py [path/to/script]', file=sys.stderr)
    else:
        run(sys.argv[1])
