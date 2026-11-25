
"""Reconhecimento de números, strings e literais booleanos.

Todos os autômatos utilizam o mesmo executor (_run_afd).
Cada AFD possui tabela de transições, estados de aceitação,
função de classificação de caracteres e estado inicial.
"""

from dataclasses import dataclass
from string import ascii_letters, digits
from typing import Callable, NamedTuple, Optional

# Constantes

INTEGER_LITERAL = "INTEGER_LITERAL"
DECIMAL_LITERAL = "DECIMAL_LITERAL"
STRING_LITERAL = "STRING_LITERAL"
BOOLEAN_LITERAL = "BOOLEAN_LITERAL"

DIGITS = frozenset(digits)
IDENTIFIER_CHARS = frozenset(ascii_letters + digits + "_")
VALID_ESCAPES = frozenset('"\\ntr')

# Classificadores de caracteres


def _number_class(_state, char):
    if char in DIGITS:
        return "D"
    if char == ".":
        return "DOT"
    return "OTHER"


def _string_class(state, char):
    if state == "q2":
        return "ESC_VALID" if char in VALID_ESCAPES else "ESC_INVALID"

    if char == '"':
        return "QUOTE"
    if char == "\\":
        return "BACKSLASH"
    if char in "\r\n":
        return "NEWLINE"

    return "CHAR"


def _boolean_class(_state, char):
    return char

# Estrutura dos AFDs

@dataclass(frozen=True)
class AFD:
    transitions: dict
    accepting: frozenset
    classify: Callable[[str, str], str]
    start: str = "q0"


# AFD dos Inteiros


INTEGER_AFD = AFD(
    transitions={
        ("q0", "D"): "q1",
        ("q1", "D"): "q1",
    },
    accepting=frozenset({"q1"}),
    classify=_number_class,
)

# AFD dos Decimais


DECIMAL_AFD = AFD(
    transitions={
        ("q0", "D"): "q1",
        ("q1", "D"): "q1",
        ("q1", "DOT"): "q2",
        ("q2", "D"): "q3",
        ("q3", "D"): "q3",
    },
    accepting=frozenset({"q3"}),
    classify=_number_class,
)


# AFD das Strings


STRING_AFD = AFD(
    transitions={
        ("q0", "QUOTE"): "q1",
        ("q1", "CHAR"): "q1",
        ("q1", "BACKSLASH"): "q2",
        ("q1", "QUOTE"): "qf",
        ("q2", "ESC_VALID"): "q1",
    },
    accepting=frozenset({"qf"}),
    classify=_string_class,
)


# AFD dos Booleanos


BOOLEAN_AFD = AFD(
    transitions={
        ("q0", "t"): "q1",
        ("q1", "r"): "q2",
        ("q2", "u"): "q37",
        ("q37", "e"): "qf",

        ("q0", "f"): "q4",
        ("q4", "a"): "q5",
        ("q5", "l"): "q6",
        ("q6", "s"): "q37",
    },
    accepting=frozenset({"qf"}),
    classify=_boolean_class,
)

# Executor genéricos dos AFDs


class RunResult(NamedTuple):
    state: str
    accept_end: Optional[int]


def _run_afd(afd: AFD, source: str, position: int) -> RunResult:
    state = afd.start
    i = position

    last_accept = i if state in afd.accepting else None

    while i < len(source):
        char_class = afd.classify(state, source[i])

        next_state = afd.transitions.get((state, char_class))

        if next_state is None:
            break

        state = next_state
        i += 1

        if state in afd.accepting:
            last_accept = i

    return RunResult(state, last_accept)


# Funções Auxiliares


def _token(type_, value, line, column):
    return {
        "type": type_,
        "value": value,
        "line": line,
        "column": column,
    }


def _ends_cleanly(source, end, forbidden=IDENTIFIER_CHARS):
    return end >= len(source) or source[end] not in forbidden


def _build(type_, source, position, end, line, column):
    return (
        _token(type_, source[position:end], line, column),
        end - position,
    )


# Reconhecimento dos Números


NUMBER_FORBIDDEN_AFTER = IDENTIFIER_CHARS | {"."}


def _recognize_number(source, position, line, column):
    result = _run_afd(DECIMAL_AFD, source, position)

    if result.accept_end is not None:
        end = result.accept_end

        if not _ends_cleanly(source, end, NUMBER_FORBIDDEN_AFTER):
            return None

        return _build(
            DECIMAL_LITERAL, source, position, end, line, column
        )

    if result.state == "q2":
        return None

    result = _run_afd(INTEGER_AFD, source, position)

    if result.accept_end is None:
        return None

    end = result.accept_end

    if not _ends_cleanly(source, end, NUMBER_FORBIDDEN_AFTER):
        return None

    return _build(
        INTEGER_LITERAL, source, position, end, line, column
    )


# Reconhecimento das Strings


def _recognize_string(source, position, line, column):
    result = _run_afd(STRING_AFD, source, position)

    end = result.accept_end

    if end is None:
        return None

    return _build(
        STRING_LITERAL, source, position, end, line, column
    )


# Reconhecimento dos Booleanos

def _recognize_boolean(source, position, line, column):
    result = _run_afd(BOOLEAN_AFD, source, position)

    end = result.accept_end

    if end is None:
        return None

    if not _ends_cleanly(source, end):
        return None

    return _build(
        BOOLEAN_LITERAL, source, position, end, line, column
    )

# Dispatch

_DISPATCH = {
    **{digit: _recognize_number for digit in DIGITS},
    '"': _recognize_string,
    "t": _recognize_boolean,
    "f": _recognize_boolean,
}

# Função Pública

def recognize(source: str, position: int, line: int = 1, column: int = 1):
    if not 0 <= position < len(source):
        return None

    recognizer = _DISPATCH.get(source[position])

    if recognizer is None:
        return None

    return recognizer(source, position, line, column)
