
"""Integra os reconhecedores e percorre o código-fonte Jalan."""

try:
    from . import identifiers, literals, symbols
except ImportError:
    import identifiers
    import literals
    import symbols


class LexicalError(Exception):
    """Erro encontrado durante a análise léxica."""

    def __init__(self, char, line, column):
        self.char = char
        self.line = line
        self.column = column

        super().__init__(
            f"Caractere inválido {char!r} na linha {line}, coluna {column}."
        )


def _advance_position(text, line, column):
    """Atualiza linha e coluna após consumir um trecho."""
    i = 0

    while i < len(text):
        char = text[i]

        if char == "\r":
            if i + 1 < len(text) and text[i + 1] == "\n":
                i += 1

            line += 1
            column = 1

        elif char == "\n":
            line += 1
            column = 1

        else:
            column += 1

        i += 1

    return line, column


def tokenize(source: str) -> list[dict]:
    """Converte o código-fonte Jalan em uma lista de tokens."""

    tokens = []
    position = 0
    line = 1
    column = 1

    recognizers = (
        identifiers.recognize,
        literals.recognize,
        symbols.recognize,
    )

    while position < len(source):
        char = source[position]

        # Ignora espaços em branco.
        if char.isspace():
            if char == "\r" and source[position:position + 2] == "\r\n":
                position += 2
                line += 1
                column = 1

            elif char in "\r\n":
                position += 1
                line += 1
                column = 1

            else:
                position += 1
                column += 1

            continue

        recognized = None

        # Tenta reconhecer o próximo token.
        for recognize in recognizers:
            result = recognize(source, position, line, column)

            if result is not None:
                recognized = result
                break

        # Nenhum reconhecedor aceitou o caractere.
        if recognized is None:
            raise LexicalError(char, line, column)

        token, consumed = recognized

        tokens.append(token)

        # Atualiza a posição após consumir o token.
        consumed_text = source[position:position + consumed]

        line, column = _advance_position(
            consumed_text, line, column
        )

        position += consumed

    return tokens
