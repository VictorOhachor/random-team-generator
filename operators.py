"""Contain the operating functions for the available keywords or opcodes."""
from sys import stderr, stdout
import random
import os

from variables import persons, teams_config, teams_desc, teams
from utilities import does_file_exist

# helper functions


def _is_name_valid(name: list) -> bool:
    """Check if name provided is valid."""
    if 0 < len(name) <= 2:
        return True
    print(f'\nError: {" ".join(name)} must contain at least firstname or at most firstname and lastname!\n')
    return False


def _is_valid_line(line: str, validator, lineno: int, filename: str) -> bool:
    """Validate given line with validator."""
    if validator(line):
        return True
    print(f'Error on line {lineno + 1} in {filename}...')
    return False


def _is_proper_desc(line: str) -> bool:
    """Check that desc line is valid."""
    tokens = line.strip().split('-', 1)
    if len(tokens) == 2 and tokens[0].strip().isnumeric():
        return True
    return False


def _set_no_per_t(v: str):
    """Set no_per_team to value."""
    print(f'Setting no_per_team to {v}')
    value = int(v)

    if not value:
        print('Number of members in a team cannot be zero!')
    else:
        teams_config['no_per_team'] = value


def _set_no_of_t(v: str):
    """Set no_of_team to value."""
    print(f'Setting no_of_team to {v}')
    value = int(v)

    if not value:
        print('Number of teams to be generated cannot be zero!')
    else:
        teams_config['no_of_teams'] = value


def _set_t_desc(filename: str):
    """Set teams_desc to content of filename."""
    print(f'Based on {filename}, setting teams description...')

    if does_file_exist(filename):
        with open(filename, 'r') as file:
            descs = file.readlines()
            for no, line in enumerate(descs):
                # each line will be in the form [no] - [desc]
                if _is_valid_line(line, _is_proper_desc, no, filename):
                    tokens = line.strip().split('-', 1)
                    teams_desc[tokens[0].strip()] = tokens[1].strip()
            return True if len(teams_desc) == len(descs) else False
    return False


def _print_teams(teams: list, file=stdout):
    """Print teams."""
    count = 0

    for team in teams:
        count += 1
        for key, value in team.items():
            print(f'\n~~~~ Team {count} {key.upper()} ~~~~', file=file)
            if type(value) == list:
                for idx, item in enumerate(value, 1):
                    print(f'{idx}: {item}', file=file)
            else:
                print(value, file=file)


# operating functions
def inst_load(filename: str) -> bool:
    """Load the names provided in filename into a list."""
    print(f'Loading content of {filename} to memory...')
    if not does_file_exist(filename):
        print(
            f'Error: {filename} was not found. Ensure path to filename is correct',
            file=stderr)
    else:
        with open(filename, 'r') as file:
            names = file.readlines()
            for line in names:
                name = line.strip().split()
                if _is_name_valid(name):
                    persons.append(" ".join(name))
            return True if persons else False
    return False


def inst_set(command: str, argument: str) -> bool:
    """
    Set some options to control the teams generation.

    :param command: (str) the option type
    :param argument: (str) argument passed to the option

    :returns: (bool) True if operation was successful, otherwise false
    """
    print(f'Setting option "{command}" based on argument "{argument}"...')
    COMMAND_LIST = {
        'NO_PER_T': _set_no_per_t,
        'NO_OF_T': _set_no_of_t,
        'T_DESC': _set_t_desc
    }

    if command in COMMAND_LIST:
        COMMAND_LIST.get(command)(argument)
        return True

    print(f'{command} is not a valid command to SET.')
    return False


def inst_combine(filename: str) -> bool:
    """Combine names in filename to existing names."""
    print(f'Combining names in {filename} to the current list...')
    if persons:
        return inst_load(filename)

    print('Error: LOAD a file before you COMBINE another.')
    return False


def inst_generate(option: str):
    """Generate teams based on names and configuration."""
    print('Generating teams randomly from names and configuration...')

    OPTION_SET = ['-quiet', '-verbose']

    new_team = {'members': [], 'desc': ''}
    names = set(persons)
    possible_teams_count = len(names) // teams_config['no_per_team']

    for i in range(possible_teams_count):
        # check that no_of_teams is not exceeded when set
        if i == teams_config['no_of_teams']:
            break

        for _ in range(teams_config['no_per_team']):
            person = random.choice(list(names))
            if person not in new_team['members']:
                new_team['members'].append(person)
            names.discard(person)

        desc = teams_desc.get(f'{i + 1}')
        if desc:
            new_team['desc'] = desc

        teams.append(new_team)
        new_team = {'members': [], 'desc': ''}

    if teams:
        if option.strip() == OPTION_SET[1]:
            _print_teams(teams)

        elif option.strip() == OPTION_SET[0] and names:
            print('\n------------ Unassigned names -------------')
            [print(f'{no}: {p}') for no, p in enumerate(names, 1)]
            print("---------------------------------------------\n")
        return True

    return False


def inst_print(filename: str) -> bool:
    """Output result to filename."""
    print(f'Saving results to {filename}...')

    if not teams:
        print('Error: GENERATE results before PRINTing!')
        return False

        print()
    with open(filename, "w") as file:
        file.write('============= Generated Teams ==============\n\n')
        _print_teams(teams, file=file)

    return True
