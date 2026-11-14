"""Reconhecimento de identificadores e palavras reservadas."""

KEYWORDS = {
    "int", "double", "string", "bool",
    "if", "else", "while", "for",
    "function", "return", "show",
}


def recognize(source: str, position: int, line: int, column: int):
    """Retorna (token, consumed) ou None se não reconhecer nesta posição."""
    if position >= len(source):
        return None

    first = source[position]
    if not (first.isalpha() or first == "_"):
        return None

    end = position + 1
    while end < len(source) and (source[end].isalnum() or source[end] == "_"):
        end += 1

    value = source[position:end]
    token_type = "KEYWORD" if value in KEYWORDS else "IDENTIFIER"
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column,
    }, end - position
