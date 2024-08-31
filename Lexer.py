from keyword import kwlist, softkwlist

# Listar todas las funciones y objetos incorporados
# print(dir(builtins))


class TokenType:
    IDENTIFIER = "IDENTIFIER"
    PRINT = "print"
    STRING = "STRING"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    WHITESPACE = "WHITESPACE"
    UNKNOWN = "UNKNOWN"


class Symbols:
    TK_SUM = "+"
    TK_SUBST = "-"
    TK_MULT = "*"
    TK_DIV = "/"
    TK_MOD = "%"
    TK_ASSIGN = "="
    TK_EQUAL = "=="
    TK_NOT_EQUAL = "!="
    TK_GREATER = ">"
    TK_LESS = "<"
    TK_GREATER_EQUAL = ">="
    TK_LESS_EQUAL = "<="
    TK_AND = "and"
    TK_OR = "or"
    TK_NOT = "not"
    TK_TRUE = "True"
    TK_FALSE = "False"
    TK_NONE = "None"
    TK_IF = "if"
    TK_ELSE = "else"
    TK_EXCLAMATION = "!"


class ReservedWordToken:
    def __init__(self, value, line, starting_position):
        self.value = value
        self.line = line
        self.starting_position = starting_position

    def __repr__(self):
        return f"<{self.value},{self.line},{self.starting_position}>"


class TokenIdentifier:
    def __init__(self, token_type: TokenType, value, line, starting_position):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.starting_position = starting_position

    def __repr__(self):
        return f"<{self.token_type},{self.value},{self.line},{self.starting_position}>"


def is_identifier_char(c):
    return c.isalnum() or c == "_"


def is_whitespace(c):
    return c.isspace()


def is_quote(c):
    return c == '"'


def is_paren(c):
    return c in "()"


class Lexer:
    def __init__(self, lines):
        self.lines = lines
        self.tokens = []
        self.space = " "
        self.keywords = kwlist
        self.soft_keywords = softkwlist

    def tokenize(self):
        for line in self.lines:
            length = len(line)
            position = 0
            while position < length:
                char = line[position]
                if char.isalpha() or char == "_":
                    start = position
                    while position < length and is_identifier_char(line[position]):
                        position += 1
                    if line[start:position] in self.keywords:
                        self.tokens.append(
                            ReservedWordToken(
                                value=line[start:position],
                                line=self.lines.index(line) + 1,
                                starting_position=start,
                            )
                        )
                    self.tokens.append(
                        TokenIdentifier(
                            TokenType.IDENTIFIER,
                            line[start:position],
                            self.lines.index(line) + 1,
                            start,
                        )
                    )
                elif is_quote(char):
                    # State: Identifying a string literal
                    start = position
                    position += 1
                    while position < length and not is_quote(line[position]):
                        position += 1
                    if position < length:
                        position += 1  # Skip the closing quote
                        self.tokens.append(
                            TokenIdentifier(
                                TokenType.STRING,
                                line[start:position],
                                self.lines.index(line) + 1,
                                start,
                            )
                        )
                    else:
                        raise RuntimeError("Unterminated string literal")

                elif is_paren(char):
                    if char == "(":
                        self.tokens.append(
                            TokenIdentifier(
                                TokenType.LPAREN,
                                char,
                                self.lines.index(line) + 1,
                                position,
                            )
                        )
                    else:
                        self.tokens.append(
                            TokenIdentifier(
                                TokenType.RPAREN,
                                char,
                                self.lines.index(line) + 1,
                                position,
                            )
                        )
                    position += 1

                elif is_whitespace(char):
                    start = position
                    while position < length and is_whitespace(line[position]):
                        position += 1
                    self.tokens.append(
                        TokenIdentifier(
                            TokenType.WHITESPACE,
                            line[start:position],
                            self.lines.index(line) + 1,
                            start,
                        )
                    )

                else:
                    self.tokens.append(
                        TokenIdentifier(
                            TokenType.UNKNOWN,
                            char,
                            self.lines.index(line) + 1,
                            position,
                        )
                    )
                    position += 1

            return self.tokens

    # temp_string = ""
    # for char in chars:
    #     if char is self.space:
    #         self.tokens.append(temp_string)
    #         temp_string = ""
    #     else:
    #         temp_string += char
    # self.tokens.append(temp_string)
    # print(self.tokens)
