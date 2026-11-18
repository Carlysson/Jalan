"""Testes do reconhecedor de literais (a implementar)."""


import pytest
from src.literals import recognize



# INTEIROS


@pytest.mark.parametrize("source", [
    "0",
    "7",
    "123",
    "2026",
])
def test_deve_reconhecer_inteiros(source):
    result = recognize(source, 0, 1, 1)

    assert result is not None

    token, consumed = result

    assert token["type"] == "INTEGER_LITERAL"
    assert token["value"] == source
    assert consumed == len(source)


@pytest.mark.parametrize("source", [
    "12abc",
    "123_",
    "12.5.6",
    "12.",
])
def test_nao_deve_reconhecer_inteiros_invalidos(source):
    assert recognize(source, 0, 1, 1) is None


def test_inteiro_deve_parar_antes_de_um_delimitador():
    result = recognize("123;", 0, 1, 1)

    assert result is not None

    token, consumed = result

    assert token["value"] == "123"
    assert consumed == 3



# DECIMAIS


@pytest.mark.parametrize("source", [
    "1.5",
    "0.25",
    "10.75",
    "123.456",
])
def test_deve_reconhecer_decimais(source):
    result = recognize(source, 0, 1, 1)

    assert result is not None

    token, consumed = result

    assert token["type"] == "DECIMAL_LITERAL"
    assert token["value"] == source
    assert consumed == len(source)


@pytest.mark.parametrize("source", [
    "10.",
    ".50",
    "12.5.6",
    "12.5abc",
    "12.a",
])
def test_nao_deve_reconhecer_decimais_invalidos(source):
    assert recognize(source, 0, 1, 1) is None


def test_decimal_deve_parar_antes_de_um_operador():
    result = recognize("12.5+", 0, 1, 1)

    assert result is not None

    token, consumed = result

    assert token["value"] == "12.5"
    assert consumed == 4



# STRINGS


@pytest.mark.parametrize("source", [
    '"Olá mundo"',
    '""',
    '"Jalan"',
    '"Texto 123"',
    '"Linha\\nNova"',
    '"Aspas: \\"Olá\\""',
    '"Barra: \\\\"',
    '"Tabulação: \\t"',
    '"Retorno: \\r"',
])
def test_deve_reconhecer_strings(source):
    result = recognize(source, 0, 1, 1)

    assert result is not None

    token, consumed = result

    assert token["type"] == "STRING_LITERAL"
    assert token["value"] == source
    assert consumed == len(source)


@pytest.mark.parametrize("source", [
    '"String sem fechamento',
    '"Escape invalido: \\x"',
    '"String com quebra\n de linha"',
    '"Escape incompleto: ' + "\\",
])
def test_nao_deve_reconhecer_strings_invalidas(source):
    assert recognize(source, 0, 1, 1) is None



# Teste dos booleanos


@pytest.mark.parametrize("source", [
    "true",
    "false",
])
def test_deve_reconhecer_booleanos(source):
    result = recognize(source, 0, 1, 1)

    assert result is not None

    token, consumed = result

    assert token["type"] == "BOOLEAN_LITERAL"
    assert token["value"] == source
    assert consumed == len(source)


@pytest.mark.parametrize("source, expected", [
    ("true;", "true"),
    ("false)", "false"),
    ("true+", "true"),
])
def test_booleano_deve_parar_antes_de_outro_token(source, expected):
    result = recognize(source, 0, 1, 1)

    assert result is not None

    token, consumed = result

    assert token["value"] == expected
    assert consumed == len(expected)


@pytest.mark.parametrize("source", [
    "trueValue",
    "false123",
    "true_false",
    "falseABC",
    "tru",
    "fals",
])
def test_nao_deve_reconhecer_booleanos_invalidos(source):
    assert recognize(source, 0, 1, 1) is None



# POSIÇÃO E METADADOS


def test_deve_retornar_none_quando_posicao_estiver_no_final():
    assert recognize("123", 3, 1, 4) is None


def test_deve_retornar_none_para_posicao_negativa():
    assert recognize("123", -1, 1, 1) is None


def test_deve_preservar_linha_e_coluna():
    result = recognize("123", 0, 4, 8)

    assert result is not None

    token, consumed = result

    assert token["line"] == 4
    assert token["column"] == 8
