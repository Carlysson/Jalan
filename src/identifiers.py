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


KEYWORD = "KEYWORD"
IDENTIFIER = "IDENTIFIER"

START = "q0"
ACCEPTING = {"q1"}
DEAD = "qe"

TRANSITIONS = {
    "q0": {"L": "q1", "D": DEAD, "O": DEAD},
    "q1": {"L": "q1", "D": "q1", "O": DEAD},
    "qe": {"L": DEAD, "D": DEAD, "O": DEAD},
}

def _token(type_, value, line, column):
    return {
        "type": type_,
        "value": value,
        "line": line,
        "column": column,
    }


def recognize(source: str, position: int, line: int = 1, column: int = 1):

    if not 0 <= position < len(source):
        return None

    estado = START
    i = position

    while i <len(source):
        classe = _symbol_class(source[i])
        proximo = TRANSITIONS[estado][classe]
        if proximo == DEAD:
            break
        estado = proximo
        i += 1

    if estado not in ACCEPTING:
        return None

    lexema = source[position:i]
    tipo = KEYWORD if lexema in KEYWORDS else IDENTIFIER
    return _token(tipo, lexema, line, column), len(lexema)
