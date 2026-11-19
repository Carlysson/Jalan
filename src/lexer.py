"""Integra os reconhecedores e percorre o código-fonte."""


def tokenize(source: str) -> list[dict]:
    """Converte o código-fonte Jalan em uma lista de tokens.

    TODO:
    1. Percorrer source da esquerda para a direita.
    2. Ignorar espaços e atualizar linha/coluna.
    3. Tentar os reconhecedores de identifiers, literals e symbols.
    4. Avançar pela quantidade de caracteres consumidos.
    5. Gerar erro léxico quando nenhum reconhecedor aceitar a posição.
    """
    raise NotImplementedError("O scanner será implementado na etapa de integração.")
