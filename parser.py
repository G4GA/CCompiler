"""
Module for class Parser and its utilities
"""
from enum import Enum

"""
Identificadores
Palabras clave (keywords)
Literales (constantes)
Operadores
Separadores (delimitadores, como paréntesis, llaves, comas, punto y coma)
Comentarios
"""

class TokenType(Enum):
    ID = 1,
    KEYWORD = 2,
    CONST = 3,
    OPERATOR = 4,
    DELIMITER = 5,

class Token():
    def __init__(self, word)
        self._components = {
            'type': TokenType,
            'lexeme': str,
        }
        self.tokenize(word)

    @property
    def t_type(self):
        return self._components['type']

    @property
    def lexeme(self):
        return self._components['lexeme']

    def tokenize(self, word: str) -> str:
        return ''


class Parser():
    def __init__(self, code_str):
        self._components = {
            'token_list': [],
            'code_str': code_str
        }

    @property
    def token_list(self) -> list:
        return self._components['token_list']

    def parse(self) -> bool:
        return False
