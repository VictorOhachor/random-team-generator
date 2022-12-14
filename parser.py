"""Parses the tokens and determine if instruction set is valid or not."""
from sys import stderr

from operators import *

VALID_INST_SET = {
    'LOAD': 1,
    'COMBINE': 1,
    'SET': 2,
    'GENERATE': 1,
    'PRINT': 1
}


def validate_operands_count(
        opcode: str, operands_count: int | None,
        operands: list) -> list | None:
    """Validate that the number of operands passed is correct."""
    if operands_count != None:
        if len(operands) == operands_count:
            return operands
        else:
            print(
                f'Error: Number of operands passed {opcode} must be {operands_count}',
                file=stderr)
    else:
        print(f'Error: {opcode} is not a valid RTGen keyword.')


def parse_tokens(tokens: list) -> tuple | None:
    """
    Parse the tokens; Check that the number of operands passed to opcode is correct.

    :param tokens: (list) list of tokens generated by scan_inst

    :returns: (tuple) the appropriate function represented by pocode and the required operands or None
    """
    if tokens:
        opcode = tokens[0]
        operands_count = VALID_INST_SET.get(opcode)

        operands = validate_operands_count(opcode, operands_count, tokens[1:])

        if operands:
            return eval(f'inst_{opcode.casefold()}'), operands
