"""Ponto de entrada do analisador léxico Jalan."""

from lexer import tokenize


def main():
    source = """\
string nome = "Pedro";
int idade = 22;
show("Olá, " + nome);
"""
    for token in tokenize(source):
        print(token)


if __name__ == "__main__":
    main()
