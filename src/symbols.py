"""Reconhecimento de operadores, delimitadores e comentários."""

# NOME DOS TIPOS DE TOKENS 
OPERATOR = "OPERATOR"
DELIMITER = "DELIMITER"
COMMENT = "COMMENT"

TWO_CHAR_OPERATORS = ("==", "!=", ">=", "<=", "++", "--", "&&", "||")
ONE_CHAR_OPERATORS = ("+", "-", "*", "/", "%", ">", "<", "=", "!", "&", "|")
DELIMITERS = ("(", ")", "{", "}", ";", ",")
COMMENTS = ("//",)

def _token(type_, value, line, column):
    return {"type": type_, "value": value, "line": line, "column": column}

def recognize(source: str, position: int, line: int = 1, column: int = 1):
    """tenta reconhecer um simbolo em source [position]"""

    """Retorna (token, consumed) ou None se não reconhecer nesta posição."""
    if position >= len(source):
        return None

    # 1. Comentário "//" até o fim da linha (obs: testar antes do operador "/"
    if source.startswith("//", position):
        end = source.find("\n", position)
        if end == -1:
            end = len(source)
        value = source[position:end].rstrip("\r")
        return _token(COMMENT, value, line, column), end - position

    # 2. Operadores de dois caracteres (maior união primeiro)
    two_char = source[position:position + 2]
    if two_char in TWO_CHAR_OPERATORS:
        return _token(OPERATOR, two_char, line, column), 2

    # 3. Operadores de um caractere 
    one_char = source[position]
    if one_char in ONE_CHAR_OPERATORS:
        return _token(OPERATOR, one_char, line, column), 1

    # 4. Delimitadores
    if one_char in DELIMITERS:
        return _token(DELIMITER, one_char, line, column), 1

    return None