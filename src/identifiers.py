"""Reconhecimento de identificadores e palavras reservadas."""

KEYWORDS = {
    "int", "double", "string", "bool",
    "if", "else", "while", "for",
    "function", "return", "show",
}


def recognize(source: str, position: int, line: int, column: int):
    """Retorna (token, consumed) ou None se não reconhecer nesta posição.

    TODO: implementar o AFD para identificadores e classificar palavras
    reservadas. Formato do token: type, value, line, column.
    """
    raise NotImplementedError
