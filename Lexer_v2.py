from keyword import softkwlist
from utils import KEYWORDS, SYMBOLS 

class TokenType:
    IDENTIFIER = "id"
    PRINT = "print"
    STRING = "tk_cadena"
    NUMBER = "tk_numero"
    LPAREN = "tk_paren_izq"
    RPAREN = "tk_paren_der"
    COLON = "tk_dos_puntos"
    COMMA = "tk_coma"
    WHITESPACE = "WHITESPACE"
    UNKNOWN = "UNKNOWN"
    ASSIGN = "tk_asignacion"
    IF = "if"
    ELSE = "else"






class Token:
    def __init__(self, token_type, value, line, starting_position):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.starting_position = starting_position

    def __repr__(self):
        return f"<{self.token_type},{self.value},{self.line},{self.starting_position}>"


class LexicalError(Exception):
    def __init__(self, line, position):
        self.line = line
        self.position = position


class TokenizerV2:
    def __init__(self, lines):
        self.lines = lines
        self.tokens = []

    def tokenize(self):
        for line_num, line in enumerate(self.lines, start=1):
            length = len(line)
            position = 0
            while position < length:
                char = line[position]
                if char.isalpha() or char == "_":
                    start = position
                    while position < length and (line[position].isalnum() or line[position] == "_"):
                        position += 1
                    value = line[start:position]
                    token_type = TokenType.IDENTIFIER if value not in KEYWORDS else value
                    self.tokens.append(Token(token_type, value, line_num, start + 1))
                elif char.isspace():
                    position += 1
                elif char == '"':
                    start = position
                    position += 1
                    while position < length and line[position] != '"':
                        position += 1
                    position += 1  # Skip closing quote
                    self.tokens.append(Token(TokenType.STRING, line[start:position], line_num, start + 1))
                elif char in SYMBOLS:
                    self.tokens.append(Token(SYMBOLS[char], char, line_num, position + 1))
                    position += 1
                else:
                    raise LexicalError(line_num, position + 1)

        return self.tokens
