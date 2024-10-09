"""
Module for class Parser and its utilities
"""
from enum import Enum
from time import sleep
"""
Identificadores
Palabras clave (keywords)
Literales (constantes)
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

LEX_KEYWORDS = (
    'char', 'double', 'enum', 'float', 'int', 'long', 'short', 'signed',
    'struct', 'union', 'unsigned', 'void', 'auto', 'break', 'case',
    'continue', 'default', 'do', 'else', 'for', 'goto', 'if', 'return',
    'switch', 'while'
)


class TokenType(Enum):
    ID = 1,
    KEYWORD = 2,
    CONST = 3,
    OPERATOR = 4,
    DELIMITER = 5,
    INVALID = 6

class Token:
    def __init__(self):
        self._components = {
            'type': TokenType,
            'lexeme': '',
            'valid': False
        }

    @property
    def t_type(self):
        return self._components['type']

    @property
    def lexeme(self):
        return self._components['lexeme']

    @property
    def is_valid(self):
        return self._components['valid']

    def tokenize(self, word: str) -> str:
        word = word.lstrip()
        word, lexeme = self.get_next_char(word)
        is_slash = lexeme == '/'

        while is_slash:
            if not Token.peek(word, '/') and\
               not Token.peek(word, '*'):
                is_slash = False
            else:
                if Token.peek(word, '/'):
                    word = self.consume_till(word, '\n')
                elif Token.peek(word, '*'):
                    while not Token.peek(word, '/'):
                        word = self.consume_till(word, '*')
                    word = self.consume_char(word)
                word = word.lstrip()
                word, lexeme = self.get_next_char(word)

        if lexeme in LEX_DELIMITERS:
            self.set_token(lexeme, TokenType.DELIMITER)
        elif lexeme in LEX_OPERATOR:
            if lexeme in ('-', '+'):
                if Token.peek(word, '-') or\
                   Token.peek(word, '+') or\
                   Token.peek(word, '='):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)

                else:
                    self.set_token(lexeme, TokenType.OPERATOR)

            elif lexeme == '=':
                if Token.peek(word, '='):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                else:
                    self.set_token(lexeme, TokenType.OPERATOR)

            elif lexeme in ('<', '>'):
                if Token.peek(word, '='):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                elif lexeme == '<' and Token.peek(word, '<'):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                elif lexeme == '>' and Token.peek(word, '>'):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                else:
                    self.set_token(lexeme, TokenType.OPERATOR)

            elif lexeme == '!':
                if Token.peek(word, '='):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                else:
                    self.set_token(lexeme, TokenType.OPERATOR)

            elif lexeme == '&':
                if Token.peek(word, '&'):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                else:
                    self.set_token(lexeme, TokenType.OPERATOR)

            elif lexeme == '|':
                if Token.peek(word, '|'):
                    word = self.set_next_char(word, lexeme, TokenType.OPERATOR)
                else:
                    self.set_token(lexeme, TokenType.OPERATOR)
            else:
                self.set_token(lexeme, TokenType.OPERATOR)
        elif lexeme == '"':
            word, lexeme = self.get_next_char(word)
            word, buffer = self.get_till(word, '"')
            lexeme += buffer
            self.set_token(lexeme, TokenType.CONST)
        else:
            if lexeme.isalpha():
                word, buffer = self.get_if(word,
                                      lambda word: word[0].isalnum() or\
                                                 Token.peek(word, '_'))
                lexeme += buffer
                if lexeme in LEX_KEYWORDS:
                    self.set_token(lexeme, TokenType.KEYWORD)
                else:
                    self.set_token(lexeme, TokenType.ID)

            elif lexeme == '_':
                word, buffer = self.get_if(word,
                                      lambda word: word[0].isalnum() or\
                                                 word[0]  == '_')
                lexeme += buffer
                self.set_token(lexeme, TokenType.ID)

            elif lexeme.isdigit():
                word, buffer = self.get_if(word, lambda word: word[0].isalnum())
                lexeme += buffer
                if lexeme.isdigit():
                    self.set_token(lexeme, TokenType.CONST)
                else:
                    self.set_token(lexeme, TokenType.INVALID, is_valid=False)

        return word

    @staticmethod
    def is_empty(word):
        return '' == word

    @staticmethod
    def peek(word, chr_exp):
        return not Token.is_empty(word) and word[0] == chr_exp

    def set_next_char(self, word, lexeme, t_type):
        lexeme += word[0]
        self.set_token(lexeme, t_type)

        return word[1:]

    def consume_char(self, word):
        if len(word) > 1:
            return word[1:]
        return ''

    def get_next_char(self, word):
        buffer = ''
        if len(word) > 0:
            buffer = word[0]
            word = word[1:]
        return word, buffer

    def get_till(self, word, delimiter):
        buffer = ''
        while not Token.peek(word, delimiter):
            word, cur_char = self.get_next_char(word)
            buffer += cur_char

        word = word[1:]
        return word, buffer


    def consume_till(self, word: str, delimiter):
        while not Token.peek(word, delimiter):
            word = self.consume_char(word)

        word = word[1:]
        return word

    def get_if(self, word, condition):
        buffer = ''
        while condition(word):
            word, cur_char = self.get_next_char(word)
            buffer += cur_char
        return word, buffer

    def set_token(self, lexeme, t_type, is_valid=True):
        self._components['valid'] = is_valid
        self._components['lexeme'] = lexeme
        self._components['type'] = t_type

    def __str__(self):
        return f'Lex: {self.lexeme} TokenType: {self.t_type} IsValid:{self.is_valid}'

class Parser():
    def __init__(self, code_str):
        self._components = {
            'token_list': [],
            'code_str': code_str,
            'copy_cstr': str(code_str)
        }

    def scan(self):
        while self.copy_cstr:
            new_token = Token()
            self.copy_cstr = new_token.tokenize(self.copy_cstr)
            self.token_list.append(new_token)

    @property
    def copy_cstr(self):
        return self._components['copy_cstr']

    @copy_cstr.setter
    def copy_cstr(self, new_str):
        if isinstance(new_str, str):
            self._components['copy_cstr'] = new_str

    @property
    def token_list(self) -> list:
        return self._components['token_list']

    def parse(self) -> bool:
        return False


if __name__ == "__main__":
    file_str = open("example.c", "r", encoding='utf-8')
    file_str = file_str.read().rstrip()
    parser = Parser(file_str)
    parser.scan()
    for token in parser.token_list:
        print(token)
