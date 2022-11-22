"""All the global variables and constants used in the program."""
# history of valid instructions
history = []

# valid options provided as arguments to script
VALID_OPTIONS = {
    'help': __doc__,
    'history': "\n".join(history)
}

# operators.py variables
persons = []
teams_config = {
    'no_of_teams': -1,
    'no_per_team': 4
}
teams_desc = {}
teams = []