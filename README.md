# Jalan — Analisador Léxico

Projeto acadêmico de Linguagens Formais e Autômatos Finitos: implementação de um analisador léxico para a linguagem fictícia Jalan.

## Objetivo

Ler um código-fonte Jalan e reconhecer sua sequência de tokens. Este projeto **não** implementa um parser nem valida a estrutura sintática completa dos programas.

## Sintaxe inicial da Jalan

```jalan
string nome = "Pedro";
int idade = 22;
double altura = 1.75;
bool estudante = true;

show("Olá, " + nome);

if (idade >= 18) {
    show("Maior de idade");
} else {
    show("Menor de idade");
}
```

## Categorias de tokens

- **Tipos:** `int`, `double`, `string`, `bool`
- **Controle:** `if`, `else`, `while`, `for`
- **Funções/palavras reservadas:** `function`, `return`, `show`
- **Booleanos:** `true`, `false`
- **Identificadores:** nomes iniciados por letra ou `_`, seguidos por letras, números ou `_`
- **Literais:** inteiros, decimais e strings entre aspas duplas
- **Operadores:** `+ - * / % = == != > < >= <= && || !`
- **Delimitadores:** `; ( ) { } ,`
- **Comentários:** `//` até o fim da linha

Espaços em branco e quebras de linha são ignorados entre tokens. O sinal `-` é reconhecido como operador separado, inclusive antes de um número.

## Estrutura

```text
Jalan/
├── src/
│   ├── main.py
│   ├── lexer.py
│   ├── identifiers.py
│   ├── literals.py
│   └── symbols.py
├── tests/
│   ├── test_identifiers.py
│   ├── test_literals.py
│   └── test_symbols.py
└── docs/
    ├── report/
    ├── slides/
    └── diagrams/
```

## Contrato entre os módulos

Para facilitar a integração, cada reconhecedor recebe o texto e a posição atual e retorna:

- um dicionário de token, se reconhecer algo naquela posição; ou
- `None`, se não reconhecer.

Formato padrão do token:

```python
{
    "type": "IDENTIFIER",
    "value": "idade",
    "line": 1,
    "column": 5
}
```

O reconhecedor também deve informar quantos caracteres consumiu. A interface sugerida é:

```python
recognize(source: str, position: int, line: int, column: int)
# Retorno: (token, consumed) ou None
```

**Importante:** conversem antes de implementar para manter exatamente essa interface e os nomes dos tipos de token.

## Como executar

Na raiz do projeto:

```bash
python src/main.py
```

Os módulos ainda serão implementados pelos integrantes. Por enquanto, este repositório é o ponto de partida e o contrato de integração.

## Divisão de trabalho

- João Victor: `identifiers.py` — identificadores e palavras reservadas.
- Paulista: `literals.py` — números, strings e booleanos.
- Paulo: `symbols.py` — operadores, delimitadores e comentários.
- Carlysson: `lexer.py` e `main.py` — varredura, integração e tratamento de erros léxicos.

Cada integrante também documenta os AFDs de sua categoria e prepara os testes correspondentes.
