from keyword import softkwlist
from utils import KEYWORDS
from Automat import AFD


def is_identifier_char(c):
    return c.isalnum() or c == "_"


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


class Lexer:
    def __init__(self, lines):
        self.lines = lines
        self.tokens = []
        self.space = " "
        self.keywords = KEYWORDS
        self.soft_keywords = softkwlist

    def tokenize_with_automat(self):
        estados = [
            "Inicio",
            "Num",
            "Letter",
            "Comment",
            "dot",
            "ID",
            "Simbolo",
            "OpenQuote",
            "str",
        ]
        alfabeto = ["%d", "%c", "%s", "#", '"', "'", "_", "whitespace"]
        transiciones = {
            "Inicio": {
                "%d": "Num",
                "%c": "Letter",
                "#": "Comment",
                "%s": "Simbolo",
                '"': "OpenQuote",
                "'": "OpenQuote",
            },
            "Num": {".": "dot"},
            "dot": {"%d": "Num"},
            "Letter": {
                "%c": "ID",
                "%d": "ID",
                "_": "ID",
            },
            "ID": {"%c": "ID", "%d": "ID", "_": "ID"},
            "Comment": {"%c": "Comment", "%d": "Comment"},
            "OpenQuote": {
                "%c": "OpenQuote",
                "%d": "OpenQuote",
                "%s": "OpenQuote",
                "whitespace": "OpenQuote",
                '"': "str",
                "'": "str",
            },
        }
        estadoInicial = "Inicio"
        estadosFinales = ["Num", "ID", "Comment", "Simbolo", "str"]

        afd = AFD(estados, alfabeto, transiciones, estadoInicial, estadosFinales)

        afd.read_lines(self.lines)

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
                                value=line[start:position],
                                line=self.lines.index(line) + 1,
                                starting_position=start + 1,
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
                                token_type=TokenType.STRING,
                                value=line[start:position],
                                line=self.lines.index(line) + 1,
                                starting_position=start,
                            )
                        )
                    else:
                        raise RuntimeError("Unterminated string literal")

                elif is_paren(char):
                    if char == "(":
                        self.tokens.append(
                            TokenSymbol(
                                value=TokenType.LPAREN,
                                line=self.lines.index(line) + 1,
                                starting_position=position + 1,
                            )
                        )
                    else:
                        self.tokens.append(
                            TokenSymbol(
                                value=TokenType.RPAREN,
                                line=self.lines.index(line) + 1,
                                starting_position=position,
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
                    #         self.lines.index(line) + 1,
                    #         start,
                    #     )
                    # )
                elif is_colon(char):
                    self.tokens.append(
                        TokenSymbol(
                            value=TokenType.COLON,
                            line=self.lines.index(line) + 1,
                            starting_position=position + 1,
                        )
                    )
                    position += 1

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


def token_to_string(self):
    """
    Convert tokens to a string representation for writing to a file.
    """
    result = []
    for token in self.tokens:
        result.append(str(token))
