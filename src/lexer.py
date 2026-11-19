
"""Integra os reconhecedores e percorre o código-fonte."""

from identifiers import recognize as recognize_identifier
from literals import recognize as recognize_literal
from symbols import recognize as recognize_symbol


def tokenize(source: str) -> list[dict]:
    """Converte o código-fonte Jalan em uma lista de tokens."""

    tokens = []
    position = 0
    line = 1
    column = 1

    while position < len(source):
        current = source[position]

        # Ignora espaços, tabulações e quebras de linha
        if current.isspace():
            if current == "\n":
                line += 1
                column = 1
            else:
                column += 1

            position += 1
            continue

        # Tenta reconhecer o próximo token
        recognizers = [
            recognize_literal,
            recognize_identifier,
            recognize_symbol,
        ]

        recognized = False

        for recognizer in recognizers:
            result = recognizer(source, position, line, column)

            if result is not None:
                token, consumed = result

                if consumed <= 0:
                    raise ValueError(
                        "Reconhecedor retornou consumo inválido."
                    )

                tokens.append(token)

                text = source[position:position + consumed]
                newlines = text.count("\n")

                if newlines:
                    line += newlines
                    column = len(text) - text.rfind("\n")
                else:
                    column += consumed

                position += consumed
                recognized = True
                break

        # Nenhum reconhecedor aceitou o caractere
        if not recognized:
            raise SyntaxError(
                f"Erro léxico na linha {line}, coluna {column}: "
                f"caractere inesperado {current!r}"
            )

    return tokens
