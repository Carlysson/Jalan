"""Reconhecedor de operadores, delimitadores e comentários da linguagem Jalan."""

# Nomes dos tipos de token:

OPERATOR = "OPERATOR"
DELIMITER = "DELIMITER"
COMMENT = "COMMENT"

TWO_CHAR_OPERATORS = ("==", "!=", ">=", "<=", "&&", "||")
ONE_CHAR_OPERATORS = "+-*/%=><!"
DELIMITERS = ";(){},"


def _token(type_, value, line, column):
    return {"type": type_, "value": value, "line": line, "column": column}


def recognize(source: str, position: int, line: int = 1, column: int = 1):
    """Tenta reconhecer um símbolo em source[position].

    Retorna (token, consumed) se reconhecer, ou None caso contrário.
    """
    if position >= len(source):
        return None

    # 1. Comentário "//" até o fim da linha (testar antes do operador "/")

    if source.startswith("//", position):
        end = source.find("\n", position)
        if end == -1:
            end = len(source)
        value = source[position:end].rstrip("\r")
        return _token(COMMENT, value, line, column), len(value)

    # 2. Operadores de dois caracteres

    two = source[position:position + 2]
    if two in TWO_CHAR_OPERATORS:
        return _token(OPERATOR, two, line, column), 2

    # 3. Operadores de um caractere

    ch = source[position]
    if ch in ONE_CHAR_OPERATORS:
        return _token(OPERATOR, ch, line, column), 1

    # 4. Delimitadores

    if ch in DELIMITERS:
        return _token(DELIMITER, ch, line, column), 1

    return None