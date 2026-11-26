
import pytest

from src.lexer import tokenize, LexicalError


def test_deve_tokenizar_programa_completo():
    source = '''
string nome = "Pedro";
int idade = 22;
bool ativo = true;
show(nome);
'''

    tokens = tokenize(source)

    values = [token["value"] for token in tokens]

    assert "string" in values
    assert "nome" in values
    assert '"Pedro"' in values
    assert "22" in values
    assert "true" in values
    assert "show" in values


def test_deve_preservar_linha_e_coluna():
    source = "int idade = 22;\nshow(idade);"

    tokens = tokenize(source)

    assert tokens[0]["line"] == 1
    assert tokens[0]["column"] == 1

    show_token = next(t for t in tokens if t["value"] == "show")

    assert show_token["line"] == 2
    assert show_token["column"] == 1


def test_deve_reconhecer_comentario():
    source = "int idade = 22; // idade do usuario"

    tokens = tokenize(source)

    comment = tokens[-1]

    assert comment["type"] == "COMMENT"
    assert comment["value"] == "// idade do usuario"


def test_deve_gerar_erro_para_caractere_invalido():
    source = "int idade = 22 @"

    with pytest.raises(LexicalError):
        tokenize(source)


def test_deve_gerar_erro_com_linha_e_coluna():
    source = "int idade = 22;\n@"

    with pytest.raises(LexicalError) as error:
        tokenize(source)

    assert error.value.line == 2
    assert error.value.column == 1
