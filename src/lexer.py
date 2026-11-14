"""Integra os reconhecedores e percorre o código-fonte."""

from identifiers import recognize as recognize_identifier
from literals import recognize as recognize_literal
from symbols import recognize as recognize_symbol


def tokenize(source: str) -> list[dict]:
    """Converte o código-fonte Jalan em uma lista de tokens."""
    tokens: list[dict] = []
    position = 0
    line = 1
    column = 1

    while position < len(source):
        current = source[position]

        if current in " \t\r":
            position += 1
            column += 1
            continue

        if current == "\n":
            position += 1
            line += 1
            column = 1
            continue

        for recognizer in (recognize_literal, recognize_identifier, recognize_symbol):
            match = recognizer(source, position, line, column)
            if match is None:
                continue

            token, consumed = match
            tokens.append(token)
            position += consumed
            column += consumed
            break
        else:
            raise ValueError(f"Erro léxico em linha {line}, coluna {column}: '{current}'")

    return tokens
