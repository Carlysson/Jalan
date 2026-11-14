"""Reconhecimento de números, strings e literais booleanos."""


def _parse_string(source: str, start: int) -> tuple[str, int]:
    """Lê uma string entre aspas duplas e retorna o valor e o tamanho consumido."""
    end = start + 1
    while end < len(source):
        if source[end] == "\\" and end + 1 < len(source):
            end += 2
            continue
        if source[end] == '"':
            value = source[start + 1:end]
            value = value.replace('\\"', '"').replace('\\\\', '\\')
            return value, end - start + 1
        end += 1
    raise ValueError(f"String sem fechamento em linha {source!r}")


def recognize(source: str, position: int, line: int, column: int):
    """Retorna (token, consumed) ou None se não reconhecer nesta posição."""
    if position >= len(source):
        return None

    if source.startswith("true", position):
        next_char = source[position + 4] if position + 4 < len(source) else ""
        if not (next_char.isalnum() or next_char == "_"):
            return {
                "type": "BOOLEAN",
                "value": True,
                "line": line,
                "column": column,
            }, 4

    if source.startswith("false", position):
        next_char = source[position + 5] if position + 5 < len(source) else ""
        if not (next_char.isalnum() or next_char == "_"):
            return {
                "type": "BOOLEAN",
                "value": False,
                "line": line,
                "column": column,
            }, 5

    if source[position] == '"':
        value, consumed = _parse_string(source, position)
        return {
            "type": "STRING",
            "value": value,
            "line": line,
            "column": column,
        }, consumed

    if source[position].isdigit():
        end = position + 1
        while end < len(source) and source[end].isdigit():
            end += 1

        if end < len(source) and source[end] == "." and end + 1 < len(source) and source[end + 1].isdigit():
            end += 1
            while end < len(source) and source[end].isdigit():
                end += 1
            value = float(source[position:end])
            token_type = "DOUBLE"
        else:
            value = int(source[position:end])
            token_type = "INTEGER"

        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column,
        }, end - position

    return None
