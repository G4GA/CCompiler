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

LEX_DELIMITERS = ('(', ')',
                  '{', '}',
                  '[', ']',
                  ';', ',',
                  '.', ':')
LEX_OPERATOR = (
    '+', '-', '*', '/', '%',
    '=', '>', '<', '!',
    '&', '|',
)


class TokenType(Enum):
    ID = 1,
    KEYWORD = 2,
    CONST = 3,
    OPERATOR = 4,
    DELIMITER = 5,

class Token:
    def __init__(self):
        self._components = {
            'type': TokenType,
            'lexeme': '',
            'done': False
        }

    @property
    def t_type(self):
        return self._components['type']

    @property
    def lexeme(self):
        return self._components['lexeme']

    @property
    def done(self):
        return self._components['done']

    def tokenize(self, word: str) -> str:
        lexeme = ''
        if not self.is_empty(word):
            lexeme= word[0]
        if len(word) > 1:
            word = word[1:]
        else:
            word = ''

        if lexeme in LEX_DELIMITERS:
            self.set_cur_char(lexeme, TokenType.DELIMITER)
        elif lexeme in LEX_OPERATOR:
            if lexeme in ('-', '+'):
                if Token.peek(word, '-') or\
                   Token.peek(word, '+') or\
                   Token.peek(word, '='):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)

                else:
                    self.set_cur_char(lexeme, TokenType.OPERATOR)

            elif lexeme == '=':
                if Token.peek(word, '='):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                else:
                    self.set_cur_char(lexeme, TokenType.OPERATOR)

            elif lexeme in ('<', '>'):
                if Token.peek(word, '='):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                elif lexeme == '<' and Token.peek(word, '<'):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                elif lexeme == '>' and Token.peek(word, '>'):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                else:
                    self.set_cur_char(lexeme, TokenType.OPERATOR)
            elif lexeme == '/':
                if Token.peek(word, '/'):
                    word = self.consume_till(word, '\n')
                else:
                    self.set_cur_char(lexeme, TokenType.OPERATOR)
            elif lexeme == '!':
                if Token.peek(word, '='):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                else:
                    self.set_cur_char(lexeme, TokenType.OPERATOR)
            elif lexeme == '&':
                if Token.peek(word, '&'):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                else:
                    self.set_cur_char(lexeme, TokenType.OPERATOR)
            elif lexeme == '|':
                if Token.peek(word, '|'):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                else:
                    self.set_cur_char(lexeme, TokenType.OPERATOR)
            else:
                self.set_cur_char(lexeme, TokenType.OPERATOR)
        return word

    @staticmethod
    def is_empty(word):
        return '' == word

    @staticmethod
    def peek(word, chr_exp):
        return not Token.is_empty(word) and word[0] == chr_exp

    def set_next_char(self, word, lexeme, t_type):
        lexeme += word[0]
        self._components['lexeme'] = lexeme
        self._components['type'] = t_type

        return word[1:]

    def consume_char(self, word):
        if len(word) > 1:
            return word[1:]

    def consume_till(self, word: str, delimiter):
        while not Token.peek(word, delimiter):
            word = self.consume_char(word)

        word = word[1:]
        return word

    def set_cur_char(self, lexeme, t_type):
        self._components['lexeme'] = lexeme
        self._components['type'] = t_type

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


if __name__ == "__main__":
    file_str = open("example.c", "r", encoding='utf-8')
    file_str = file_str.read().rstrip()
    tokens = []
    while file_str:
        test_token = Token()
        file_str = test_token.tokenize(file_str)
        if test_token.lexeme:
            print(f'Lexeme: {test_token.lexeme} TokenType: {test_token.t_type}')
