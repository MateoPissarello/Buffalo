from enum import Enum


class TokenType(Enum):
    IDENTIFIER = 1
    KEYWORD = 2
    ADD = 3
    SUBTRACT = 4
    MULTIPLY = 5
    DIVIDE = 6
    ASSIGN = 7
    EQUAL = 8
    NOT_EQUAL = 9
    LESS = 10
    GREATER = 11
    LESS_EQUAL = 12
    GREATER_EQUAL = 13
    LPAREN = 14
    RPAREN = 15
    LBRACE = 16
    RBRACE = 17
    LBRACKET = 18
    RBRACKET = 19
    COMMA = 20
    COLON = 21
    PRINT = 22
    # Agrega otros tipos de token según sea necesario
