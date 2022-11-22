"""Contain the 'scan_inst' function and its helper functions."""


def _add_token(token: str, tokens: list) -> str:
    """Add token to tokens if not empty."""
    if token:
        tokens.append(token)
        token = ''
    return token


def scan_inst(inst: str) -> list:
    """Scan and split instruction into tokens."""
    tokens = []
    token = ''

    chars_set = list(inst)

    while chars_set:
        c = chars_set.pop(0)

        if c == ' ' or c == '\n':
            token = _add_token(token, tokens)
        else:
            token += c
        
        if c == '#':
            break
    return tokens
