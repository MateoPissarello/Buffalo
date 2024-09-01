from keyword import softkwlist
from utils import KEYWORDS
from utils import SYMBOLS


class LexicalError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TokenType:
    IDENTIFIER = "id"
    PRINT = "print"
    STRING = "tk_cadena"
    LPAREN = "tk_paren_izq"
    RPAREN = "tk_paren_der"
    COLON = "tk_dos_puntos"
    LBRACE = "tk_llave_izq"
    RBRACE = "tk_llave_der"
    SUM = "tk_suma"
    ASSIGN = "tk_asignacion"
    EQUAL = "tk_igual"
    COMMA = "tk_coma"
    WHITESPACE = "WHITESPACE"
    UNKNOWN = "UNKNOWN"


# class Symbols:
#     TK_SUM = "+"
#     TK_SUBST = "-"
#     TK_MULT = "*"
#     TK_DIV = "/"
#     TK_MOD = "%"
#     TK_ASSIGN = "="
#     TK_EQUAL = "=="
#     TK_NOT_EQUAL = "!="
#     TK_GREATER = ">"
#     TK_LESS = "<"
#     TK_GREATER_EQUAL = ">="
#     TK_LESS_EQUAL = "<="
#     TK_AND = "and"
#     TK_OR = "or"
#     TK_NOT = "not"
#     TK_TRUE = "True"
#     TK_FALSE = "False"
#     TK_NONE = "None"
#     TK_IF = "if"
#     TK_ELSE = "else"
#     TK_EXCLAMATION = "!"


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


class TokenSymbol:
    def __init__(self, value, line, starting_position):
        self.value = value
        self.line = line
        self.starting_position = starting_position

    def __repr__(self):
        return f"<{self.value},{self.line},{self.starting_position}>"


def is_identifier_char(c):
    return c.isalnum() or c == "_"


def is_symbol(c):
    return c in SYMBOLS


def is_number(c):
    return c.isdigit()


def is_whitespace(c):
    return c.isspace()


def is_quote(c):
    return c == '"'


def is_paren(c):
    return c in "()"


def is_colon(c):
    return c == ":"


def is_hash(c):
    return c == "#"


def is_hyphen(c):
    return c == "-"


class Lexer:
    def __init__(self, lines):
        self.lines = lines
        self.tokens = []
        self.space = " "
        self.keywords = KEYWORDS
        self.soft_keywords = softkwlist

    def tokenize(self):
        for line in self.lines:
            length = len(line)
            position = 0
            while position < length:
                char = line[position]

                if self.is_identifier_start(char):
                    position = self.handle_identifier(line, position)
                elif is_symbol(char):
                    position = self.handle_symbol(line, position)
                elif is_quote(char):
                    position = self.handle_string_literal(line, position)
                elif is_paren(char):
                    position = self.handle_parenthesis(char, line, position)
                elif is_whitespace(char):
                    position = self.skip_whitespace(line, position)
                elif is_colon(char):
                    position = self.handle_colon(line, position)
                elif is_hash(char):
                    position = self.skip_comentary(line, position)
                # elif is_number(char):
                #     position = self.handle_number(line, position)
                else:
                    self.raise_lexical_error(line, position)

        return self.tokens

    #           if position < length:
    #             position += 1  # Saltar la comilla de cierre
    #             self.tokens.append(
    #                 TokenIdentifier(
    #                     token_type=TokenType.STRING,
    #                     value=line[start:position],
    #                     line=self.lines.index(line) + 1,
    #                     starting_position=start,
    #                 )
    #             )
    #         else:
    #             self.raise_lexical_error(
    #                 line, position - 1
    #             )  # Se resta menos uno para quitar el \n
    #         return position
    # def handle_number(self, line, position):
    #     start = position
    #     length = len(line)
    #     while position < length and is_number(line[position]):
    #         position += 1
    #     if line[]

    def skip_comentary(self, line, position):
        length = len(line)
        while position < length:
            position += 1
        return position

    def handle_symbol(self, line, position):
        char = line[position]
        if char == "=":
            if line[position + 1] == "=":
                self.tokens.append(
                    TokenSymbol(
                        value=TokenType.EQUAL,
                        line=self.lines.index(line) + 1,
                        starting_position=position + 1,
                    )
                )
                return position + 2
            else:
                self.tokens.append(
                    TokenSymbol(
                        value=TokenType.ASSIGN,
                        line=self.lines.index(line) + 1,
                        starting_position=position + 1,
                    )
                )
                return position + 1
        elif char == "+":
            self.tokens.append(
                TokenSymbol(
                    value=TokenType.SUM,
                    line=self.lines.index(line) + 1,
                    starting_position=position + 1,
                )
            )
            return position + 1
        elif char == ",":  # Coma
            self.tokens.append(
                TokenSymbol(
                    value=TokenType.COMMA,
                    line=self.lines.index(line) + 1,
                    starting_position=position + 1,
                )
            )
            return position + 1

    def is_identifier_start(self, char):
        return char.isalnum() or char == "_"

    def handle_identifier(self, line, position):
        start = position
        length = len(line)
        if is_number(line[position]):
            self.raise_lexical_error(line, position)
        while position < length and is_identifier_char(line[position]):
            position += 1
        value = line[start:position]
        if value in self.keywords:
            self.tokens.append(
                ReservedWordToken(
                    value=value,
                    line=self.lines.index(line) + 1,
                    starting_position=start + 1,
                )
            )
        else:
            self.tokens.append(
                TokenIdentifier(
                    token_type=TokenType.IDENTIFIER,
                    value=value,
                    line=self.lines.index(line) + 1,
                    starting_position=start + 1,
                )
            )
        return position

    def handle_string_literal(self, line, position):
        start = position
        position += 1
        length = len(line)
        while position < length and not is_quote(line[position]):
            position += 1
        if position < length:
            position += 1  # Saltar la comilla de cierre
            self.tokens.append(
                TokenIdentifier(
                    token_type=TokenType.STRING,
                    value=line[start:position],
                    line=self.lines.index(line) + 1,
                    starting_position=start,
                )
            )
        else:
            self.raise_lexical_error(
                line, position - 1
            )  # Se resta menos uno para quitar el \n
        return position

    def handle_parenthesis(self, char, line, position):
        token_type = TokenType.LPAREN if char == "(" else TokenType.RPAREN
        self.tokens.append(
            TokenSymbol(
                value=token_type,
                line=self.lines.index(line) + 1,
                starting_position=position + 1,
            )
        )
        return position + 1

    def skip_whitespace(self, line, position):
        length = len(line)
        while position < length and is_whitespace(line[position]):
            position += 1
        return position

    def handle_colon(self, line, position):
        self.tokens.append(
            TokenSymbol(
                value=TokenType.COLON,
                line=self.lines.index(line) + 1,
                starting_position=position + 1,
            )
        )
        return position + 1

    def raise_lexical_error(self, line, position):
        raise LexicalError(
            f">>> Error Léxico (line: {self.lines.index(line) + 1}, posicion: {position + 1})"
        )


def token_to_string(self):
    """
    Convert tokens to a string representation for writing to a file.
    """
    result = []
    for token in self.tokens:
        result.append(str(token))
