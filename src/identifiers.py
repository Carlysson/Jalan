"""Identificadores e palavras reservadas."""


import string


KEYWORDS = {
    "int", "double", "string", "bool",
    "if", "else", "while", "for",
    "function", "return", "show",
}


LETTERS = set(string.ascii_letters) | set("_")
DIGITS = set(string.digits)

def _symbol_class(char):
    if char in LETTERS:
        return "L"
    elif char in DIGITS:
        return "D"
    else:
        return "O"


START = "q0"
ACEPTING = {"q1"}
DEAD = {"qe"}

TRANSITIONS = {
    ("q0", "L"): "q1",
    ("q0", "D"): "qe",
    ("q0", "O"): "qe",
    ("q1", "L"): "q1",
    ("q1", "D"): "q1",
    ("q1", "O"): "qe",
    ("qe", "L"): "qe",
    ("qe", "D"): "qe",
    ("qe", "O"): "qe",
}


def recognize(source: str, position: int, line: int, column: int):
    """Retorna (token, consumed) ou None se não reconhecer nesta posição.

    TODO: implementar o AFD para identificadores e classificar palavras
    reservadas. Formato do token: type, value, line, cSolumn.
    """
    raise NotImplementedError
