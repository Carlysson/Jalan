import pytest

from src.identifiers import recognize


@pytest.mark.parametrize("source",["abc", "_x", "x1", "_a_1", "ifx", "Whilex"])
def test_deve_reconhecer_identificadores(source):
    result = recognize(source, 0, 1, 1)

    assert result is not None

    token, consumed = result

    assert token ["type"] == "IDENTIFIER"
    assert token ["value"] == source
    assert consumed == len(source)


@pytest.mark.parametrize("source", [
    "int", "double", "string", "bool", "if", "else",
    "while", "for", "function", "return", "show",
])
def test_deve_reconhecer_palavras_reservadas(source):
    result = recognize(source, 0, 1, 1)

    assert result is not None

    token, consumed = result

    assert token ["type"] == "KEYWORD"
    assert token ["value"] == source
    assert consumed == len(source)


@pytest.mark.parametrize("source", ["1abc", "+x", " x", ""])
def test_nao_deve_reconhecer(source):
    assert recognize(source, 0, 1, 1) is None


def test_deve_parar_antes_de_um_operador():
    token, consumed = recognize("abc+1", 0, 1, 1)

    assert token ["value"] == "abc"
    assert consumed == 3


def test_deve_reconhecer_no_meio_do_texto():
    token, consumed = recognize("a + bcd", 4, 1, 5)

    assert token["value"] == "bcd"
    assert token["column"] == 5


def test_deve_retornar_none_quando_posicao_estiver_no_final():
    assert recognize("abc", 3, 1, 4) is None


def test_deve_preservar_linha_e_coluna():
    token, _= recognize("abc", 0, 4, 8)

    assert token ["line"] == 4
    assert token ["column"] == 8


@pytest.mark.parametrize("source", ["true", "false"])
def test_nao_deve_reconhecer_booleanos(source):
    assert recognize(source, 0, 1, 1) is None


@pytest.mark.parametrize("source", ["trueish", "false1", "_true", "True"])
def test_deve_reconhecer_como_identificador_se_nao_for_booleano_exato(source):
    token, consumed = recognize(source, 0, 1, 1)

    assert token["type"] == "IDENTIFIER"
    assert consumed == len(source)


@pytest.mark.parametrize("source", ["If", "WHILE", "Show"])
def test_palavra_reservada_maiuscula_e_identificador(source):
    token, _ = recognize(source, 0, 1, 1)
    assert token["type"] == "IDENTIFIER"


def test_deve_parar_antes_de_parenteses():
    token, consumed = recognize("show(x)", 0, 1, 1)
    assert token["type"] == "KEYWORD"
    assert consumed == 4


def test_deve_parar_antes_de_quebra_de_linha():
    token, consumed = recognize("abc\ndef", 0, 1, 1)
    assert token["value"] == "abc"
    assert consumed == 3
