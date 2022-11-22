"""All the utility functions used in the program."""
import os

from variables import VALID_OPTIONS


def validate_option(arg: str) -> any:
    """Check that option provided is valid."""
    if arg in VALID_OPTIONS:
        return VALID_OPTIONS[arg]
    return 'Error: not a valid option!'


def does_file_exist(filename: str) -> bool:
    """Check if the filename given exist as a file."""
    if os.path.isfile(filename):
        return True
    return False
