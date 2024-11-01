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
    QUOTE = "tk_comilla"
    WHITESPACE = "WHITESPACE"
    UNKNOWN = "UNKNOWN"
    ASSIGN = "tk_asignacion"
    IF = "if"
    ELSE = "else"
    ELIF = "elif"
    IMPORT = "import"
    FROM = "from"
    DOT = "tk_punto"
    DEF = "def"
    RETURN = "return"
    FOR = "for"
    IN = "in"
    RANGE = "range"
    LBRACE = "tk_llave_izq"
    RBRACE = "tk_llave_der"
    
    @classmethod
    def get_token_name(cls, value):
        for name, val in vars(cls).items():
            if val == value:
                return getattr(cls, name)
        return None  # Devuelve None si no se encuentra el valor


class Detokenizer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.detokenized = []
        self.tokens_map = {
            "tk_suma": "+",
            "tk_resta": "-",
            "tk_mult": "*",
            "tk_div": "/",
            "tk_arroba": "@",
            "tk_mod": "%",
            "tk_coma": ",",
            "tk_flecha": "->",
            "tk_asignacion": "=",
            "tk_igual": "==",
            "tk_diferente": "!=",
            "tk_menor": "<",
            "tk_mayor": ">",
            "tk_corchete_izq": "[",
            "tk_corchete_der": "]",
            "tk_menor_igual": "<=",
            "tk_mayor_igual": ">=",
            "tk_punto": ".",
            "tk_llave_izq": "{",
            "tk_llave_der": "}",
            "tk_comilla": '"',
            "tk_paren_izq": "(",
            "tk_paren_der": ")",
            "tk_dos_puntos": ":",
        }

    def detokenize(self):
        for token in self.tokens:
            val = self.tokens_map.get(token)
            if val is None:
                self.detokenized.append(token)
            else:
                self.detokenized.append(val)


def is_token_comparing_operator(token):
    return token in [
        SymbolsDict["=="],
        SymbolsDict["!="],
        SymbolsDict["<"],
        SymbolsDict[">"],
        SymbolsDict["<="],
        SymbolsDict[">="],
    ]


class LexicalError(Exception):
    def __init__(self, line, position):
        self.line = line
        self.position = position


def obtain_key(val):
    for key, value in SymbolsDict.items():
        if val == value:
            return key
    return None


def is_token_identifier_cls(token):
    return isinstance(token, TokenIdentifier)


def is_token_symbol_cls(token):
    return isinstance(token, TokenSymbol)


def is_token_reserved_word_cls(token):
    return isinstance(token, ReservedWordToken)


def is_comparsion_operator(token):
    return token in ["==", "!=", "<", ">", "<=", ">=", "and", "or", "not", "in", "is"]


SymbolsDict = {
    "+": "tk_suma",
    "-": "tk_resta",
    "*": "tk_mult",
    "/": "tk_div",
    "@": "tk_arroba",
    "%": "tk_mod",
    ",": "tk_coma",
    "->": "tk_flecha",
    "=": "tk_asignacion",
    "==": "tk_igual",
    '"': "tk_comilla",
    "!=": "tk_diferente",
    "<": "tk_menor",
    ">": "tk_mayor",
    "[": "tk_corchete_izq",
    "]": "tk_corchete_der",
    "<=": "tk_menor_igual",
    ">=": "tk_mayor_igual",
    ".": "tk_punto",
    "{": "tk_llave_izq",
    "}": "tk_llave_der",
    ":": "tk_dos_puntos",
}


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


class TokenSymbol:
    def __init__(self, value, line, starting_position):
        self.value = value
        self.symbol = obtain_key(value)
        self.line = line
        self.starting_position = starting_position

    def __repr__(self):
        return f"<{self.value},{self.line},{self.starting_position}>"


def is_identifier_char(c):
    return c.isalnum() or c == "_"


def tk_menor(c):
    return c == "<"


def tk_mayor(c):
    return c == ">"


def is_symbol(c):
    return c in SYMBOLS


def is_number(c):
    return c.isdigit()


def is_whitespace(c):
    return c.isspace()


def is_dot(c):
    return c == "."


def is_arroba(c):
    return c == "@"


def is_square_bracket(c):
    return c in "[]"


def is_dash(c):
    return c == "-"


def is_quote(c):
    return c == '"'


def is_brace(c):
    return c in "{}"


def is_admiracion(c):
    return c == "!"


def is_paren(c):
    return c in "()"


def is_equal(c):
    return c == "="


def is_operation(c):
    return c in "+-*/%"


def is_colon(c):
    return c == ":"


def is_hash(c):
    return c == "#"


def is_comma(c):
    return c == ","


def is_numer(c):
    return c in "0123456789"


class Lexer:
    def __init__(self, lines):
        self.lines = lines
        self.tokens = []
        self.space = " "
        self.keywords = KEYWORDS
        self.soft_keywords = softkwlist

    def tokenize(self):
        try:
            for n_line in range(len(self.lines)):
                line = self.lines[n_line]
                length = len(line)
                position = 0
                while position < length:
                    char = line[position]
                    if char.isalpha() or char == "_":
                        start = position
                        while position < length and is_identifier_char(line[position]):
                            position += 1
                        value = line[start:position]
                        if value in self.keywords:
                            self.tokens.append(
                                ReservedWordToken(
                                    value=value,
                                    line=n_line + 1,
                                    starting_position=start + 1,
                                )
                            )

                        else:
                            self.tokens.append(
                                TokenIdentifier(
                                    token_type=TokenType.IDENTIFIER,
                                    value=line[start:position],
                                    line=n_line + 1,
                                    starting_position=start + 1,
                                )
                            )
                    elif is_hash(char):
                        break

                    elif is_operation(char):
                        self.tokens.append(
                            TokenSymbol(
                                value=SymbolsDict[char],
                                line=n_line + 1,
                                starting_position=position + 1,
                            )
                        )
                        position += 1

                    elif is_square_bracket(char):
                        if char == "[":
                            self.tokens.append(
                                TokenSymbol(
                                    value=SymbolsDict[char],
                                    line=n_line + 1,
                                    starting_position=position + 1,
                                )
                            )
                        else:
                            self.tokens.append(
                                TokenSymbol(
                                    value=SymbolsDict[char],
                                    line=n_line + 1,
                                    starting_position=position + 1,
                                )
                            )
                        position += 1
                    elif is_quote(char):
                        # State: Identifying a string literal
                        self.tokens.append(
                            TokenSymbol(
                                value=SymbolsDict[char],
                                line=n_line + 1,
                                starting_position=position + 1,
                            )
                        )
                        start = position
                        position += 1
                        while position < length and not is_quote(line[position]):
                            position += 1

                        if position < length:
                            position += 1  # Skip the closing quote
                            self.tokens.append(
                                TokenIdentifier(
                                    token_type=TokenType.STRING,
                                    value=line[start:position],
                                    line=n_line + 1,
                                    starting_position=start + 2,
                                )
                            )
                        self.tokens.append(
                            TokenSymbol(
                                value=SymbolsDict['"'],
                                line=n_line + 1,
                                starting_position=position,
                            )
                        )
                        # else:
                        #     raise RuntimeError("Unterminated string literal")

                    elif is_paren(char):
                        if char == "(":
                            self.tokens.append(
                                TokenSymbol(
                                    value=TokenType.LPAREN,
                                    line=n_line + 1,
                                    starting_position=position + 1,
                                )
                            )
                        else:
                            self.tokens.append(
                                TokenSymbol(
                                    value=TokenType.RPAREN,
                                    line=n_line + 1,
                                    starting_position=position + 1,
                                )
                            )
                        position += 1

                    elif is_brace(char):
                        if char == "{":
                            self.tokens.append(
                                TokenSymbol(
                                    value=SymbolsDict[char],
                                    line=n_line + 1,
                                    starting_position=position + 1,
                                )
                            )
                        else:
                            self.tokens.append(
                                TokenSymbol(
                                    value=SymbolsDict[char],
                                    line=n_line + 1,
                                    starting_position=position + 1,
                                )
                            )
                        position += 1

                    elif is_number(char):
                        start = position
                        while position < length and is_number(line[position]):
                            position += 1
                        self.tokens.append(
                            TokenIdentifier(
                                token_type=TokenType.NUMBER,
                                value=line[start:position],
                                line=n_line + 1,
                                starting_position=start + 1,
                            )
                        )

                    elif is_dot(char):
                        self.tokens.append(
                            TokenSymbol(
                                value=SymbolsDict[char],
                                line=n_line + 1,
                                starting_position=position + 1,
                            )
                        )
                        position += 1

                    elif is_whitespace(char):
                        start = position
                        while position < length and is_whitespace(line[position]):
                            position += 1
                        # self.tokens.append(
                        #     TokenIdentifier(
                        #         TokenType.WHITESPACE,
                        #         line[start:position],
                        #         n_line + 1,
                        #         start,
                        #     )
                        # )
                    elif is_colon(char):
                        self.tokens.append(
                            TokenSymbol(
                                value=TokenType.COLON,
                                line=n_line + 1,
                                starting_position=position + 1,
                            )
                        )
                        position += 1
                    elif is_equal(char):
                        if position + 1 < length and line[position + 1] == "=":
                            self.tokens.append(
                                TokenSymbol(
                                    value=SymbolsDict["=="],
                                    line=n_line + 1,
                                    starting_position=position + 1,
                                )
                            )
                            position += 2  # Salta el siguiente carácter ya que es parte del token
                        else:
                            self.tokens.append(
                                TokenSymbol(
                                    value=SymbolsDict[char],
                                    line=n_line + 1,
                                    starting_position=position + 1,
                                )
                            )
                            position += 1

                    elif is_admiracion(char):
                        if position + 1 < length and line[position + 1] == "=":
                            char = "!="
                            position += 1
                        self.tokens.append(
                            TokenSymbol(
                                value=SymbolsDict[char],
                                line=n_line + 1,
                                starting_position=position + 1,
                            )
                        )
                        position += 1
                    elif is_arroba(char):
                        self.tokens.append(
                            TokenSymbol(
                                value=SymbolsDict[char],
                                line=n_line + 1,
                                starting_position=position + 1,
                            )
                        )
                        position += 1

                    elif is_dash(char):
                        initial_position = position
                        if position + 1 < length and line[position + 1] == ">":
                            char = "->"
                            position += 1
                        self.tokens.append(
                            TokenSymbol(
                                value=SymbolsDict[char],
                                line=n_line + 1,
                                starting_position=initial_position + 1,
                            )
                        )
                        position += 1

                    elif is_comma(char):
                        self.tokens.append(
                            TokenSymbol(
                                value=SymbolsDict[char],
                                line=n_line + 1,
                                starting_position=position + 1,
                            )
                        )
                        position += 1

                    else:
                        raise LexicalError(line=n_line + 1, position=position + 1)
            return self.tokens
        except LexicalError as e:
            self.tokens.append(f">>>Error lexico(linea:{e.line},posicion:{e.position})")

            return self.tokens


def token_to_string(self):
    """
    Convert tokens to a string representation for writing to a file.
    """
    result = []
    for token in self.tokens:
        result.append(str(token))
