
"""Reconhecimento de números, strings e literais booleanos."""


# Os tipos de tokens


INTEGER_LITERAL = "INTEGER_LITERAL"
DECIMAL_LITERAL = "DECIMAL_LITERAL"
STRING_LITERAL = "STRING_LITERAL"
BOOLEAN_LITERAL = "BOOLEAN_LITERAL"


# Classe de Caracteres que serão utilizados

DIGITS = set("0123456789")
LETTERS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
IDENTIFIER_CHARS = LETTERS | DIGITS | {"_"}


def _number_class(char):
    if char in DIGITS:
        return "D"
    elif char == ".":
        return "DOT"
    return "O"


def _string_class(char):
    if char == '"':
        return "QUOTE"
    elif char == "\\":
        return "BACKSLASH"
    elif char in ("\n", "\r"):
        return "NEWLINE"
    return "CHAR"


def _is_identifier_continue(char):
    return char in IDENTIFIER_CHARS


# AFD dos números inteiros


INTEGER_START = "q0"
INTEGER_ACCEPTING = {"q1"}

INTEGER_TRANSITIONS = {
    ("q0", "D"): "q1",
    ("q1", "D"): "q1",
}

# AFD dos números decimais


DECIMAL_START = "q0"
DECIMAL_ACCEPTING = {"q3"}

DECIMAL_TRANSITIONS = {
    ("q0", "D"): "q1",
    ("q1", "D"): "q1",
    ("q1", "DOT"): "q2",
    ("q2", "D"): "q3",
    ("q3", "D"): "q3",
}

# AFD das Strings (com escape)


STRING_START = "q0"
STRING_ACCEPTING = {"qf"}

STRING_TRANSITIONS = {
    ("q0", "QUOTE"): "q1",
    ("q1", "CHAR"): "q1",
    ("q1", "BACKSLASH"): "q2",
    ("q1", "QUOTE"): "qf",
    ("q2", '"'): "q1",
    ("q2", "\\"): "q1",
    ("q2", "n"): "q1",
    ("q2", "t"): "q1",
    ("q2", "r"): "q1",
}


# AFD dos Booleanos


BOOLEAN_START = "q0"
BOOLEAN_ACCEPTING = {"qf"}

BOOLEAN_TRANSITIONS = {
    ("q0", "t"): "q1",
    ("q1", "r"): "q2",
    ("q2", "u"): "q3",
    ("q3", "e"): "qf",

    ("q0", "f"): "q4",
    ("q4", "a"): "q5",
    ("q5", "l"): "q6",
    ("q6", "s"): "q7",
    ("q7", "e"): "qf",
}

# Funções auziliares


def _token(type_, value, line, column):
    return {
        "type": type_,
        "value": value,
        "line": line,
        "column": column
    }


def _run_afd(source, position, start, accepting,
             transitions, classify):

    state = start
    i = position
    last_accept = None

    if state in accepting:
        last_accept = i

    while i < len(source):
        char_class = classify(source[i])
        next_state = transitions.get((state, char_class))

        if next_state is None:
            break

        state = next_state
        i += 1

        if state in accepting:
            last_accept = i

    return state, i, last_accept


# Reconhecimento dos inteiros e decimais


def _recognize_number(source, position, line, column):

    decimal_state, decimal_end, decimal_accept = _run_afd(
        source,
        position,
        DECIMAL_START,
        DECIMAL_ACCEPTING,
        DECIMAL_TRANSITIONS,
        _number_class
    )

    has_decimal_point = (
        decimal_state == "q2"
        or (
            decimal_end < len(source)
            and source[decimal_end] == "."
            and decimal_state == "q1"
        )
    )

    if has_decimal_point:
        if decimal_accept is None:
            return None

        end = decimal_accept

        if end < len(source):
            if (
                _is_identifier_continue(source[end])
                or source[end] == "."
            ):
                return None

        value = source[position:end]

        return (
            _token(DECIMAL_LITERAL, value, line, column),
            end - position
        )

    integer_state, integer_end, integer_accept = _run_afd(
        source,
        position,
        INTEGER_START,
        INTEGER_ACCEPTING,
        INTEGER_TRANSITIONS,
        _number_class
    )

    if integer_accept is None:
        return None

    end = integer_accept

    if end < len(source):
        if (
            _is_identifier_continue(source[end])
            or source[end] == "."
        ):
            return None

    value = source[position:end]

    return (
        _token(INTEGER_LITERAL, value, line, column),
        end - position
    )



# Reconhecimento das Strings


def _recognize_string(source, position, line, column):

    state = STRING_START
    i = position

    while i < len(source):
        char = source[i]
        char_class = _string_class(char)

        if state == "q2":
            next_state = STRING_TRANSITIONS.get((state, char))
        else:
            next_state = STRING_TRANSITIONS.get((state, char_class))

        if next_state is None:
            return None

        state = next_state
        i += 1

        if state in STRING_ACCEPTING:
            value = source[position:i]

            return (
                _token(STRING_LITERAL, value, line, column),
                i - position
            )

    return None


# Reconhecimento dos Booleanos


def _recognize_boolean(source, position, line, column):

    state = BOOLEAN_START
    i = position

    while i < len(source):
        char = source[i]
        next_state = BOOLEAN_TRANSITIONS.get((state, char))

        if next_state is None:
            break

        state = next_state
        i += 1

        if state in BOOLEAN_ACCEPTING:

            if i < len(source):
                if _is_identifier_continue(source[i]):
                    return None

            value = source[position:i]

            return (
                _token(BOOLEAN_LITERAL, value, line, column),
                i - position
            )

    return None


# Função que será a principal


def recognize(source: str, position: int, line: int = 1, column: int = 1):
    """
    Ela reconhece números, strings e literais booleanos.

    e vai retornar (token, consumed) ou None se não reconhecer.
    """

    if position < 0 or position >= len(source):
        return None

    char = source[position]

    if char == '"':
        return _recognize_string(source, position, line, column)

    if char in DIGITS:
        return _recognize_number(source, position, line, column)

    if char in ("t", "f"):
        return _recognize_boolean(source, position, line, column)

    return None
