"""Testes do reconhecedor de símbolos (a implementar)."""

import os
import sys

import pytest

# Faz o Python achar symbols.py dento de src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from symbols import recognize

#TIDO: combinar com o grupo os nomes dos tipos de token
#ex: "DELIMITER", "OPERATOR", "COMMENT". e usar nos asserts

#Delimitadores
#Usar @pyntest.mark.parmetriz com os delimitadores

def test_delimiter(delimiter):
    #esperado: token do tipo, value, line, column corretos e consumed = ?

    pass

# Operadores de1 carctere
def test_one_char_operator(operator):
    #esperado: token do tipo, value, line, column corretos e consumed = ?
    pass

#operadores de 2 caracteres
def test_two_char_operator(operator):
    pass

#maior união
def test_operator_union():
    #ex: ">=" deve ser reconhecido como operador de 2 caracteres, não como ">" e "="
    pass

#comentários
def test_comment():
    pass

def test_comment_at_end_of_line():
    pass

def test_comment_without_a_line_break_at_the_end():
    pass

def test_standalone_slash_and_operator():
    pass

#Casos especiais
def test_minus_sing_before_number():
    #ex: "-1" deve ser reconhecido como operador "-" e número "1", não como um token só
    pass

def test_row_and_column_in_middle_position():
    #ex: "a + b" deve retornar token "+" com line=1 e column=3
    pass

#Oque não reconhece (deve retornar nome)
def test_not_recognized():
    #ex: "&" não é reconhecido como símbolo, deve retornar None
    pass

def test_end_of_text():
    pass