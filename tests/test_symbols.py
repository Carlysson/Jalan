"""Testes do reconhecedor de símbolos (operadores, delimitadores e comentários)."""

import os
import sys

import pytest

# Faz o Python achar symbols.py dentro de src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from symbols import recognize  # noqa: E402

OPERATOR = "OPERATOR"
DELIMITER = "DELIMITER"
COMMENT = "COMMENT"

DELIMITERS = [";", "(", ")", "{", "}", ","]
ONE_CHAR_OPERATORS = ["+", "-", "*", "/", "%", "=", ">", "<", "!"]
TWO_CHAR_OPERATORS = ["==", "!=", ">=", "<=", "&&", "||"]


def token(type_, value, line, column):
    """Monta o dicionário de token esperado."""
    return {"type": type_, "value": value, "line": line, "column": column}


# ---------- Delimitadores ----------
@pytest.mark.parametrize("delimiter", DELIMITERS)
def test_delimiter(delimiter):
    # esperado: token do tipo DELIMITER, value, line, column corretos e consumed = 1
    result = recognize(delimiter, 0, 1, 1)
    assert result == (token(DELIMITER, delimiter, 1, 1), 1)


# Operadores de 1 caractere 
@pytest.mark.parametrize("operator", ONE_CHAR_OPERATORS)
def test_one_char_operator(operator):
    # o espaço depois garante que o operador não é confundido com um de 2 caracteres
    result = recognize(operator + " x", 0, 1, 1)
    assert result == (token(OPERATOR, operator, 1, 1), 1)


# Operadores de 2 caracteres
@pytest.mark.parametrize("operator", TWO_CHAR_OPERATORS)
def test_two_char_operator(operator):
    # esperado: um único token e consumed = 2
    result = recognize(operator + " x", 0, 1, 1)
    assert result == (token(OPERATOR, operator, 1, 1), 2)


# Maior união
@pytest.mark.parametrize("operator, prefix", [
    ("==", "="), ("!=", "!"), (">=", ">"), ("<=", "<"),
])
def test_operator_union(operator, prefix):
    # ex: ">=" deve ser reconhecido como operador de 2 caracteres, não como ">" e "="
    tok, consumed = recognize(operator, 0, 1, 1)
    assert tok["value"] == operator
    assert tok["value"] != prefix
    assert consumed == 2


def test_operator_union_with_three_equals():
    # "===" vira "==" seguido de "="
    first, first_consumed = recognize("===", 0, 1, 1)
    second, second_consumed = recognize("===", 2, 1, 3)
    assert (first["value"], first_consumed) == ("==", 2)
    assert (second["value"], second_consumed) == ("=", 1)


# Comentários 
def test_comment():
    result = recognize("// ola mundo", 0, 1, 1)
    assert result == (token(COMMENT, "// ola mundo", 1, 1), 12)


def test_comment_at_end_of_line():
    # o comentário vai até o fim da linha e não consome o \n
    source = "// ola\nint x;"
    tok, consumed = recognize(source, 0, 1, 1)
    assert tok == token(COMMENT, "// ola", 1, 1)
    assert consumed == 6
    assert source[consumed] == "\n"


def test_comment_without_a_line_break_at_the_end():
    result = recognize("// fim", 0, 3, 1)
    assert result == (token(COMMENT, "// fim", 3, 1), 6)


def test_empty_comment():
    assert recognize("//", 0, 1, 1) == (token(COMMENT, "//", 1, 1), 2)


def test_comment_ignores_symbols_inside_it():
    source = '// a == b; show("x")'
    tok, consumed = recognize(source, 0, 1, 1)
    assert tok["type"] == COMMENT
    assert tok["value"] == source
    assert consumed == len(source)


def test_comment_with_windows_line_break():
    tok, consumed = recognize("// a\r\nint", 0, 1, 1)
    assert tok["value"] == "// a"
    assert consumed == 4


def test_comment_after_code_uses_given_line_and_column():
    source = "x = 1; // nota\ny = 2;"
    result = recognize(source, 7, 1, 8)
    assert result == (token(COMMENT, "// nota", 1, 8), 7)


def test_standalone_slash_and_operator():
    # "/" sozinho é divisão, não comentário
    assert recognize("/ 2", 0, 1, 1) == (token(OPERATOR, "/", 1, 1), 1)


def test_slashes_separated_by_space_are_not_a_comment():
    tok, consumed = recognize("/ /", 0, 1, 1)
    assert tok["type"] == OPERATOR
    assert consumed == 1


# Casos especiais 
def test_minus_sign_before_number():
    # ex: "-1" deve ser reconhecido como operador "-" (o número é do literals.py)
    assert recognize("-1", 0, 1, 1) == (token(OPERATOR, "-", 1, 1), 1)


def test_row_and_column_in_middle_position():
    # ex: "a + b" deve retornar token "+" com line=1 e column=3
    result = recognize("a + b", 2, 1, 3)
    assert result == (token(OPERATOR, "+", 1, 3), 1)


def test_token_on_another_line():
    source = "a\n\n  >= b"
    assert recognize(source, 5, 3, 3) == (token(OPERATOR, ">=", 3, 3), 2)


#  O que não reconhece (deve retornar None) 
@pytest.mark.parametrize("source", [
    "&", "|", "&|", "|&", "@", "#", "$", ".", ":", "[", "]", "?", "~", "^",
    "a", "Z", "_", "1", "9", '"', "'", " ", "\t", "\n",
])
def test_not_recognized(source):
    # ex: "&" não é reconhecido como símbolo, deve retornar None
    assert recognize(source, 0, 1, 1) is None


def test_incomplete_and_at_end_of_text():
    # "&" e "|" incompletos no fim do texto
    assert recognize("x &", 2, 1, 3) is None
    assert recognize("x |", 2, 1, 3) is None


def test_three_ampersands():
    tok, consumed = recognize("&&&", 0, 1, 1)
    assert (tok["value"], consumed) == ("&&", 2)
    assert recognize("&&&", 2, 1, 3) is None


def test_end_of_text():
    assert recognize("", 0, 1, 1) is None
    assert recognize("+", 1, 1, 2) is None
    assert recognize("+", 10, 1, 11) is None


# Consumed percorrendo uma sequência 
def scan_symbols(source):
    """Percorre o texto só com recognize, pulando espaços, usando o consumed."""
    position = 0
    result = []
    while position < len(source):
        if source[position] in " \t\r\n":
            position += 1
            continue
        found = recognize(source, position, 1, position + 1)
        assert found is not None, f"não reconheceu {source[position]!r} em {position}"
        tok, consumed = found
        result.append((tok["type"], tok["value"]))
        position += consumed
    return result


def test_consumed_walks_through_all_symbols():
    source = ">= == != <= && || ! ( ) { } ; , // fim\n+ - * / % = > <"
    assert scan_symbols(source) == [
        (OPERATOR, ">="), (OPERATOR, "=="), (OPERATOR, "!="), (OPERATOR, "<="),
        (OPERATOR, "&&"), (OPERATOR, "||"), (OPERATOR, "!"),
        (DELIMITER, "("), (DELIMITER, ")"), (DELIMITER, "{"), (DELIMITER, "}"),
        (DELIMITER, ";"), (DELIMITER, ","),
        (COMMENT, "// fim"),
        (OPERATOR, "+"), (OPERATOR, "-"), (OPERATOR, "*"), (OPERATOR, "/"),
        (OPERATOR, "%"), (OPERATOR, "="), (OPERATOR, ">"), (OPERATOR, "<"),
    ]


def test_glued_operators_are_split_correctly():
    assert scan_symbols(">=<=!==") == [
        (OPERATOR, ">="), (OPERATOR, "<="), (OPERATOR, "!="), (OPERATOR, "="),
    ]